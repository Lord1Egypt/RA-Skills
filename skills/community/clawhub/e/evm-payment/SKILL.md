---
name: eth-payment
version: 1.0.4
description: Generate EIP-681 Ethereum payment links and QR codes for any EVM chain. Zero configuration, instant setup for receiving ETH and ERC-20 payments. Use when you need to create payment requests, invoices, donation links, or any on-chain payment request. Supports Base, Ethereum, Arbitrum, Optimism, Polygon.
author: Antalpha AI Team
metadata:
  requires:
    - python3
    - pip
  pip:
    - qrcode
    - pillow
  install:
    type: instruction-only
---

# ETH Payment Skill

> **Zero config. Instant setup. Works on any EVM chain.**

## What This Does

Generate EIP-681 compliant payment links that work with MetaMask and other Ethereum wallets. Perfect for:

- Payment requests and invoices
- Donation links
- Mobile-friendly checkout
- Any on-chain payment collection

**No API keys. No servers. No configuration.**

## Installation

### Prerequisites

- **Python 3.8+** - Required to run the script
- **pip packages**: `qrcode`, `pillow` - For QR code generation

### Quick Install

Install the required packages:

```bash
pip install qrcode pillow
```

### Run the Skill

```bash
python3 scripts/eth_payment.py create --to 0xYourAddress --amount 0.1
```

---

## Quick Start

```bash
# Basic ETH payment on Base
eth-payment create --to 0xYourAddress --amount 0.1

# USDC payment with QR code
eth-payment create --to 0xYourAddress --amount 100 --token USDC --qr payment.png

# Specify network
eth-payment create --to 0xYourAddress --amount 10 --token USDC --network ethereum --qr qr.png
```

## Commands

### `create` - Generate Payment Link

```bash
eth-payment create --to <address> --amount <number> [options]

Required:
  --to <address>      Recipient address (0x...)
  --amount <number>   Amount to request

Options:
  --token <symbol>    Token symbol (default: ETH)
  --network <name>    Network: base, ethereum, arbitrum, optimism, polygon (default: base)
  --qr <path>         Generate QR code and save to path
  --json              Output as JSON for programmatic use
```

### `chains` - List Supported Networks

```bash
eth-payment chains
eth-payment chains --json
```

### `tokens` - List Tokens for Network

```bash
eth-payment tokens --network base
eth-payment tokens --network ethereum --json
```

### `validate` - Validate Address

```bash
eth-payment validate 0x...
```

## Supported Networks

| Network | Chain ID | Native Token | ERC-20 Tokens |
|---------|----------|--------------|---------------|
| base | 8453 | ETH | USDC, USDT, WETH |
| ethereum | 1 | ETH | USDC, USDT, WETH, DAI |
| arbitrum | 42161 | ETH | USDC, USDT, ARB |
| optimism | 10 | ETH | USDC, OP |
| polygon | 137 | MATIC | USDC, USDT, WETH |

## Examples

### Invoice with QR Code

```bash
eth-payment create \
  --to 0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e \
  --amount 100 \
  --token USDC \
  --network base \
  --qr invoice_qr.png
```

### JSON Output for Integration

```bash
eth-payment create --to 0x... --amount 10 --token USDC --json
```

Output:
```json
{
  "success": true,
  "network": "base",
  "chain_id": 8453,
  "token": "USDC",
  "recipient": "0x...",
  "amount": "10",
  "links": {
    "eip681": "ethereum:0x833...@8453/transfer?address=0x...&uint256=10000000",
    "metamask": "https://metamask.app.link/send/..."
  },
  "transaction": {
    "to": "0x833...",
    "value": "0x0",
    "data": "0xa9059cbb..."
  }
}
```

## How It Works

1. **EIP-681 Standard**: Uses the Ethereum Improvement Proposal 681 format for payment links
2. **Universal**: Same code works on any EVM chain - only configuration differs
3. **QR Codes**: Generated locally via Python qrcode library, no external services

## Security Notes

- This skill only **generates** payment links, it cannot execute transactions
- No private keys or secrets required
- All processing happens locally
- Always verify the recipient address before sharing payment links

## Adding New Chains

To add a new EVM chain, edit `config/chains.json`:

```json
{
  "chains": {
    "new-chain": {
      "name": "New Chain",
      "chain_id": 12345,
      "native_token": "NATIVE",
      "tokens": {
        "NATIVE": {
          "address": "0x0000000000000000000000000000000000000000",
          "decimals": 18,
          "is_native": true
        },
        "USDC": {
          "address": "0x...",
          "decimals": 6
        }
      }
    }
  }
}
```

---

**Maintainer**: Antalpha AI Team
**License**: MIT