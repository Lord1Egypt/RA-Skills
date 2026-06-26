/**
 * AAWP Solana Swap Module (thin wrapper)
 * Primary: pump.js (bonding curve + AMM auto-detect)
 * Fallback: Jupiter Metis Swap API
 */
'use strict';

const https = require('https');
const http = require('http');

const SOL_MINT = 'So11111111111111111111111111111111111111112';
const USDC_MINT = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';

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

function resolveToken(symbol) {
  const lower = (symbol || '').toLowerCase();
  if (lower === 'sol' || lower === 'wsol') return SOL_MINT;
  if (lower === 'usdc') return USDC_MINT;
  if (symbol.length >= 32 && /^[1-9A-HJ-NP-Za-km-z]+$/.test(symbol)) return symbol;
  return null;
}

async function searchToken(query) {
  try {
    const results = await httpGet(`https://lite-api.jup.ag/tokens/v2/search?query=${encodeURIComponent(query)}`);
    if (Array.isArray(results) && results.length > 0) return results[0];
  } catch (_) {}
  return null;
}

async function getPrice(mint) {
  const data = await httpGet(`https://lite-api.jup.ag/price/v3?ids=${mint}`);
  if (data && data[mint]) return { price: data[mint].usdPrice, ...data[mint] };
  if (data && data.data && data.data[mint]) return data.data[mint];
  return null;
}

// Jupiter Metis fallback
async function jupiterSwap({ inputMint, outputMint, amount, slippageBps, userPublicKey, signTx, connection }) {
  const { VersionedTransaction } = require('@solana/web3.js');
  const quoteUrl = `https://lite-api.jup.ag/swap/v1/quote?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${slippageBps}&restrictIntermediateTokens=true`;
  const quote = await httpGet(quoteUrl);
  if (!quote || quote.error) throw new Error('Jupiter quote failed: ' + JSON.stringify(quote));

  console.log(`[swap] Jupiter quote: ${quote.inAmount} → ${quote.outAmount} (impact: ${quote.priceImpactPct}%)`);

  const swapResp = await httpPost('https://lite-api.jup.ag/swap/v1/swap', {
    quoteResponse: quote, userPublicKey,
    dynamicComputeUnitLimit: true, dynamicSlippage: true,
    prioritizationFeeLamports: { priorityLevelWithMaxLamports: { maxLamports: 500000, priorityLevel: 'veryHigh' } },
  });
  if (!swapResp || !swapResp.swapTransaction) throw new Error('Jupiter swap build failed');

  const txBuf = Buffer.from(swapResp.swapTransaction, 'base64');
  const vtx = VersionedTransaction.deserialize(txBuf);
  const msgBytes = Buffer.from(vtx.message.serialize());
  const sig = await signTx(msgBytes);
  vtx.signatures[0] = sig;

  const rawTx = Buffer.from(vtx.serialize());
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, route: 'jupiter', inAmount: quote.inAmount, outAmount: quote.outAmount, priceImpact: quote.priceImpactPct };
}

/**
 * Main swap: tries Pump SDK first, then Jupiter
 */
async function swap(opts) {
  const { Connection } = require('@solana/web3.js');
  const pump = require('./pump');
  const rpcUrl = opts.rpcUrl || process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
  const connection = new Connection(rpcUrl, 'confirmed');
  const signerPk = await opts.getAddress();

  let inputMint = resolveToken(opts.from);
  let outputMint = resolveToken(opts.to);
  if (!inputMint) { const i = await searchToken(opts.from); if (i) inputMint = i.id || i.address; else throw new Error(`Cannot resolve: ${opts.from}`); }
  if (!outputMint) { const i = await searchToken(opts.to); if (i) outputMint = i.id || i.address; else throw new Error(`Cannot resolve: ${opts.to}`); }

  const isBuy = inputMint === SOL_MINT;
  const pool = opts.pool || 'pump';

  if (pool !== 'jupiter') {
    try {
      const tokenMint = isBuy ? outputMint : inputMint;
      console.log(`[swap] Pump.fun SDK: smart swap...`);

      if (isBuy) {
        const solLamports = Math.round(opts.amount * 1e9);
        return await pump.smartSwap({ connection, mint: tokenMint, user: signerPk, action: 'buy', amount: solLamports, slippage: opts.slippage || 15, signTx: opts.signTx });
      } else {
        return await pump.smartSwap({ connection, mint: tokenMint, user: signerPk, action: 'sell', amount: Math.round(opts.amount), slippage: opts.slippage || 15, signTx: opts.signTx });
      }
    } catch (e) {
      console.error(`[swap] Pump SDK failed: ${e.message}`);
      if (pool !== 'jupiter') console.log('[swap] Falling back to Jupiter...');
      else throw e;
    }
  }

  // Jupiter fallback
  console.log(`[swap] Jupiter Metis...`);
  let amountRaw;
  if (inputMint === SOL_MINT) { amountRaw = Math.round(opts.amount * 1e9); }
  else { const i = await searchToken(opts.from); amountRaw = Math.round(opts.amount * Math.pow(10, i?.decimals || 6)); }

  return jupiterSwap({ inputMint, outputMint, amount: amountRaw, slippageBps: Math.round((opts.slippage || 1.5) * 100), userPublicKey: signerPk, signTx: opts.signTx, connection });
}

module.exports = { swap, getPrice, searchToken, resolveToken, jupiterSwap, SOL_MINT, USDC_MINT };
