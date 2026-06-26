# ClawPurse Operator Guide

Complete guide for operators running ClawPurse—whether you're integrating with agentic AI (including OpenClaw), automation scripts, or using it as an individual.

## Prerequisites

- Node.js 18+ installed
- Network access to Neutaro RPC (`https://rpc2.neutaro.io`)
- Terminal access for CLI commands

---

## Installation

```bash
# Clone or navigate to ClawPurse directory
cd ClawPurse

# Install dependencies
npm install

# Build TypeScript
npm run build

# Link globally (makes 'clawpurse' available everywhere)
npm link
```

---

## Initial Wallet Setup

### Create a New Wallet

```bash
clawpurse init --password <strong-password>
```

This will:
1. Generate a new 24-word mnemonic
2. Create an encrypted keystore at `~/.clawpurse/keystore.enc`
3. Run the guardrail wizard (choose enforce or allow mode)
4. Display your wallet address and mnemonic

> ⚠️ **CRITICAL**: Back up the mnemonic immediately! It's only shown once.

**Example output:**
```
Generating new wallet...
Encrypting and saving keystore...

╔══════════════════════════════════════════════════════════════════╗
║                    WALLET CREATED SUCCESSFULLY                   ║
╠══════════════════════════════════════════════════════════════════╣
║ Address: neutaro1fnpesef2y2lzt48xvtqeh4dts6ztdeuq86vgt3          ║
║ Keystore: /home/user/.clawpurse/keystore.enc                     ║
╠══════════════════════════════════════════════════════════════════╣
║ ⚠️  BACKUP YOUR MNEMONIC - THIS IS THE ONLY TIME IT'S SHOWN ⚠️   ║
╠══════════════════════════════════════════════════════════════════╣
║  1. word1        2. word2        3. word3        4. word4        ║
║  5. word5        6. word6        7. word7        8. word8        ║
...
╚══════════════════════════════════════════════════════════════════╝
```

### Import an Existing Wallet

```bash
clawpurse import --mnemonic "word1 word2 ... word24" --password <password>
```

Or use environment variable:
```bash
export CLAWPURSE_MNEMONIC="word1 word2 ... word24"
clawpurse import --password <password>
```

---

## Daily Operations

### Check Chain Status

```bash
clawpurse status
```

Verifies connection to the Neutaro network:
```
╔══════════════════════════════════════════════════════════════════╗
║                      CHAIN STATUS                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Status: 🟢 CONNECTED                                             ║
║ Chain ID: Neutaro-1                                              ║
║ Block Height: 13837090                                           ║
║ RPC: https://rpc2.neutaro.io                                     ║
╚══════════════════════════════════════════════════════════════════╝
```

### View Your Address

```bash
clawpurse address
# Output: neutaro1fnpesef2y2lzt48xvtqeh4dts6ztdeuq86vgt3
```

### Check Balance

```bash
clawpurse balance --password <password>
```

Or with environment variable:
```bash
export CLAWPURSE_PASSWORD=<password>
clawpurse balance
```

### Get Receive Address

```bash
clawpurse receive
```

Shows your address and QR data for receiving NTMPI.

### Send Tokens

```bash
clawpurse send <recipient-address> <amount> --password <password>
```

**Options:**
| Flag | Description |
|------|-------------|
| `--memo "text"` | Add memo to transaction |
| `--yes` | Skip confirmation for amounts > 100 NTMPI |
| `--override-allowlist` | Bypass allowlist restrictions |

**Examples:**
```bash
# Simple send
clawpurse send neutaro1abc... 10.5 --password mypass

# With memo
clawpurse send neutaro1abc... 10.5 --memo "payment for service" --password mypass

# Large amount (skip confirmation)
clawpurse send neutaro1abc... 500 --yes --password mypass
```

### View Transaction History

```bash
clawpurse history
# Or limit results
clawpurse history --limit 5
```

### Export Mnemonic (⚠️ Dangerous)

```bash
clawpurse export --yes --password <password>
```

Only use this if you need to back up or migrate the wallet.

---

## Allowlist Management

The allowlist controls which addresses can receive funds from your wallet.

### Run Guardrail Wizard

```bash
clawpurse allowlist init
# Or pre-set mode
clawpurse allowlist init --mode enforce
```

### View Allowlist

```bash
clawpurse allowlist list
```

### Add Trusted Destination

```bash
clawpurse allowlist add neutaro1xyz... --name "Partner" --max 500
```

### Remove Destination

```bash
clawpurse allowlist remove neutaro1xyz...
```

See [ALLOWLIST.md](./ALLOWLIST.md) for complete documentation.

---

## Safety Rails

ClawPurse includes built-in limits to prevent costly mistakes:

