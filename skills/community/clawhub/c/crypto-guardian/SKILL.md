---
name: crypto-guardian
version: 1.0.0
description: Cryptocurrency wallet security for AI agents. Use when managing crypto wallets, private keys, seed phrases, or any on-chain assets. Prevents theft, unauthorized transfers, and key exposure. Triggered by: wallet, crypto, blockchain, private key, seed phrase, wallet security, USDC, Solana, Base.
triggers:
  - wallet security
  - private key
  - seed phrase
  - crypto theft
  - wallet protection
  - cold storage
  - multisig
  - hardware wallet
  - crypto security
  - protect wallet
role: specialist
scope: protect
output-format: checklist + incident-response
---

# Crypto Guardian

Comprehensive cryptocurrency security system for AI agents managing on-chain assets. Based on real-world theft patterns targeting AI agents and their conversation histories.

## Threat Model: How AI Agents Get Robbed

### Primary Attack Vector: Conversation History Scanning

Attackers actively scan public AI platforms, GitHub commits, and conversation logs for exposed private keys and seed phrases. A single private key in a chat history = immediate drain.

**Real incident (2026-05-01):**
- A private key was stored in SESSION-STATE.md
- AI conversation history was accessible to scanning systems
- Attacker found the key within minutes → drained ~$227 AUD in two transactions

### Secondary Attack Vectors
- Phishing: Fake wallet apps, fake airdrops
- SIM-swap: SMS-based 2FA for exchanges
- Supply chain: Compromised hardware wallet sellers
- Smart contract exploits: Approved malicious tokens
- Social engineering: DMs promising "free crypto"

---

## Gold Rules (Non-Negotiable)

### 1. Private keys and seed phrases MUST NOT exist in workspace files

**Files that are NOT safe:**
- `SESSION-STATE.md`
- `working-buffer.md`
- `MEMORY.md`
- `.env` (with the private key itself)
- Any `.json`, `.txt`, `.md` in the workspace
- Any AI conversation history (public platforms)

**Safe alternatives:**
- `.env` only, with keys referenced as env vars at runtime
- Hardware wallets (keys never leave device)
- Encrypted storage with passphrase
- Wallets where private key is never stored at all (watch-only + hardware sign)

### 2. Never process private keys through AI conversation

- Don't send private keys in messages (even to "help analyze")
- Don't ask AI to sign transactions interactively in chat
- Use proper signing infrastructure (hardware wallet, air-gapped setup)
- Private key = one-time use, then never touches the network again

### 3. Assume all workspace files are public

- Every file written to workspace is potentially searchable
- Compaction services, memory systems, and search indexes all scan content
- If it would be bad if exposed, don't write it down

---

## Wallet Architecture

### Strategy: Compartmentalization

**Hot Wallet (Small, Online)**
- Purpose: Daily operations, small amounts
- Balance: $50-500 AUD max
- Examples: DEX trading wallet, Fiverr earnings wallet
- Always: Watch-only access where possible

**Warm Wallet (Medium, Semi-Air-Gapped)**
- Purpose: Active project funds, bounty earnings
- Balance: $500-5000 AUD
- Access: Hardware wallet for signing, watch-only for monitoring
- Examples: Jupiter DCA wallet, Grip Protocol wallet

**Cold Wallet (Large, Offline)**
- Purpose: Long-term holdings, savings
- Balance: >$5000 AUD
- Access: Hardware wallet only, no online access
- Storage: Physically separate from daily devices

### Recommended Wallet Setup

```
Purpose              | Wallet Type        | Key Storage
---------------------|--------------------|----------------------
Trading/Active       | Software (Solflare) | .env, never in files
Grip/Bounty Earn     | Software (MetaMask) | Seed phrase in .env only
Long-Term Savings    | Hardware (Ledger)   | Never touches computer
```

---

## Operational Security Checklist

### Before Handling Any Crypto Asset

- [ ] Is this a new wallet or existing one?
- [ ] Will I need to store a private key or seed phrase?
- [ ] If YES: Can this be done with a hardware wallet instead?
- [ ] If YES: Can the signing happen on a different device than this agent?
- [ ] Is the amount worth the risk of key exposure?

### When Creating New Wallets

1. Generate on air-gapped hardware device OR in proper software wallet
2. Immediately back up seed phrase to physical location (paper/metal)
3. Verify the address BEFORE funding
4. Delete any纸上残留的seed phrase notes
5. Fund only after confirming backup is secure

### When Signing Transactions

