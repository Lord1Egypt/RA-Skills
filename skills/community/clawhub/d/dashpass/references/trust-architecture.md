# DashPass Trust Architecture

> Your credentials, your keys, your control. AI is just the messenger.

---

## Why This Document Exists

Password managers ask you to trust a company. DashPass asks you to trust math and open-source code.

This document explains how DashPass is designed so that you **never need to trust the AI** managing your credentials. Every claim here is verifiable — that's the point.

---

## The Three Layers of Trust Minimization

### 1. Transparency Layer — Everything Is Auditable

**On-chain audit trail:** Every credential operation (create, read, rotate, delete) can be logged to the Dash blockchain. Blockchain entries are immutable — nobody can edit or delete the history, not even the system administrators.

**Open-source code:** The entire DashPass codebase is open. You can read the encryption logic, verify there are no backdoors, and build it yourself. "Trust, but verify" becomes just "verify."

**Independent verification:** Any credential stored on Dash Platform can be independently verified using standard cryptographic tools. You don't need DashPass software to prove your data is intact — you need math.

### 2. Control Layer — Humans Hold the Keys

**You hold the master key (WIF):** The private key that encrypts and decrypts your credentials never leaves your machine. It's not stored on any server, not transmitted over the network, and not accessible to the AI agent. The AI can ask the system to decrypt — but the system uses *your* key, stored in *your* environment.

**One-click revocation:** If an AI agent misbehaves, you can:
- Delete the environment variable (instant: AI loses all access)
- Rotate the WIF (all credentials re-encrypted, old key worthless)
- Revoke the Platform Identity key (permanent: on-chain access removed)

**CRITICAL-level human confirmation:** Credentials marked "critical" (like mainnet private keys or primary API keys) require explicit human approval before any AI agent can access or modify them. The AI cannot escalate its own permissions.

**Principle:** The human is always one step away from pulling the plug. No ceremony, no waiting period, no "are you sure?" — just delete the key.

### 3. Verifiability Layer — Don't Believe, Check

**Client-side encryption:** Credentials are encrypted on your machine *before* they touch the network. Dash Platform nodes store ciphertext — they literally cannot read your secrets, even if every node operator collaborated. This is mathematically guaranteed by AES-256-GCM (the same encryption used by governments and banks).

**Cache is optional and encrypted:** The local cache (for offline/fast access) is encrypted with a key derived from your master key. You can disable caching entirely with `DASHPASS_CACHE=none` — every access goes directly to the blockchain.

**Every claim is falsifiable:** If someone claims "DashPass can't read your credentials," you can verify this by:
1. Reading the open-source encryption code
2. Capturing network traffic (you'll see only ciphertext)
3. Querying Dash Platform directly (you'll see only encrypted blobs)
4. Changing your WIF and confirming old ciphertext becomes unreadable

---

## How DashPass Actually Works (Simplified)

```
You (human) → create a private key (WIF)
                    ↓
              Store WIF securely on your machine
                    ↓
AI agent → "store this API key for service X"
                    ↓
         Your machine encrypts the value using YOUR key
                    ↓
         Encrypted blob uploaded to Dash blockchain
                    ↓
AI agent → "retrieve the API key for service X"
                    ↓
         Encrypted blob downloaded from Dash blockchain
                    ↓
         Your machine decrypts using YOUR key
                    ↓
         Plaintext value given to AI agent (in memory only)
```

**What the AI never has:** Your private key. It has *access to a system* that uses your key, but the key itself stays in environment variables that the AI cannot exfiltrate.

**What Dash Platform nodes never have:** Your plaintext credentials. They store encrypted blobs and metadata. Even if every Platform node was compromised, your secrets remain encrypted.

---

## Comparison: DashPass vs. Traditional Password Managers

| Aspect | 1Password / Bitwarden | DashPass |
|--------|:---------------------:|:--------:|
| **Where are credentials stored?** | Company's cloud servers | Decentralized blockchain (Dash Platform) |
| **Who can access the servers?** | Company employees, law enforcement with warrant | No one — data is distributed across thousands of nodes |
| **Master secret type** | Password (human-memorable, guessable) | 256-bit cryptographic key (not guessable) |
| **Can the company read your data?** | They claim no (zero-knowledge) — you trust their claim | Provably no — client-side encryption is verifiable |
| **What if the company is breached?** | Encrypted vaults may be stolen (LastPass, 2022) | No central server to breach |
| **What if the company shuts down?** | You lose access (unless you exported) | Blockchain persists — your data outlives any company |
| **AI agent support** | Limited, not designed for programmatic access | Built for AI agents from day one |
| **Audit trail** | Internal logs (you trust the company) | On-chain logs (you trust math) |
| **Vendor lock-in** | Proprietary formats | Open standard on a public blockchain |

**The key difference:** Traditional password managers ask you to trust that a company *won't* read your data. DashPass makes it so they *can't* — not because of policy, but because of math.

---

## Trust Minimization: A Blockchain Philosophy

DashPass inherits its trust model from the blockchain world:

> "Don't trust. Verify."

In Bitcoin, you don't trust a bank to hold your money — the network enforces the rules mathematically. In DashPass, you don't trust an AI to protect your secrets — the encryption enforces the rules mathematically.

| Traditional trust | Trust-minimized equivalent |
|-------------------|---------------------------|
| "The AI won't steal my keys" | "The AI never sees my keys" |
| "The server won't be breached" | "There is no central server" |
| "The company won't read my data" | "The data is encrypted before it leaves my machine" |
| "The audit log is accurate" | "The audit log is on a blockchain and can't be forged" |

This is not about believing AI is good. It's about building systems where it doesn't matter if it's not.

---

## What DashPass Does NOT Protect Against

Transparency requires honesty about limitations:

- **Compromised machine:** If malware has root access to your computer, it can read your WIF from memory. DashPass encrypts data at rest and in transit — not in a compromised runtime.
- **Lost master key:** If you lose your WIF and have no backup, your credentials are gone forever. This is the same trade-off as a Bitcoin private key: total control means total responsibility.
- **Metadata visibility:** Service names and credential types are visible on the blockchain (so the system can look them up). The *values* are encrypted, but an observer can see *which services* you use.
- **Social engineering:** If someone tricks you into giving them your WIF, they can decrypt everything. Technology can't fix human judgment.

---

## The Bottom Line

DashPass is built on a simple principle: **the best security is the kind that doesn't require trust.**

You don't need to trust the AI. You don't need to trust Dash Platform node operators. You don't need to trust the DashPass developers. You need to:

1. **Keep your private key safe** (like any crypto wallet)
2. **Verify the code** (it's open source)
3. **Check the chain** (it's a public blockchain)

Everything else is math.
