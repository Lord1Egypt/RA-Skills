# Alby Lightning Payments Skill

## Overview
Easily send, receive, and manage Bitcoin Lightning payments via Alby Hub's Nostr Wallet Connect (NWC).

## Features
- Check wallet balance
- Pay Lightning invoices
- Send to Lightning addresses
- Generate receive invoices

## Setup

### Prerequisites
- Alby Hub account
- NWC (Nostr Wallet Connect) URL

### Installation
```bash
mkdir -p ~/.openclaw/workspace/skills/alby-lightning
cd ~/.openclaw/workspace/skills/alby-lightning
npm init -y
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

## Gotchas
- Always specify amount for zero-amount invoices
- Use `result.invoice`, not `result.payment_request`
- Set spending limits in Alby Hub

## Contributing
Improvements welcome! Open issues at GitHub.
