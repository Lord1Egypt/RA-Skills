/**
 * AAWP Solana Raydium LP Module
 * Pool info, add/remove liquidity, search pools via Raydium API
 * Uses Raydium V2 HTTP API: https://api-v3.raydium.io
 */
'use strict';

const https = require('https');
const http = require('http');

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
const RAYDIUM_API = 'https://api-v3.raydium.io';

let _web3;
function getWeb3() { if (!_web3) _web3 = require('@solana/web3.js'); return _web3; }

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${d.slice(0, 200)}`));
        try { resolve(JSON.parse(d)); } catch { reject(new Error('Bad JSON: ' + d.slice(0, 200))); }
      });
    }).on('error', reject);
  });
}

function httpPost(url, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const payload = JSON.stringify(body);
    const opts = {
      hostname: u.hostname, port: u.port, path: u.pathname + u.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) },
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

/**
 * Get pool info by pool ID
 */
async function getPoolInfo(poolId) {
  const resp = await httpGet(`${RAYDIUM_API}/pools/info/ids?ids=${poolId}`);
  if (!resp || resp.success === false) throw new Error('Raydium API error: ' + JSON.stringify(resp).slice(0, 200));
  
  const data = resp.data || resp;
  if (Array.isArray(data) && data.length > 0) return data[0];
  if (data[poolId]) return data[poolId];
  throw new Error(`Pool not found: ${poolId}`);
}

/**
 * Search pools by token mint
 */
async function listPools(tokenMint) {
  const resp = await httpGet(`${RAYDIUM_API}/pools/info/mint?mint1=${tokenMint}&poolType=all&poolSortField=liquidity&sortType=desc&pageSize=10&page=1`);
  if (!resp || resp.success === false) throw new Error('Raydium API error: ' + JSON.stringify(resp).slice(0, 200));
  
  const data = resp.data || resp;
  if (data.data && Array.isArray(data.data)) return data.data;
  if (Array.isArray(data)) return data;
  return [];
}

/**
 * Add liquidity to a Raydium pool
 * Uses Raydium compute API for transaction building
 */
async function addLiquidity({ connection, user, poolId, amountA, amountB, slippage = 1, signTx }) {
  const { PublicKey, VersionedTransaction } = getWeb3();
  const userPk = new PublicKey(user);

  // Get pool info first to determine mints and decimals
  const pool = await getPoolInfo(poolId);
  const mintA = pool.mintA || pool.baseMint;
  const mintB = pool.mintB || pool.quoteMint;
  
  if (!mintA || !mintB) throw new Error('Cannot determine pool mints');

  const decimalsA = mintA.decimals || pool.mintADecimals || 9;
  const decimalsB = mintB.decimals || pool.mintBDecimals || 6;
  const mintAAddr = mintA.address || mintA;
  const mintBAddr = mintB.address || mintB;

  const rawAmountA = BigInt(Math.round(amountA * Math.pow(10, decimalsA)));
  const rawAmountB = BigInt(Math.round(amountB * Math.pow(10, decimalsB)));

  // Use Raydium's compute API for deposit
  const computeResp = await httpPost(`${RAYDIUM_API}/liquidity/add`, {
    id: poolId,
    inputAmount: rawAmountA.toString(),
    otherAmountThreshold: rawAmountB.toString(),
    fixedSide: 'a',
    slippage: slippage / 100, // API expects decimal
    wallet: user,
  });

  if (!computeResp || (!computeResp.data && !computeResp.transaction)) {
    throw new Error('Raydium compute API failed: ' + JSON.stringify(computeResp).slice(0, 300));
  }

  const txData = computeResp.data?.transaction || computeResp.transaction;
  if (!txData) throw new Error('No transaction returned from Raydium API');

  // Sign and send versioned transaction
  const txBuf = Buffer.from(txData, 'base64');
  const vtx = VersionedTransaction.deserialize(txBuf);
  const msgBytes = Buffer.from(vtx.message.serialize());
  const sig = await signTx(msgBytes);
  vtx.signatures[0] = sig;

  const rawTx = Buffer.from(vtx.serialize());
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, poolId, amountA, amountB };
}

/**
 * Remove liquidity from a Raydium pool
 */
async function removeLiquidity({ connection, user, poolId, lpAmount, slippage = 1, signTx }) {
  const { PublicKey, VersionedTransaction } = getWeb3();
  const userPk = new PublicKey(user);

  // Get pool info for LP decimals
  const pool = await getPoolInfo(poolId);
  const lpDecimals = pool.lpDecimals || pool.lpMint?.decimals || 9;
  const rawLpAmount = BigInt(Math.round(lpAmount * Math.pow(10, lpDecimals)));

  // Use Raydium's compute API for withdrawal
  const computeResp = await httpPost(`${RAYDIUM_API}/liquidity/remove`, {
    id: poolId,
    lpAmount: rawLpAmount.toString(),
    slippage: slippage / 100,
    wallet: user,
  });

  if (!computeResp || (!computeResp.data && !computeResp.transaction)) {
    throw new Error('Raydium compute API failed: ' + JSON.stringify(computeResp).slice(0, 300));
  }

  const txData = computeResp.data?.transaction || computeResp.transaction;
  if (!txData) throw new Error('No transaction returned from Raydium API');

  const txBuf = Buffer.from(txData, 'base64');
  const vtx = VersionedTransaction.deserialize(txBuf);
  const msgBytes = Buffer.from(vtx.message.serialize());
  const sig = await signTx(msgBytes);
  vtx.signatures[0] = sig;

  const rawTx = Buffer.from(vtx.serialize());
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, poolId, lpAmount };
}

module.exports = { getPoolInfo, listPools, addLiquidity, removeLiquidity };
