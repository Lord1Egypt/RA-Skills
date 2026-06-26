# Alby Lightning Payments for OpenClaw

Send and receive Bitcoin Lightning payments from your OpenClaw agent using [Alby Hub](https://albyhub.com)'s Nostr Wallet Connect (NWC) protocol.

## What this skill does

This skill provides two scripts:

- **`send_sats.mjs`** — Sends sats to any Lightning address (e.g. `user@walletofsatoshi.com`)
- **`pay_bolt11.mjs`** — Pays a bolt11 invoice directly

Both scripts connect to your own self-hosted or cloud Alby Hub via NWC — **no third-party custodian, no API key for a payment processor**.

## Network access — why and what

This skill makes outbound HTTPS requests to **two types of external domains**, both required by open Lightning standards:

### 1. LNURL resolution (Lightning address → invoice)
When you send to a Lightning address like `user@domain.com`, the script fetches:
```
https://domain.com/.well-known/lnurlp/user
```
This is the standard [LNURL-pay](https://github.com/lnurl/luds/blob/legacy/lnurl-pay.md) protocol (LUD-06/LUD-16), used universally across Lightning wallets. The domain is always the **recipient's own domain** — not a central server.

### 2. Invoice fetch (callback URL)
The LNURL metadata returns a callback URL (on the same domain) to request a payment invoice. The script fetches this to get the bolt11 string before paying.

### 3. NWC connection (your own wallet)
The NWC connection goes to **your own Alby Hub** (self-hosted or albyhub.com). No payment data passes through any third party.

### Security measures implemented
- Callback URLs are validated: HTTPS only, domain must match the Lightning address domain, private/internal IPs blocked (SSRF protection), no redirects
- Invoice amount is decoded and verified before payment (prevents overpayment by malicious servers)
- Input validation on all CLI arguments (format, length, type)
- Timeouts on all network requests (10s fetch, 30s payment)
- No sensitive data logged (NWC URL, full invoice details)

## Setup

### Prerequisites
- [Alby Hub](https://albyhub.com) account (self-hosted or cloud)
- NWC connection URL from your Alby Hub

### Installation
```bash
mkdir -p ~/.openclaw/workspace/skills/alby-lightning
cd ~/.openclaw/workspace/skills/alby-lightning
npm install @getalby/sdk
```

### Configuration
Add to `openclaw.json`:
```json
{
  "env": {
    "ALBY_NWC_URL": "nostr+walletconnect://..."
  }
}
```

## ⚠️ Security

Your NWC URL contains your wallet's **private key**. Anyone with this URL can spend your funds.

- **NEVER** commit it to git or share it publicly
- **ALWAYS** set spending limits in Alby Hub before use
- Store it only in `openclaw.json` (not in code files)
- Rotate the NWC URL immediately if you suspect it was leaked

## Usage

### Send sats to a Lightning address
```bash
node send_sats.mjs user@domain.com 1000
```

### Pay a bolt11 invoice
```bash
node pay_bolt11.mjs lnbc...
```

## License

MIT — free to use, modify, and redistribute.
