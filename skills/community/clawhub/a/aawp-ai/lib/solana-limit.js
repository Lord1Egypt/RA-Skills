/**
 * AAWP Solana Jupiter Limit Orders Module
 * Place, list, cancel limit orders via Jupiter Limit Order API v2
 * API: https://api.jup.ag/limit-order/v2
 * Requires JUP_API_KEY env var (paid Jupiter API access)
 */
'use strict';

const https = require('https');
const http = require('http');

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
const LIMIT_API = 'https://api.jup.ag/limit-order/v2';
const SOL_MINT = 'So11111111111111111111111111111111111111112';

let _web3;
function getWeb3() { if (!_web3) _web3 = require('@solana/web3.js'); return _web3; }

function getApiKey() {
  const key = process.env.JUP_API_KEY;
  if (!key) throw new Error('Jupiter API key required. Set JUP_API_KEY env var. Get one at https://portal.jup.ag');
  return key;
}

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const opts = { hostname: u.hostname, port: u.port, path: u.pathname + u.search, headers };
    mod.get(opts, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${d.slice(0, 200)}`));
        try { resolve(JSON.parse(d)); } catch { reject(new Error('Bad JSON: ' + d.slice(0, 200))); }
      });
    }).on('error', reject);
  });
}

function httpPost(url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const payload = JSON.stringify(body);
    const opts = {
      hostname: u.hostname, port: u.port, path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload), ...headers },
    };
    const req = mod.request(opts, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${d.slice(0, 300)}`));
        try { resolve(JSON.parse(d)); } catch { reject(new Error('Bad JSON: ' + d.slice(0, 200))); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function authHeaders() {
  return { 'x-api-key': getApiKey() };
}

async function getMintDecimals(connection, mint) {
  const { PublicKey } = getWeb3();
  if (mint === SOL_MINT) return 9;
  const info = await connection.getParsedAccountInfo(new PublicKey(mint));
  if (!info.value) throw new Error(`Mint not found: ${mint}`);
  return info.value.data.parsed.info.decimals;
}

/**
 * Create a limit order via Jupiter Limit Order API v2
 */
async function createLimitOrder({ connection, user, inputMint, outputMint, inAmount, outAmount, expiredAt, signTx }) {
  const { VersionedTransaction, PublicKey } = getWeb3();
  const headers = authHeaders();

  const inDecimals = await getMintDecimals(connection, inputMint);
  const outDecimals = await getMintDecimals(connection, outputMint);

  const makingAmount = BigInt(Math.round(inAmount * Math.pow(10, inDecimals))).toString();
  const takingAmount = BigInt(Math.round(outAmount * Math.pow(10, outDecimals))).toString();

  const body = {
    maker: user,
    payer: user,
    inputMint,
    outputMint,
    makingAmount,
    takingAmount,
    computeUnitPrice: '50000',
  };
  if (expiredAt) body.expiredAt = expiredAt.toString();

  const resp = await httpPost(`${LIMIT_API}/create-order`, body, headers);
  if (!resp || !resp.tx) throw new Error('Limit order API failed: ' + JSON.stringify(resp).slice(0, 300));

  const txBuf = Buffer.from(resp.tx, 'base64');
  const vtx = VersionedTransaction.deserialize(txBuf);
  const msgBytes = Buffer.from(vtx.message.serialize());
  const sig = await signTx(msgBytes);
  vtx.signatures[0] = sig;

  const rawTx = Buffer.from(vtx.serialize());
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, order: resp.orderPubkey || null };
}

/**
 * Get open limit orders for a user
 */
async function getOpenOrders(user) {
  const headers = authHeaders();
  const resp = await httpGet(`${LIMIT_API}/open-orders?wallet=${user}`, headers);
  if (Array.isArray(resp)) return resp;
  if (resp && resp.orders) return resp.orders;
  return [];
}

/**
 * Cancel a limit order
 */
async function cancelOrder({ connection, user, orderPubkey, signTx }) {
  const { VersionedTransaction } = getWeb3();
  const headers = authHeaders();

  const resp = await httpPost(`${LIMIT_API}/cancel-order`, {
    maker: user,
    orders: [orderPubkey],
    computeUnitPrice: '50000',
  }, headers);
  if (!resp || !resp.tx) throw new Error('Cancel order API failed: ' + JSON.stringify(resp).slice(0, 300));

  const txBuf = Buffer.from(resp.tx, 'base64');
  const vtx = VersionedTransaction.deserialize(txBuf);
  const msgBytes = Buffer.from(vtx.message.serialize());
  const sig = await signTx(msgBytes);
  vtx.signatures[0] = sig;

  const rawTx = Buffer.from(vtx.serialize());
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig };
}

/**
 * Get order history for a user
 */
async function getOrderHistory(user) {
  const headers = authHeaders();
  const resp = await httpGet(`${LIMIT_API}/order-history?wallet=${user}`, headers);
  if (Array.isArray(resp)) return resp;
  if (resp && resp.orders) return resp.orders;
  return [];
}

module.exports = { createLimitOrder, getOpenOrders, cancelOrder, getOrderHistory };