| Setting | Default | Purpose |
|---------|---------|---------|
| `maxSendAmount` | 1000 NTMPI | Hard cap per transaction |
| `requireConfirmAbove` | 100 NTMPI | Requires `--yes` flag |
| Allowlist mode | Choose during init | Enforce or allow unknown destinations |

### Adjusting Limits

Edit `src/config.ts` and rebuild:

```typescript
export const KEYSTORE_CONFIG = {
  maxSendAmount: 5000_000000,      // 5000 NTMPI (micro-units)
  requireConfirmAbove: 500_000000, // 500 NTMPI
  // ...
};
```

Then:
```bash
npm run build
npm link
```

---

## Transaction Receipts

Every send creates a receipt in `~/.clawpurse/receipts.json`:

```json
{
  "id": "send-79EC3BC1-1770478262438",
  "type": "send",
  "txHash": "79EC3BC17965A0987F4B7462C40B5FAC0889C5D3F9DD63C72B59571987E40F7D",
  "fromAddress": "neutaro1fnpesef2y2lzt48xvtqeh4dts6ztdeuq86vgt3",
  "toAddress": "neutaro16us2fdzl8vf2lvn5tqsswajkqtelfpspxj9hvx",
  "amount": "400000",
  "displayAmount": "0.400000 NTMPI",
  "denom": "uneutaro",
  "memo": "test tx",
  "height": 13835843,
  "gasUsed": 87567,
  "timestamp": "2026-02-07T15:31:02.434Z",
  "status": "confirmed"
}
```

**Back up this file** for your audit trail.

---

## Verifying Transactions

### As the Sender

After sending, share the receipt or tx hash with the recipient.

### As the Recipient

Verify on-chain:
```bash
curl "https://api2.neutaro.io/cosmos/tx/v1beta1/txs/<TX_HASH>"
```

Confirm:
- `from_address` matches expected sender
- `to_address` is your address
- `amount` and `denom` are correct
- Transaction is in a confirmed block

See [TRUST-MODEL.md](./TRUST-MODEL.md) for detailed verification procedures.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAWPURSE_PASSWORD` | Wallet password (avoids `--password` flag) |
| `CLAWPURSE_MNEMONIC` | Mnemonic for import (avoids `--mnemonic` flag) |

**Example session:**
```bash
export CLAWPURSE_PASSWORD=mysecretpassword
clawpurse balance
clawpurse send neutaro1... 10.0 --memo "payment"
clawpurse history
```

---

## Security Checklist

### Initial Setup
- [ ] Used strong password (12+ characters)
- [ ] Backed up mnemonic offline immediately
- [ ] Verified keystore permissions: `ls -la ~/.clawpurse/keystore.enc` shows `-rw-------`

### Ongoing
- [ ] Safety limits configured appropriately
- [ ] Allowlist in enforce mode with trusted addresses only
- [ ] Receipts backed up periodically
- [ ] Password not stored in scripts or shell history

### Host Security
- [ ] Machine is secured (firewall, updates)
- [ ] Limited user access to keystore
- [ ] No malware or keyloggers

---

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| `Status: 🔴 DISCONNECTED` | Network or RPC issue | Check internet; try different RPC in config |
| "Amount exceeds safety limit" | `maxSendAmount` too low | Adjust in `src/config.ts` and rebuild |
| "Invalid address prefix" | Wrong address format | Neutaro addresses start with `neutaro1` |
| "Password incorrect" | Wrong password | Double-check; re-import from mnemonic if forgotten |
| "Destination not in allowlist" | Allowlist enforcement | Add address or use `--override-allowlist` |
| `ENOENT: no such file` | Missing keystore | Run `clawpurse init` or `import` |

### Reset Everything

If you need to start fresh:
```bash
# Remove all ClawPurse data (DESTRUCTIVE!)
rm -rf ~/.clawpurse

# Reinitialize
clawpurse init --password <new-password>
```

> ⚠️ Only do this if you have your mnemonic backed up or don't need the existing wallet.

---

## Command Reference

| Command | Description |
|---------|-------------|
| `clawpurse init` | Create new wallet |
| `clawpurse import` | Import from mnemonic |
| `clawpurse status` | Check chain connection |
| `clawpurse address` | Show wallet address |
| `clawpurse balance` | Check balance |
| `clawpurse receive` | Show receive info |
| `clawpurse send <to> <amt>` | Send tokens |
| `clawpurse history` | View transactions |
| `clawpurse export --yes` | Export mnemonic |
| `clawpurse allowlist init` | Setup allowlist |
| `clawpurse allowlist list` | View allowlist |
| `clawpurse allowlist add` | Add destination |
| `clawpurse allowlist remove` | Remove destination |

---

## Support

- **Neutaro chain docs**: https://docs.neutaro.io
- **Block explorer**: https://explorer.neutaro.io
- **RPC endpoints**: `https://rpc2.neutaro.io`, `https://api2.neutaro.io`
