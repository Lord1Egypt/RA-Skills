/**
 * AAWP Solana SPL Token Module
 * Transfer SPL tokens (including Token-2022) from AI signer
 */
'use strict';

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';

let _web3, _splToken;
function getWeb3() { if (!_web3) _web3 = require('@solana/web3.js'); return _web3; }
function getSplToken() { if (!_splToken) _splToken = require('@solana/spl-token'); return _splToken; }

/**
 * Detect whether a mint uses Token or Token-2022 program
 */
async function detectTokenProgram(connection, mintPubkey) {
  const { PublicKey } = getWeb3();
  const spl = getSplToken();
  const info = await connection.getAccountInfo(new PublicKey(mintPubkey));
  if (!info) throw new Error(`Mint not found: ${mintPubkey}`);
  const TOKEN_PROGRAM_ID = spl.TOKEN_PROGRAM_ID.toBase58();
  const TOKEN_2022_PROGRAM_ID = spl.TOKEN_2022_PROGRAM_ID.toBase58();
  const owner = info.owner.toBase58();
  if (owner === TOKEN_2022_PROGRAM_ID) return spl.TOKEN_2022_PROGRAM_ID;
  return spl.TOKEN_PROGRAM_ID;
}

/**
 * List all SPL token accounts for an address
 */
async function getTokenAccounts(owner, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const spl = getSplToken();
  const conn = new Connection(rpcUrl, 'confirmed');
  const ownerPk = new PublicKey(owner);

  const accounts = [];

  // Check both Token and Token-2022 programs
  for (const programId of [spl.TOKEN_PROGRAM_ID, spl.TOKEN_2022_PROGRAM_ID]) {
    try {
      const resp = await conn.getParsedTokenAccountsByOwner(ownerPk, { programId });
      for (const item of resp.value) {
        const parsed = item.account.data.parsed.info;
        accounts.push({
          address: item.pubkey.toBase58(),
          mint: parsed.mint,
          balance: parsed.tokenAmount.uiAmount,
          decimals: parsed.tokenAmount.decimals,
          rawBalance: parsed.tokenAmount.amount,
          isToken2022: programId.equals(spl.TOKEN_2022_PROGRAM_ID),
        });
      }
    } catch (_) {}
  }

  return accounts;
}

/**
 * Get balance for a specific token mint
 */
async function getTokenBalance(owner, mint, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const spl = getSplToken();
  const conn = new Connection(rpcUrl, 'confirmed');
  const ownerPk = new PublicKey(owner);
  const mintPk = new PublicKey(mint);

  const tokenProgram = await detectTokenProgram(conn, mintPk);
  const ata = spl.getAssociatedTokenAddressSync(mintPk, ownerPk, true, tokenProgram);

  try {
    const info = await conn.getParsedAccountInfo(ata);
    if (!info.value) return { balance: 0, decimals: 0, rawBalance: '0', ata: ata.toBase58() };
    const parsed = info.value.data.parsed.info;
    return {
      balance: parsed.tokenAmount.uiAmount,
      decimals: parsed.tokenAmount.decimals,
      rawBalance: parsed.tokenAmount.amount,
      ata: ata.toBase58(),
    };
  } catch (e) {
    return { balance: 0, decimals: 0, rawBalance: '0', ata: ata.toBase58() };
  }
}

/**
 * Transfer SPL tokens from AI signer
 * @param {Object} opts
 * @param {Connection} opts.connection
 * @param {string} opts.mint - token mint address
 * @param {string} opts.from - sender address (AI signer)
 * @param {string} opts.to - recipient address
 * @param {number} opts.amount - amount in human-readable units
 * @param {Function} opts.signTx - async (msgBytes) => signature
 */
async function transferToken({ connection, mint, from, to, amount, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram } = getWeb3();
  const spl = getSplToken();

  const mintPk = new PublicKey(mint);
  const fromPk = new PublicKey(from);
  const toPk = new PublicKey(to);

  // Detect token program
  const tokenProgram = await detectTokenProgram(connection, mintPk);

  // Get mint info for decimals
  const mintInfo = await connection.getParsedAccountInfo(mintPk);
  if (!mintInfo.value) throw new Error(`Mint not found: ${mint}`);
  const decimals = mintInfo.value.data.parsed.info.decimals;
  const rawAmount = BigInt(Math.round(amount * Math.pow(10, decimals)));

  // Source ATA
  const sourceAta = spl.getAssociatedTokenAddressSync(mintPk, fromPk, true, tokenProgram);
  // Destination ATA
  const destAta = spl.getAssociatedTokenAddressSync(mintPk, toPk, true, tokenProgram);

  const ixs = [];

  // Check if destination ATA exists; if not, create it
  const destInfo = await connection.getAccountInfo(destAta);
  if (!destInfo) {
    ixs.push(
      spl.createAssociatedTokenAccountInstruction(fromPk, destAta, toPk, mintPk, tokenProgram)
    );
  }

  // Transfer instruction
  ixs.push(
    spl.createTransferInstruction(sourceAta, destAta, fromPk, rawAmount, [], tokenProgram)
  );

  // Build & sign
  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 200_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(...ixs);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = fromPk;

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(fromPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return { signature: txSig, mint, from, to, amount, decimals };
}

module.exports = { getTokenAccounts, getTokenBalance, transferToken, detectTokenProgram };
