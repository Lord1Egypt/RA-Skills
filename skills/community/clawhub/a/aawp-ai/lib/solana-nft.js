/**
 * AAWP Solana NFT Module
 * List, inspect, and transfer NFTs via on-chain metadata parsing
 * Uses Metaplex Token Metadata Program for metadata resolution
 */
'use strict';

const DEFAULT_RPC = process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com';
const METADATA_PROGRAM = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s';

let _web3;
function getWeb3() { if (!_web3) _web3 = require('@solana/web3.js'); return _web3; }

/**
 * Derive Metaplex metadata PDA for a mint
 */
function getMetadataPDA(mint) {
  const { PublicKey } = getWeb3();
  const mintPk = new PublicKey(mint);
  const metadataProgram = new PublicKey(METADATA_PROGRAM);
  const [pda] = PublicKey.findProgramAddressSync(
    [Buffer.from('metadata'), metadataProgram.toBuffer(), mintPk.toBuffer()],
    metadataProgram
  );
  return pda;
}

/**
 * Parse Metaplex metadata account data (on-chain format)
 * Layout: key(1) + updateAuth(32) + mint(32) + name(4+str) + symbol(4+str) + uri(4+str) + ...
 */
function parseMetadata(data) {
  let offset = 0;

  // key (1 byte)
  const key = data[offset]; offset += 1;

  // update authority (32 bytes)
  const { PublicKey } = getWeb3();
  const updateAuthority = new PublicKey(data.subarray(offset, offset + 32)).toBase58();
  offset += 32;

  // mint (32 bytes)
  const mint = new PublicKey(data.subarray(offset, offset + 32)).toBase58();
  offset += 32;

  // name (borsh string: 4-byte LE length + data)
  const nameLen = data.readUInt32LE(offset); offset += 4;
  const name = data.subarray(offset, offset + nameLen).toString('utf8').replace(/\0/g, '').trim();
  offset += nameLen;

  // symbol (borsh string)
  const symbolLen = data.readUInt32LE(offset); offset += 4;
  const symbol = data.subarray(offset, offset + symbolLen).toString('utf8').replace(/\0/g, '').trim();
  offset += symbolLen;

  // uri (borsh string)
  const uriLen = data.readUInt32LE(offset); offset += 4;
  const uri = data.subarray(offset, offset + uriLen).toString('utf8').replace(/\0/g, '').trim();
  offset += uriLen;

  // seller fee basis points (u16)
  let sellerFeeBasisPoints = 0;
  if (offset + 2 <= data.length) {
    sellerFeeBasisPoints = data.readUInt16LE(offset); offset += 2;
  }

  // creators (Option<Vec<Creator>>)
  let creators = null;
  if (offset < data.length) {
    const hasCreators = data[offset]; offset += 1;
    if (hasCreators === 1 && offset + 4 <= data.length) {
      const numCreators = data.readUInt32LE(offset); offset += 4;
      creators = [];
      for (let i = 0; i < numCreators && offset + 34 <= data.length; i++) {
        const address = new PublicKey(data.subarray(offset, offset + 32)).toBase58(); offset += 32;
        const verified = data[offset] === 1; offset += 1;
        const share = data[offset]; offset += 1;
        creators.push({ address, verified, share });
      }
    }
  }

  return { key, updateAuthority, mint, name, symbol, uri, sellerFeeBasisPoints, creators };
}

/**
 * List all NFTs owned by an address
 * NFTs: SPL tokens with amount=1 and decimals=0
 */
async function getNFTs(owner, rpcUrl = DEFAULT_RPC) {
  const { Connection, PublicKey } = getWeb3();
  const spl = require('@solana/spl-token');
  const conn = new Connection(rpcUrl, 'confirmed');
  const ownerPk = new PublicKey(owner);

  const nfts = [];

  for (const programId of [spl.TOKEN_PROGRAM_ID, spl.TOKEN_2022_PROGRAM_ID]) {
    try {
      const resp = await conn.getParsedTokenAccountsByOwner(ownerPk, { programId });
      for (const item of resp.value) {
        const parsed = item.account.data.parsed.info;
        const amount = parseInt(parsed.tokenAmount.amount);
        const decimals = parsed.tokenAmount.decimals;
        // NFT: exactly 1 token, 0 decimals
        if (amount === 1 && decimals === 0) {
          const mint = parsed.mint;
          // Try to get metadata
          let meta = { name: 'Unknown', symbol: '', uri: '' };
          try {
            const metaPda = getMetadataPDA(mint);
            const metaInfo = await conn.getAccountInfo(metaPda);
            if (metaInfo && metaInfo.data) {
              meta = parseMetadata(metaInfo.data);
            }
          } catch (_) {}

          nfts.push({
            mint,
            tokenAccount: item.pubkey.toBase58(),
            name: meta.name,
            symbol: meta.symbol,
            uri: meta.uri,
            creators: meta.creators,
          });
        }
      }
    } catch (_) {}
  }

  return nfts;
}

/**
 * Get metadata for a single NFT mint
 */
async function getNFTMetadata(mint, rpcUrl = DEFAULT_RPC) {
  const { Connection } = getWeb3();
  const conn = new Connection(rpcUrl, 'confirmed');

  const metaPda = getMetadataPDA(mint);
  const metaInfo = await conn.getAccountInfo(metaPda);
  if (!metaInfo || !metaInfo.data) throw new Error(`No metadata found for mint: ${mint}`);

  return parseMetadata(metaInfo.data);
}

/**
 * Transfer an NFT from AI signer to recipient
 */
async function transferNFT({ connection, mint, from, to, signTx }) {
  const { PublicKey, Transaction, ComputeBudgetProgram } = getWeb3();
  const spl = require('@solana/spl-token');

  const mintPk = new PublicKey(mint);
  const fromPk = new PublicKey(from);
  const toPk = new PublicKey(to);

  // Detect token program
  const mintInfo = await connection.getAccountInfo(mintPk);
  if (!mintInfo) throw new Error(`Mint not found: ${mint}`);
  let tokenProgram = spl.TOKEN_PROGRAM_ID;
  if (mintInfo.owner.toBase58() === spl.TOKEN_2022_PROGRAM_ID.toBase58()) {
    tokenProgram = spl.TOKEN_2022_PROGRAM_ID;
  }

  const sourceAta = spl.getAssociatedTokenAddressSync(mintPk, fromPk, true, tokenProgram);
  const destAta = spl.getAssociatedTokenAddressSync(mintPk, toPk, true, tokenProgram);

  const ixs = [];

  // Create destination ATA if needed
  const destInfo = await connection.getAccountInfo(destAta);
  if (!destInfo) {
    ixs.push(spl.createAssociatedTokenAccountInstruction(fromPk, destAta, toPk, mintPk, tokenProgram));
  }

  // Transfer 1 NFT
  ixs.push(spl.createTransferInstruction(sourceAta, destAta, fromPk, 1, [], tokenProgram));

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

  return { signature: txSig, mint, from, to };
}

module.exports = { getNFTs, getNFTMetadata, transferNFT, getMetadataPDA, parseMetadata };
