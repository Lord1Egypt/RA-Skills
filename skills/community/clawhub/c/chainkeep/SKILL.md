---
name: chainkeep
description: Store a file permanently onchain with ChainKeep and read it back, encrypted by default. Pay over x402 in USDC (signatures only, no gas) or in the chain's native coin. Use when the user asks to back up, archive or permanently keep a file or an agent's memory.
metadata:
  openclaw:
    requires:
      env: [CHAINKEEP_PRIVATE_KEY, CHAINKEEP_URL]
      bins: [node]
    primaryEnv: CHAINKEEP_PRIVATE_KEY
    envVars:
      - name: CHAINKEEP_PRIVATE_KEY
        required: true
        description: A dedicated agent wallet's private key, holding only what it needs. Never a user's main wallet.
      - name: CHAINKEEP_URL
        required: true
        description: The ChainKeep server, e.g. https://chainkeep.online
    install:
      - kind: node
        package: chainkeep
        bins: [chainkeep]
    emoji: '🔒'
    homepage: https://chainkeep.online/docs
---

# ChainKeep for agents

ChainKeep writes files to a blockchain for good: the bytes live in the chain's history, are
checked against an onchain Merkle root and SHA-256 when read back, and are paid for once, with no
renewals. The base URL (below, `$URL`) is `$CHAINKEEP_URL` when set; otherwise the site this file
was served from, or `https://chainkeep.online` if it was installed from a skill registry.

## Rules

- **Get approval before paying.** Show the user the price (`quote`, or the 402 response) and wait
  for an explicit yes. Never pay more than they approved.
- **Encrypt by default.** Store unencrypted only when the user says the file should be public.
  Public files are readable by anyone, forever, and their name and type are public metadata.
- **The recovery key is shown once.** Give it to the user to keep in their password manager.
  Never log it, put it in memory, or write it to a plain-text file. Without it an encrypted file
  can never be opened, and nobody can recover it.
- **Use a dedicated wallet** for the agent, holding only what it needs. Never ask a user for
  their private key.
- **Nothing can be deleted.** Do not store anything the user may want removed later.

## The quickest way: the CLI

```sh
export CHAINKEEP_URL=$URL
export CHAINKEEP_PRIVATE_KEY=0x…   # the agent's own wallet
npx -y chainkeep quote notes.md                  # price; pays nothing
npx -y chainkeep store notes.md --max-usdc 0.50  # pays only if the price is at most 0.50 USDC
npx -y chainkeep get 42 0x<fileId> --key <recovery key> --out notes.md
npx -y chainkeep list                            # this wallet's files
```

`store` refuses to pay without `--yes` or `--max-usdc`: it prints the price and exits with code 2
so you can ask the user first. Output is JSON on stdout; the result carries `fileId`, `chainId`,
`url` and, for encrypted files, `key`. `--public` stores unencrypted; `--pay native` pays in the
storage chain's coin instead of USDC; `--key-out key.json` also writes the key to a file (mode 600) when the user wants that. `--chain` picks the storage network (`chainkeep networks`).

## Paying over x402 (USDC, no gas)

Two signatures from the agent wallet, no transaction: an EIP-3009 USDC authorization pays, and an
EIP-712 `CreateFile` request makes the wallet the file's owner. The wallet needs USDC on the
payment network (Base) and nothing else.

1. **Prepare the bytes.** For a private file, encrypt them (format below). Then compute `size`,
   `contentHash = sha256(bytes)` and the Merkle root (below).
