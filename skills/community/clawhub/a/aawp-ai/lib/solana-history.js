/**
 * AAWP Solana Transaction History Module
 * Fetch and parse recent transactions
 */
'use strict';

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';

let _web3;
function getWeb3() { if (!_web3) _web3 = require('@solana/web3.js'); return _web3; }

/**
 * Classify a parsed transaction
 */
function classifyTransaction(parsedTx) {
  if (!parsedTx || !parsedTx.meta) return { type: 'unknown', details: '' };

  const instructions = parsedTx.transaction?.message?.instructions || [];
  const logMessages = parsedTx.meta.logMessages || [];

  // Check log messages for common patterns
  const logStr = logMessages.join(' ');
  if (logStr.includes('Swap') || logStr.includes('swap') || logStr.includes('Route')) {
    return { type: 'swap', details: 'Token swap' };
  }
  if (logStr.includes('Transfer') && logStr.includes('spl-token')) {
    return { type: 'token-transfer', details: 'SPL token transfer' };
  }
  if (logStr.includes('CreateAccount') || logStr.includes('InitializeAccount')) {
    return { type: 'account-create', details: 'Account creation' };
  }

  // Check instruction programs
  for (const ix of instructions) {
    const prog = ix.programId?.toBase58?.() || ix.programId || '';
    const pStr = typeof prog === 'string' ? prog : '';

    if (pStr === '11111111111111111111111111111111') {
      const ixType = ix.parsed?.type || '';
      if (ixType === 'transfer') {
        const info = ix.parsed?.info || {};
        const sol = info.lamports ? (info.lamports / 1e9).toFixed(6) + ' SOL' : '';
        return { type: 'sol-transfer', details: `${sol} → ${info.destination || '?'}` };
      }
      return { type: 'system', details: ixType || 'System program' };
    }

    // SPL Token program
    if (pStr === 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA' ||
        pStr === 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb') {
      const ixType = ix.parsed?.type || '';
      if (ixType === 'transfer' || ixType === 'transferChecked') {
        const info = ix.parsed?.info || {};
        return { type: 'token-transfer', details: `${info.tokenAmount?.uiAmount || info.amount || '?'} tokens` };
      }
      return { type: 'token-op', details: ixType || 'Token operation' };
    }

    // Jupiter / Pump etc
    if (pStr.includes('JUP') || pStr === 'JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4') {
      return { type: 'swap', details: 'Jupiter swap' };
    }
    if (pStr === '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P') {
      return { type: 'pump-trade', details: 'Pump.fun trade' };
    }
  }

  // Fallback: check pre/post balances
  if (parsedTx.meta.preBalances && parsedTx.meta.postBalances) {
    const diff = parsedTx.meta.postBalances[0] - parsedTx.meta.preBalances[0];
    if (Math.abs(diff) > 5000) {
      return { type: 'sol-transfer', details: `${(diff / 1e9).toFixed(6)} SOL change` };
    }
  }

  return { type: 'unknown', details: '' };
}

/**
 * Get transaction history for an address
 * @param {string} address - Solana address
 * @param {number} limit - max transactions to fetch
 * @param {string} rpcUrl - RPC endpoint
 */
async function getHistory(address, limit = 20, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');
  const pubkey = new PublicKey(address);

  // Get signatures
  const sigs = await conn.getSignaturesForAddress(pubkey, { limit });

  const results = [];
  // Fetch parsed details in batches (avoid overwhelming RPC)
  const batchSize = 5;
  for (let i = 0; i < sigs.length; i += batchSize) {
    const batch = sigs.slice(i, i + batchSize);
    const promises = batch.map(async (sigInfo) => {
      let classified = { type: 'unknown', details: '' };
      try {
        const parsed = await conn.getParsedTransaction(sigInfo.signature, {
          maxSupportedTransactionVersion: 0,
        });
        classified = classifyTransaction(parsed);
      } catch (_) {}

      return {
        signature: sigInfo.signature,
        timestamp: sigInfo.blockTime,
        err: sigInfo.err,
        memo: sigInfo.memo,
        type: classified.type,
        details: classified.details,
      };
    });
    const batchResults = await Promise.all(promises);
    results.push(...batchResults);
  }

  return results;
}

module.exports = { getHistory, classifyTransaction };