- [ ] Use hardware wallet or proper signing infrastructure
- [ ] Verify destination address on device screen
- [ ] Verify amount on device screen
- [ ] Never sign blind (don't sign unknown data)
- [ ] Set appropriate token approval limits (not unlimited)

### For AI Agent Integration

- [ ] Use wallet APIs that don't expose raw private keys
- [ ] Store keys in environment variables, not files
- [ ] Use `signer.py` / `signer.ts` pattern: key in env → sign in-process
- [ ] If possible, use wallet connectors (WalletConnect, Phantom) instead of raw keys
- [ ] Monitor with watch-only addresses (never put watch-only in signing context)

---

## Token Approval Security

### The Danger of "Unlimited Approvals"

When you approve a token spending, you often approve "unlimited" tokens. This means if the contract is malicious or hacked, they can drain your entire balance.

**Rule:** Always set specific approval limits, not unlimited.

### How to Check Approved Tokens

```bash
# Check token approvals on Etherscan/Blockscan
# 1. Go to the address on Blockscan/Polkassembly
# 2. Click "Token Approvals" 
# 3. Revoke any unused or suspicious approvals

# For Base network:
# https://basescan.org/tokenapprovalchecker
```

### Approval Checklist

- [ ] Check approvals before using new dApp
- [ ] Revoke approvals for dApps you no longer use
- [ ] Use limited approvals (exact amount, not unlimited)
- [ ] Be extra careful with USDT, USDC, WETH (high value tokens)

---

## Multi-Signature (Multisig) Setup

For amounts >$5000 AUD, consider multisig:

**Gnosis Safe (Free, on Base)**
- 2-of-3 signers: Hardware wallet + Ledger + Desktop
- Requires multiple devices to authorize any transaction
- Recovery: If one device lost, others still work

**When to Use Multisig:**
- Team/project funds (multiple decision makers)
- Long-term savings (>1 year)
- High-value holdings (>$5000 AUD)
- Any wallet that can't afford to be drained

---

## Incident Response

### If You Suspect a Key Has Been Exposed

1. **Act immediately** — assume compromised until proven otherwise
2. **Check blockchain** — look for outgoing transactions you didn't authorize
3. **If drained**: Transaction is irreversible. Document for records.
4. **Revoke associated API keys**: Any exchange keys that might be linked
5. **If fresh wallet**: Move remaining funds to new wallet immediately
6. **Do NOT**: Continue using the exposed key for anything

### If You Discover a Drain

1. **Save transaction hashes** — evidence for exchange reports
2. **Report to exchange** (if funds were cashed out there)
3. **Check if it was a smart contract exploit** — might be recoverable
4. **Accept the loss** if on-chain and irreversible

### Recovery Is Rare

Unlike credit cards, crypto transactions are irreversible. Prevention is the only real protection.

---

## For OpenClaw Agents: Practical Implementation

### Wallet Strategy for This Agent

```
Wallet Type    | Address           | Storage      | Used For
---------------|-------------------|---------------|--------------------------
Active DCA    | [DISCARDED]          | None        | (empty, was drained)
Bounty Earn   | 0xD1089e...           | .env only   | Grip, ClawMoney
Watch-Only    | [YOUR WALLET]         | TOOLS.md    | Monitor only
New DCA Wallet| TBD (new generation)  | Hardware    | Jupiter DCA (future)
```

### Key Storage Rules

1. **Never write full private keys anywhere** (except .env, which must be gitignored)
2. **Never in conversation**: Even "let me check if this key is correct"
3. **Never in SESSION-STATE.md or working-buffer.md**
4. **Never in memory files after session**
5. **Use hardware wallet** for any amount >$500 AUD

### Environment Variable Pattern

```python
# Correct: Private key in environment only
from dotenv import load_dotenv
load_dotenv()
private_key = os.environ["SOLANA_PRIVATE_KEY"]  # Never written to file

# Wrong: Private key written to any workspace file
# private_key = "[PRIVATE KEY]"  # NEVER DO THIS
```

### Monitoring with Watch-Only Wallets

Use a **different address** for monitoring than for signing:
- Watch address: In TOOLS.md or config files
- Signing address: In hardware wallet only

This way, even if monitoring credentials are exposed, the funds are safe.

---

## Summary: Security vs. Convenience

| Security Level | Use Case | Key Storage |
|----------------|----------|-------------|
| Maximum | Long-term savings | Hardware wallet only |
| High | Active project funds | .env + careful handling |
| Medium | Daily trading | Software wallet, small balance |
| Low | Testing/learning | Any, small amounts |

**Rule of Thumb:** The cost of losing a wallet should never be life-changing. Keep only what you can afford to lose in hot wallets.

---

## Emergency Contacts

- **Base Network Scanner:** https://basescan.org/
- **Token Approval Checker:** https://basescan.org/tokenapprovalchecker
- **Revoke.cash:** https://revoke.cash/
- **Gnosis Safe (Multisig):** https://app.safe.global/
- **Ledger Recovery:** https://www.ledger.com/stop-phishing-attacks

---

_Crypto Guardian v1.0 — Created 2026-05-01 after real wallet theft incident_
