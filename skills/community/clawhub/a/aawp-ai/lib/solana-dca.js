/**
 * AAWP Solana Jupiter DCA Module
 * Dollar-cost averaging via Jupiter DCA program
 * Program: DCA265Vj8a9CE9x8BmVUGMRMCfKTiaNqKJrBKQdLQ
 */
'use strict';

const https = require('https');
const http = require('http');
const crypto = require('crypto');

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
const DCA_PROGRAM = 'DCAK36VfExkPdAkYUQg6ewgxyinvcEyPLyHjRbmveKFw';
const SOL_MINT = 'So11111111111111111111111111111111111111112';
const JUP_DCA_API = 'https://dca-api.jup.ag';

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

async function getMintDecimals(connection, mint) {
  const { PublicKey } = getWeb3();
  const info = await connection.getParsedAccountInfo(new PublicKey(mint));
  if (!info.value) throw new Error(`Mint not found: ${mint}`);
  return info.value.data.parsed.info.decimals;
}

/**
 * Create a DCA position using Jupiter DCA API
 */
async function createDCA({ connection, user, inputMint, outputMint, inAmount, inAmountPerCycle, cycleFrequency, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram, Keypair, SystemProgram } = getWeb3();
  const spl = require('@solana/spl-token');

  const userPk = new PublicKey(user);
  const inputMintPk = new PublicKey(inputMint);
  const outputMintPk = new PublicKey(outputMint);

  // Get decimals
  let decimals;
  if (inputMint === SOL_MINT) {
    decimals = 9;
  } else {
    decimals = await getMintDecimals(connection, inputMint);
  }

  const totalRaw = BigInt(Math.round(inAmount * Math.pow(10, decimals)));
  const perCycleRaw = BigInt(Math.round(inAmountPerCycle * Math.pow(10, decimals)));

  // Derive DCA account PDA
  // The DCA program uses a random seed for the DCA account
  const dcaSeed = crypto.randomBytes(8);
  const [dcaPda] = PublicKey.findProgramAddressSync(
    [Buffer.from('dca'), userPk.toBuffer(), dcaSeed],
    new PublicKey(DCA_PROGRAM)
  );

  // Detect token program for input
  let inputTokenProgram = spl.TOKEN_PROGRAM_ID;
  if (inputMint !== SOL_MINT) {
    const mintInfo = await connection.getAccountInfo(inputMintPk);
    if (mintInfo && mintInfo.owner.toBase58() === spl.TOKEN_2022_PROGRAM_ID.toBase58()) {
      inputTokenProgram = spl.TOKEN_2022_PROGRAM_ID;
    }
  }

  // Get user's input ATA
  const userInAta = spl.getAssociatedTokenAddressSync(inputMintPk, userPk, true, inputTokenProgram);

  // Build open DCA instruction data
  // Discriminator for "open_dca" = first 8 bytes of sha256("global:open_dca")
  const discrim = crypto.createHash('sha256').update('global:open_dca').digest().subarray(0, 8);
  const data = Buffer.alloc(8 + 8 + 8 + 8 + 8 + 8 + 1); // disc + inAmount + perCycle + cycleFreq + minOut + maxOut + pad
  discrim.copy(data, 0);
  data.writeBigUInt64LE(totalRaw, 8);
  data.writeBigUInt64LE(perCycleRaw, 16);
  data.writeBigInt64LE(BigInt(cycleFrequency), 24);
  // minOutPerCycle = 0 (no minimum)
  data.writeBigUInt64LE(0n, 32);
  // maxOutPerCycle = max (no maximum)
  data.writeBigUInt64LE(BigInt('18446744073709551615'), 40);

  const dcaProgramPk = new PublicKey(DCA_PROGRAM);

  // DCA account keys following the program's expected layout
  const ix = {
    programId: dcaProgramPk,
    keys: [
      { pubkey: dcaPda, isSigner: false, isWritable: true },
      { pubkey: userPk, isSigner: true, isWritable: true },
      { pubkey: inputMintPk, isSigner: false, isWritable: false },
      { pubkey: outputMintPk, isSigner: false, isWritable: false },
      { pubkey: userInAta, isSigner: false, isWritable: true },
      { pubkey: spl.getAssociatedTokenAddressSync(inputMintPk, dcaPda, true, inputTokenProgram), isSigner: false, isWritable: true },
      { pubkey: spl.getAssociatedTokenAddressSync(outputMintPk, dcaPda, true), isSigner: false, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
      { pubkey: inputTokenProgram, isSigner: false, isWritable: false },
      { pubkey: spl.TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      { pubkey: spl.ASSOCIATED_TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
    ],
    data,
  };

  // Use the buildAndSign pattern from pump.js
  const { Transaction: Tx, ComputeBudgetProgram: CBP } = getWeb3();
  const tx = new Tx();
  tx.add(CBP.setComputeUnitLimit({ units: 300_000 }));
  tx.add(CBP.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(ix);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, dcaAccount: dcaPda.toBase58() };
}

/**
 * List active DCA positions for a user
 */
async function getDCAAccounts(user, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');
  const dcaProgramPk = new PublicKey(DCA_PROGRAM);

  // Fetch all program accounts owned by DCA program that match user
  try {
    const accounts = await conn.getProgramAccounts(dcaProgramPk, {
      filters: [
        { memcmp: { offset: 8, bytes: new PublicKey(user).toBase58() } }, // user pubkey at offset 8
      ],
    });

    return accounts.map(a => {
      const data = a.account.data;
      let parsed = { pubkey: a.pubkey.toBase58() };
      try {
        // Parse DCA account data
        if (data.length >= 72) {
          parsed.user = new PublicKey(data.subarray(8, 40)).toBase58();
          parsed.inputMint = new PublicKey(data.subarray(40, 72)).toBase58();
          if (data.length >= 104) {
            parsed.outputMint = new PublicKey(data.subarray(72, 104)).toBase58();
          }
          if (data.length >= 120) {
            parsed.inDeposited = Number(data.readBigUInt64LE(104));
            if (data.length >= 128) parsed.inWithdrawn = Number(data.readBigUInt64LE(112));
          }
        }
      } catch (_) {}
      return parsed;
    });
  } catch (e) {
    // Fallback: try Jupiter API
    try {
      const resp = await httpGet(`${JUP_DCA_API}/user/${user}`);
      return Array.isArray(resp) ? resp : (resp.dcaAccounts || []);
    } catch (_) {
      throw e;
    }
  }
}

/**
 * Close a DCA position
 */
async function closeDCA({ connection, user, dcaAccount, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram, SystemProgram } = getWeb3();
  const spl = require('@solana/spl-token');

  const userPk = new PublicKey(user);
  const dcaPk = new PublicKey(dcaAccount);
  const dcaProgramPk = new PublicKey(DCA_PROGRAM);

  // Discriminator for "close_dca"
  const discrim = crypto.createHash('sha256').update('global:close_dca').digest().subarray(0, 8);

  const ix = {
    programId: dcaProgramPk,
    keys: [
      { pubkey: dcaPk, isSigner: false, isWritable: true },
      { pubkey: userPk, isSigner: true, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
    ],
    data: discrim,
  };

  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(ix);

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

module.exports = { createDCA, getDCAAccounts, closeDCA, DCA_PROGRAM };