2. **Get the price.** `POST $URL/api/v1/x402/files?chainId=42&size=<bytes>` with no body answers
   `402` with `{ x402Version: 1, accepts: [requirement] }`. In the requirement:
   `maxAmountRequired` (atomic USDC, 6 decimals), `payTo`, `asset` (USDC), `network`,
   `maxTimeoutSeconds`, and `extra`: `name`, `version`, `chainId` (USDC's EIP-712 domain) and
   `storage: { chainId, vault, uploader, size }`. Show the price; wait for approval.
3. **Sign the file request** (EIP-712), domain
   `{ name: "ByteVault", version: "1", chainId: storage.chainId, verifyingContract: storage.vault }`:
   ```
   CreateFile(address owner, bytes32 nonce, uint64 size, bytes32 merkleRoot, bytes32 contentHash,
              bytes32 manifestHash, bool encrypted, address uploader, string metadata, uint256 deadline)
   ```
   `owner` is your address, `nonce` 32 random bytes, `uploader` is `storage.uploader`,
   `manifestHash` zero, `metadata` empty for encrypted files (or `{"name","type"}` JSON for public
   ones, at most 512 bytes), `deadline` a unix time at least an hour away (use a day).
4. **Sign the payment** (x402 "exact"): an EIP-3009 `TransferWithAuthorization(address from,
address to, uint256 value, uint256 validAfter, uint256 validBefore, bytes32 nonce)` with
   `to = payTo`, `value = maxAmountRequired`, a window covering now, and a random nonce, in the
   USDC domain from `extra`. The `X-PAYMENT` header is base64 of
   `{ "x402Version": 1, "scheme": "exact", "network": "base", "payload": { "signature", "authorization" } }`.
5. **Send.** `POST $URL/api/v1/x402/files?chainId=…&owner=…&nonce=…&deadline=…&signature=…&encrypted=true|false[&metadata=…]`
   with the `X-PAYMENT` header and the exact stored bytes as the body
   (`application/octet-stream`, at most 128 MB). `202` returns the job (`fileId`, `state`), and
   the `X-PAYMENT-RESPONSE` header carries the settlement transaction.
6. **Follow it.** `GET $URL/api/v1/uploads/<chainId>/<fileId>` until `state` is `done`. The file is
   at `$URL/file/<chainId>/<fileId>`.

The server checks everything before money moves: the bytes must reproduce your signed root, the
vault must accept the request, and USDC must accept the authorization. A refusal is a 4xx with
an `error` message and nothing charged. Sending the same file again returns its job, unpaid.

## Paying in the native coin

The browser's path: `POST $URL/api/v1/uploads/quote` with `{ chainId, size }` returns `amount`,
`relayer` and a `token`. Call the vault's
`createFile(bytes32 nonce, uint64 size, bytes32 merkleRoot, bytes32 contentHash, bytes32 manifestHash, bool encrypted, address uploader, string metadata)`
from your wallet with `uploader = relayer` and `value = amount`, then
`POST $URL/api/v1/uploads?chainId=…&fileId=…&tx=<hash>` with header `x-bytevault-quote: <token>`
and the bytes as the body. The file ID is `computeFileId(owner, nonce)` on the vault.

## Formats

- **Chunks:** 122,880 bytes (120 KiB); the last one is shorter.
- **Merkle root:** leaf `i` is `sha256(uint256(i) as 32 bytes ‖ sha256(chunk_i))`; each parent is
  `sha256` of its two children sorted ascending as bytes32, an odd node paired with itself.
- **Encryption** (AES-256-GCM, Web Crypto): the envelope is `"BVE" 0x02 ‖ 12-byte IV ‖ ciphertext`,
  with the 4 magic bytes as additional authenticated data. The plaintext is
  `uint32 header length ‖ header JSON {"name","type"} ‖ file bytes`. The recovery key is the
  32-byte AES key in base64.

## Reading back

`npx -y chainkeep get <chainId> <fileId> [--key …]`, or by hand: the vault's
`getChunkBlocks(fileId, start, count)` gives each chunk's block; `eth_getLogs` on those blocks
for `ChunkData(bytes32 indexed fileId, uint32 indexed index, bytes data)` gives the bytes. Check
them against `getFile(fileId)` (`merkleRoot`, `contentHash`, `size`) before trusting them, then
decrypt. Public files are also served at `$URL/raw/<chainId>/<fileId>`.
