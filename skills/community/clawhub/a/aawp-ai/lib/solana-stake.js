/**
 * AAWP Solana Staking Module
 * Native SOL staking + Marinade liquid staking
 */
'use strict';

const https = require('https');
const http = require('http');

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';

// Marinade program IDs
const MARINADE_PROGRAM = 'MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD';
const MSOL_MINT = 'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So';

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

/**
 * Create a stake account and delegate to a validator
 */
async function stake({ connection, user, amount, validatorVoteAccount, signTx }) {
  const {
    PublicKey, Transaction, ComputeBudgetProgram, StakeProgram,
    SystemProgram, Authorized, Lockup, LAMPORTS_PER_SOL,
  } = getWeb3();

  const userPk = new PublicKey(user);
  const votePk = new PublicKey(validatorVoteAccount);
  const lamports = Math.round(amount * LAMPORTS_PER_SOL);

  // Generate a deterministic stake account seed from user + timestamp
  const seed = `stake-${Date.now()}`;
  const stakeAccountPk = await PublicKey.createWithSeed(userPk, seed, StakeProgram.programId);

  // Minimum delegation rent
  const rentExempt = await connection.getMinimumBalanceForRentExemption(200); // StakeAccount size
  const totalLamports = lamports + rentExempt;

  const createIx = SystemProgram.createAccountWithSeed({
    fromPubkey: userPk,
    newAccountPubkey: stakeAccountPk,
    basePubkey: userPk,
    seed,
    lamports: totalLamports,
    space: 200,
    programId: StakeProgram.programId,
  });

  const initIx = StakeProgram.initialize({
    stakePubkey: stakeAccountPk,
    authorized: new Authorized(userPk, userPk),
    lockup: new Lockup(0, 0, userPk),
  });

  const delegateIx = StakeProgram.delegate({
    stakePubkey: stakeAccountPk,
    authorizedPubkey: userPk,
    votePubkey: votePk,
  });

  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 300_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(createIx);
  tx.add(initIx);
  tx.add(delegateIx);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, stakeAccount: stakeAccountPk.toBase58(), amount: lamports, validator: validatorVoteAccount };
}

/**
 * Deactivate (unstake) a stake account
 */
async function unstake({ connection, user, stakeAccount, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram, StakeProgram } = getWeb3();

  const userPk = new PublicKey(user);
  const stakePk = new PublicKey(stakeAccount);

  const deactivateIx = StakeProgram.deactivate({
    stakePubkey: stakePk,
    authorizedPubkey: userPk,
  });

  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(deactivateIx);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig };
}

/**
 * Withdraw SOL from a deactivated stake account
 */
async function withdrawStake({ connection, user, stakeAccount, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram, StakeProgram } = getWeb3();

  const userPk = new PublicKey(user);
  const stakePk = new PublicKey(stakeAccount);

  // Get stake account balance
  const stakeInfo = await connection.getAccountInfo(stakePk);
  if (!stakeInfo) throw new Error('Stake account not found');
  const lamports = stakeInfo.lamports;

  const withdrawIx = StakeProgram.withdraw({
    stakePubkey: stakePk,
    authorizedPubkey: userPk,
    toPubkey: userPk,
    lamports,
  });

  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(withdrawIx);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, amount: lamports };
}

/**
 * List all stake accounts for a user
 */
async function getStakeAccounts(user, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey, StakeProgram } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');
  const userPk = new PublicKey(user);

  // Get all stake accounts where the user is the authorized staker
  const accounts = await conn.getParsedProgramAccounts(StakeProgram.programId, {
    filters: [
      { memcmp: { offset: 12, bytes: userPk.toBase58() } }, // authorized.staker at offset 12
    ],
  });

  return accounts.map(a => {
    const parsed = a.account.data.parsed;
    const info = parsed?.info || {};
    const stake = info.stake || {};
    const meta = info.meta || {};

    let state = 'unknown';
    if (parsed.type === 'delegated') state = 'active';
    else if (parsed.type === 'initialized') state = 'initialized';

    // Check activation/deactivation
    const delegation = stake.delegation || {};
    if (delegation.deactivationEpoch && delegation.deactivationEpoch !== '18446744073709551615') {
      state = 'deactivating';
    }

    return {
      pubkey: a.pubkey.toBase58(),
      lamports: a.account.lamports,
      state,
      voter: delegation.voter || null,
      activationEpoch: delegation.activationEpoch || null,
      deactivationEpoch: delegation.deactivationEpoch || null,
      rentExemptReserve: meta.rentExemptReserve || null,
    };
  });
}

/**
 * Stake SOL for mSOL via Marinade Finance
 * Uses Marinade's staking API endpoint for transaction building
 */
async function marinadeMSOL({ connection, user, amount, signTx }) {
  const { PublicKey, VersionedTransaction, LAMPORTS_PER_SOL } = getWeb3();
  const userPk = new PublicKey(user);
  const lamports = Math.round(amount * LAMPORTS_PER_SOL);

  // Use Marinade API to get the stake transaction
  try {
    const resp = await httpGet(`https://api.marinade.finance/v1/deposit?amount=${lamports}&wallet=${user}`);
    if (!resp || !resp.transaction) throw new Error('Marinade API did not return a transaction');

    const txBuf = Buffer.from(resp.transaction, 'base64');
    const vtx = VersionedTransaction.deserialize(txBuf);
    const msgBytes = Buffer.from(vtx.message.serialize());
    const sig = await signTx(msgBytes);
    vtx.signatures[0] = sig;

    const rawTx = Buffer.from(vtx.serialize());
    const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
    const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
    await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

    return { signature: txSig, amount: lamports, msolMint: MSOL_MINT };
  } catch (e) {
    throw new Error(`Marinade stake failed: ${e.message}. You may need to use a direct swap via Jupiter: swap SOL mSOL`);
  }
}

/**
 * Unstake mSOL back to SOL via Marinade
 */
async function marinadeUnstake({ connection, user, amount, signTx }) {
  const { PublicKey, VersionedTransaction } = getWeb3();
  const userPk = new PublicKey(user);

  // mSOL has 9 decimals
  const rawAmount = Math.round(amount * 1e9);

  try {
    const resp = await httpGet(`https://api.marinade.finance/v1/withdraw?amount=${rawAmount}&wallet=${user}`);
    if (!resp || !resp.transaction) throw new Error('Marinade API did not return a transaction');

    const txBuf = Buffer.from(resp.transaction, 'base64');
    const vtx = VersionedTransaction.deserialize(txBuf);
    const msgBytes = Buffer.from(vtx.message.serialize());
    const sig = await signTx(msgBytes);
    vtx.signatures[0] = sig;

    const rawTx = Buffer.from(vtx.serialize());
    const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
    const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
    await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

    return { signature: txSig, amount: rawAmount };
  } catch (e) {
    throw new Error(`Marinade unstake failed: ${e.message}. You may need to use a direct swap via Jupiter: swap mSOL SOL`);
  }
}

module.exports = { stake, unstake, withdrawStake, getStakeAccounts, marinadeMSOL, marinadeUnstake, MSOL_MINT };
