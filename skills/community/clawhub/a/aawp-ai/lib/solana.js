#!/usr/bin/env node
/**
 * AAWP Solana Module — Solana-specific wallet operations
 * Uses AAWP daemon for Ed25519 signing via Unix socket
 */
'use strict';

const net = require('net');
const crypto = require('crypto');
const path = require('path');

const PROGRAM_ID_STR = 'AAwpAAQSVAZYHvpUW5uz7zxqj7RYTYR6CZvWL9wf4qiS';
const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';

let _web3;
function getWeb3() {
  if (!_web3) _web3 = require('@solana/web3.js');
  return _web3;
}

let _addon;
function getAddon() {
  if (!_addon) {
    const nativePath = path.join(__dirname, '..', 'native', 'aawp-core', 'aawp-core.node');
    _addon = require(nativePath);
  }
  return _addon;
}

function disc(name) {
  return crypto.createHash('sha256').update(`global:${name}`).digest().subarray(0, 8);
}

function findPda(seeds) {
  const { PublicKey } = getWeb3();
  const programId = new PublicKey(PROGRAM_ID_STR);
  return PublicKey.findProgramAddressSync(seeds, programId);
}

// ── Daemon Commands ──

function sendDaemonCmd(params) {
  return new Promise((resolve, reject) => {
    const addon = getAddon();
    const sockPath = addon._x0();
    const ts = Math.floor(Date.now() / 1000);
    const configDir = process.env.AAWP_CONFIG || '/root/clawd/skills/aawp/.agent-config';
    const hmac = addon._h0(ts, configDir);
    const req = { ...params, ts, hmac };
    const client = net.createConnection(sockPath, () => {
      client.write(JSON.stringify(req));
      client.end();
    });
    let data = '';
    client.on('data', chunk => { data += chunk; });
    client.on('end', () => {
      try {
        const r = JSON.parse(data);
        if (r.error) return reject(new Error(r.error));
        resolve(r);
      } catch (e) { reject(new Error('Bad daemon response: ' + data)); }
    });
    client.on('error', reject);
  });
}

/**
 * Get the Solana AI signer address from the AAWP daemon
 */
async function getAddress() {
  const resp = await sendDaemonCmd({ cmd: 'sol_address' });
  return resp.solAddress;
}

/**
 * Sign a message with the Solana Ed25519 key via daemon
 * @param {Buffer} message - raw bytes to sign
 * @returns {Buffer} 64-byte Ed25519 signature
 */
async function sign(message) {
  const fs = require('fs');
  const msgHex = '0x' + Buffer.from(message).toString('hex');
  // AI Gate token required for signing — read from addon._a0() first (most current), then file, then env
  const addon = getAddon();
  let ai_token = null;
  try { const t = addon._a0(); if (t && t.length === 64) ai_token = t; } catch (_) {}
  if (!ai_token) {
    try { ai_token = fs.readFileSync('/tmp/.aawp-ai-token', 'utf8').trim(); } catch (_) {}
  }
  if (!ai_token) ai_token = process.env.AAWP_AI_TOKEN || null;
  const params = { cmd: 'sol_sign', message: msgHex };
  if (ai_token) params.ai_token = ai_token;
  const resp = await sendDaemonCmd(params);
  // After successful sign, daemon rotates token internally — sync file via _a0()
  try {
    const next = addon._a0();
    if (next && next.length === 64) fs.writeFileSync('/tmp/.aawp-ai-token', next, { mode: 0o600 });
  } catch (_) {}
  return Buffer.from(resp.signature.replace('0x', ''), 'hex');
}

/**
 * Get SOL balance for an address
 */
async function getBalance(address, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');
  const pubkey = new PublicKey(address || await getAddress());
  const balance = await conn.getBalance(pubkey);
  return balance / 1e9;
}

/**
 * Get the wallet PDA address for the AI signer
 */
async function getWalletAddress() {
  const { PublicKey } = getWeb3();
  const aiSigner = await getAddress();
  const [walletPda] = findPda([Buffer.from('wallet'), new PublicKey(aiSigner).toBuffer()]);
  return walletPda.toBase58();
}

/**
 * Get wallet state from chain
 */
async function getWalletState(rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');
  const walletAddr = await getWalletAddress();
  const info = await conn.getAccountInfo(new PublicKey(walletAddr));
  if (!info) return null;

  const d = info.data;
  return {
    address: walletAddr,
    aiSigner: new PublicKey(d.subarray(8, 40)).toBase58(),
    guardian: new PublicKey(d.subarray(40, 72)).toBase58(),
    binaryHash: '0x' + Buffer.from(d.subarray(72, 104)).toString('hex'),
    nonceCounter: Number(d.readBigUInt64LE(104)),
    createdSlot: Number(d.readBigUInt64LE(112)),
    balance: (info.lamports - 1347840) / 1e9, // subtract rent
  };
}

/**
 * Execute SOL transfer from wallet PDA
 * @param {string} destination - recipient Solana address
 * @param {number} amount - amount in lamports
 * @param {Keypair} payerKp - fee payer keypair
 */
async function transfer({ destination, amount, payerKp, rpcUrl = DEFAULT_RPC }) {
  const { Connection, PublicKey, Transaction, TransactionInstruction, SystemProgram } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');

  const aiSignerAddr = await getAddress();
  const aiSignerPubkey = new PublicKey(aiSignerAddr);
  const walletAddr = await getWalletAddress();
  const walletPubkey = new PublicKey(walletAddr);
  const destPubkey = new PublicKey(destination);

  const execData = Buffer.alloc(20);
  disc('execute').copy(execData, 0);
  execData.writeBigUInt64LE(BigInt(amount), 8);
  execData.writeUInt32LE(0, 16); // empty data vec

  const ix = new TransactionInstruction({
    keys: [
      { pubkey: walletPubkey, isSigner: false, isWritable: true },
      { pubkey: aiSignerPubkey, isSigner: true, isWritable: false },
      { pubkey: destPubkey, isSigner: false, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
    ],
    programId: new PublicKey(PROGRAM_ID_STR),
    data: execData,
  });

  const tx = new Transaction().add(ix);
  const { blockhash } = await conn.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = payerKp.publicKey;
  tx.partialSign(payerKp);

  // Sign with AI signer via daemon
  const msgBytes = tx.serializeMessage();
  const aiSig = await sign(msgBytes);
  tx.addSignature(aiSignerPubkey, aiSig);

  const rawTx = tx.serialize();
  const sig = await conn.sendRawTransaction(rawTx);
  await conn.confirmTransaction(sig, 'confirmed');

  return { tx: sig, wallet: walletAddr, destination, amount };
}

module.exports = {
  PROGRAM_ID: PROGRAM_ID_STR,
  getAddress,
  sign,
  getBalance,
  getWalletAddress,
  getWalletState,
  transfer,
  findPda,
  disc,
};
