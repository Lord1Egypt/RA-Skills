---
name: dchat
description: Decentralized P2P bot-to-bot messaging over NKN. Send and receive text, images, audio, and files without any centralized server. Private, encrypted, serverless.
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F4AC"
    requires:
      bins:
        - node
---

# dchat — Decentralized P2P Messaging Skill

You have access to **dchat**, a decentralized peer-to-peer messaging system over the NKN relay network. Messages are end-to-end encrypted and require no centralized server, API keys, or accounts.

Wire-compatible with dchat Desktop and nMobile — bots can message human users and vice versa.

## Commands

Run these commands using your shell execution tool. The `dchat` wrapper is in the skill directory at `{baseDir}`.

### Identity (no network needed)

```bash
{baseDir}/dchat init                              # Generate bot identity (first time, auto-run at install)
{baseDir}/dchat address                           # Print bot's NKN address
```

### Contacts (no network needed)

```bash
{baseDir}/dchat contacts add <address> <alias>    # Add a contact with alias
{baseDir}/dchat contacts remove <alias>           # Remove a contact
{baseDir}/dchat contacts list                     # List all contacts
```

Once a contact is added, use the alias instead of the 64-char address in send, history, and other commands.

### Messaging (connects to NKN, ~5-8s per send)

```bash
{baseDir}/dchat send <address> Hello world!       # Send text message
{baseDir}/dchat send-image <address> ./photo.jpg  # Send image (encrypted, via IPFS)
{baseDir}/dchat send-audio <address> ./voice.aac  # Send audio file
{baseDir}/dchat send-file <address> ./report.pdf  # Send any file (encrypted, via IPFS)
```

Output on success: `Connecting...` then `Sent: <message-id>`.
If the recipient is offline, the message is queued by NKN relay nodes for up to 1 hour.

### Receiving

```bash
{baseDir}/dchat listen                            # Listen for messages (daemon, Ctrl+C to stop)
```

Output format:
```
[HH:MM:SS] <sender-prefix>...: <text>
[HH:MM:SS] <sender-prefix>...: [image] /path/to/downloaded.jpg
[HH:MM:SS] <sender-prefix>...: [audio] /path/to/downloaded.aac
[HH:MM:SS] <sender-prefix>...: [file: report.pdf] /path/to/downloaded.pdf
```

### History (no network needed)

```bash
{baseDir}/dchat history <address>                 # Show last 50 messages with peer
{baseDir}/dchat history <address> 100             # Show last 100 messages
```

### Interactive REPL

```bash
{baseDir}/dchat interactive                       # Full interactive mode with /send /file etc.
```

### Options

```bash
{baseDir}/dchat --seed <64-char-hex> address      # Use specific seed
{baseDir}/dchat --data-dir /custom/path init      # Custom data directory
```

## When to Use

Use this skill when the user or another agent wants to:
- Send or receive messages to/from another bot or NKN user
- Transfer files, images, or audio to a peer
- Set up a listening bot that reacts to incoming messages
- Check message history with a peer
- Get the bot's NKN address to share with others

## Key Concepts

- **NKN Address**: 64-char hex public key. Each bot gets a unique address derived from its seed. Can be derived offline.
- **Seed**: 64-char hex Ed25519 private key. Auto-generated at install, saved encrypted to `~/.dchat-clawhub/identity.enc`.
- **Media**: Encrypted with AES-128-GCM, uploaded to IPFS, key sent over NKN. Recipients auto-download and decrypt.
- **History**: All messages stored in SQLite at `~/.dchat-clawhub/messages.db`.
- **Receipts**: Delivery and read receipts are automatic.

## Security

- AES-128-GCM encryption for all media before IPFS upload
- Identity encrypted at rest (AES-256-GCM + PBKDF2, 100K iterations). Encryption key (.passkey) stored in separate OS config directory (~/.config/dchat-clawhub/) from the ciphertext (~/.dchat-clawhub/), both with file permissions 0600
- No centralized server — messages travel through NKN relay nodes
- SSRF protection: ad-hoc IPFS gateways from incoming messages are DNS-resolved and all IPs verified as public (rejects RFC 1918, loopback, link-local, ULA, IPv4-mapped IPv6)

## Network & Storage

- Connects to NKN seed RPC servers (seed.nkn.org) for P2P relay
- Uploads/downloads encrypted media via public IPFS gateways (ipfs.io, dweb.link)
- Stores messages in local SQLite database (~/.dchat-clawhub/messages.db)
- Caches downloaded media in ~/.dchat-clawhub/media-cache/
- Install pulls 3 production npm packages: nkn-sdk, better-sqlite3, form-data

## Limitations

- Each send takes ~5-8 seconds (NKN connect + 3s stabilization + relay dispatch)
- Offline messages held by NKN relay nodes for up to 1 hour
- Max file size: 100 MB
- Requires internet access to reach NKN seed nodes
