/**
 * AAWP Solana Portfolio Module
 * List all token holdings with USD values via Jupiter price API
 */
'use strict';

const https = require('https');
const http = require('http');

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
const SOL_MINT = 'So11111111111111111111111111111111111111112';

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

// Cache Jupiter token list for the session
let _tokenListCache = null;
let _tokenListTs = 0;

async function getTokenList() {
  if (_tokenListCache && Date.now() - _tokenListTs < 300_000) return _tokenListCache;
  try {
    const list = await httpGet('https://lite-api.jup.ag/tokens/v2/mints/tradable');
    const map = {};
    if (Array.isArray(list)) {
      for (const t of list) {
        if (t.address || t.id) map[t.address || t.id] = t;
      }
    }
    _tokenListCache = map;
    _tokenListTs = Date.now();
    return map;
  } catch (_) {
    return {};
  }
}

async function getPrices(mints) {
  if (!mints.length) return {};
  // Jupiter price API: batch up to 100 at a time
  const results = {};
  const batchSize = 100;
  for (let i = 0; i < mints.length; i += batchSize) {
    const batch = mints.slice(i, i + batchSize);
    try {
      const url = `https://lite-api.jup.ag/price/v3?ids=${batch.join(',')}`;
      const data = await httpGet(url);
      if (data && data.data) {
        for (const [k, v] of Object.entries(data.data)) {
          if (v && v.price) results[k] = parseFloat(v.price);
        }
      } else if (data) {
        for (const [k, v] of Object.entries(data)) {
          if (v && v.usdPrice) results[k] = parseFloat(v.usdPrice);
          else if (v && v.price) results[k] = parseFloat(v.price);
        }
      }
    } catch (_) {}
  }
  return results;
}

/**
 * Get full portfolio for an address
 */
async function getPortfolio(owner, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const spl = require('@solana/spl-token');
  const conn = new Connection(rpcUrl, 'confirmed');
  const ownerPk = new PublicKey(owner);

  // Get SOL balance
  const solLamports = await conn.getBalance(ownerPk);
  const solBalance = solLamports / 1e9;

  // Get all token accounts (Token + Token-2022)
  const tokenAccounts = [];
  for (const programId of [spl.TOKEN_PROGRAM_ID, spl.TOKEN_2022_PROGRAM_ID]) {
    try {
      const resp = await conn.getParsedTokenAccountsByOwner(ownerPk, { programId });
      for (const item of resp.value) {
        const parsed = item.account.data.parsed.info;
        if (parseFloat(parsed.tokenAmount.amount) > 0) {
          tokenAccounts.push({
            mint: parsed.mint,
            balance: parsed.tokenAmount.uiAmount,
            decimals: parsed.tokenAmount.decimals,
            rawBalance: parsed.tokenAmount.amount,
          });
        }
      }
    } catch (_) {}
  }

  // Get token metadata (symbols) from Jupiter
  const tokenList = await getTokenList();

  // Get prices for all mints + SOL
  const allMints = [SOL_MINT, ...tokenAccounts.map(t => t.mint)];
  const prices = await getPrices(allMints);

  const solPrice = prices[SOL_MINT] || 0;
  const solValueUSD = solBalance * solPrice;

  const tokens = tokenAccounts.map(t => {
    const info = tokenList[t.mint];
    const price = prices[t.mint] || 0;
    return {
      mint: t.mint,
      symbol: info?.symbol || null,
      name: info?.name || null,
      balance: t.balance,
      decimals: t.decimals,
      priceUSD: price,
      valueUSD: t.balance * price,
    };
  });

  // Sort by USD value descending
  tokens.sort((a, b) => b.valueUSD - a.valueUSD);

  const tokenTotalUSD = tokens.reduce((s, t) => s + t.valueUSD, 0);

  return {
    owner,
    solBalance,
    solPrice,
    solValueUSD,
    tokens,
    totalValueUSD: solValueUSD + tokenTotalUSD,
  };
}

module.exports = { getPortfolio, getPrices, getTokenList };
