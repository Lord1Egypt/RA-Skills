# Filehub Reference

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup & Prerequisites](#setup--prerequisites)
- [How File Storage Works](#how-file-storage-works)
- [Integration with dApps](#integration-with-dapps)
- [Common Mistakes](#common-mistakes)

---

## Overview

Filehub is Chromia's decentralized, scalable storage platform built on the relational blockchain. It enables dApps to store files (images, videos, documents) directly on-chain rather than relying on centralized servers, IPFS, or Arweave.

**Key properties:**
- Decentralized blob storage across multiple Filechains
- Payment in CHR tokens
- ICCF-based payment verification between Filehub and Filechains
- Integrated with CRC2 for NFT content storage
- Available on both Mainnet and Testnet

---

## Architecture

Filehub has a two-tier architecture:

### Filehub Blockchain (Central Index)

- Tracks files and metadata
- Manages references to data chunks distributed across Filechains
- Processes payments and allocates storage

### Filechains (Blob Storage)

- Store actual file data chunks
- Operate without knowledge of file metadata or chunk relationships
- Validate data integrity by hashing incoming data against expected hashes
- Accept transactions only after ICCF-verified payment confirmation

### Communication Flow

1. User uploads file to Filehub
2. Filehub allocates storage on a suitable Filechain
3. Filehub processes CHR payment
4. Filehub generates **ICCF proof** of payment
5. Filechain validates the ICCF proof
6. Filechain stores the data chunks

---

## Setup & Prerequisites

### Funding Your Filehub Account

1. **Mainnet**: Requires CHR on the Economy Chain
   - Minimum deposit: 1 CHR to create an account
   - If CHR is on an EVM chain, use Vault Transfer to bridge to Economy Chain
   - Transfer CHR from Economy Chain to Filehub Chain via Vault UI
2. **Testnet**: Request testnet CHR from the Chromia Faucet
   - Testnet files are NOT guaranteed permanent storage

### Accessing Filehub

- **Mainnet UI**: Available via Chromia Vault
- **Testnet UI**: Same interface, uses testnet CHR
- **Programmatic**: Via Filehub client libraries

---

## How File Storage Works

### Upload Process

1. File is chunked into manageable pieces
2. Each chunk is hashed for integrity verification
3. Chunks are distributed across one or more Filechains
4. Filehub records the file metadata and chunk-to-Filechain mapping
5. Payment is deducted from user's Filehub balance

### Retrieval Process

1. Query Filehub for file metadata and chunk locations
2. Retrieve chunks from respective Filechains
3. Reassemble the file from chunks

---

## Integration with dApps

### CRC2 NFTs + Filehub

CRC2 NFTs can store content directly via Filehub:

```rell
// When minting an NFT, store content reference
// The actual file upload happens via Filehub client
// The on-chain record links the NFT to its Filehub content
```

This makes NFTs self-contained — no external content hosting dependency.

### Use Cases

- **NFT media storage**: Images, animations, audio for CRC2 tokens
- **Game assets**: 3D models, textures, level data
- **Document storage**: Certificates, legal documents
- **AI data**: Training datasets, model weights (via AI extensions)

---

## Common Mistakes

1. **Insufficient CHR balance**: File uploads fail silently if Filehub account has insufficient CHR. Always check balance before upload.
2. **Using testnet for permanent storage**: Testnet files may be wiped. Only mainnet provides persistent storage.
3. **Not accounting for chunk distribution**: Large files are split across Filechains. Retrieval requires querying the Filehub index first.
4. **Forgetting ICCF dependency**: Filehub-to-Filechain communication uses ICCF proofs. If ICCF is misconfigured, storage allocation fails.
