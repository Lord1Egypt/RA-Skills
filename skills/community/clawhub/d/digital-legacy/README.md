# Digital Legacy

> Your digital life outlives you. Plan for it.

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs) / OpenClaw skill
that helps you create a **digital inheritance plan**: inventory accounts,
subscriptions, and crypto wallets; document your wishes for each; and generate
an **encrypted digital will** plus a **printable emergency access guide** for
trusted family members.

## Why

When someone dies or becomes incapacitated, their family faces a maze of
unknown accounts, unrecoverable passwords, lost crypto wallets, and
auto-renewing subscriptions. Most people have dozens of digital accounts their
family doesn't know exist. Without a plan, digital assets are lost, bills keep
charging, and closing accounts becomes a months-long detective project.

Digital Legacy structures the solution: a complete inventory, clear wishes, and
encrypted instructions that only your trusted person can open.

## What's Included

- **`SKILL.md`** — core skill: security model, workflow, quick-reference.
- **`references/`**
  - `security-best-practices.md` — encryption, passphrase management, storage.
  - `account-checklist.md` — 100+ account types across 10 categories.
  - `platform-policies.md` — Google, Apple, Facebook, etc. legacy policies.
  - `workflow-guide.md` — full step-by-step setup and maintenance process.
- **`scripts/digital_legacy.py`** — main tool: inventory, encryption, guide.
- **`scripts/templates/template_will.md`** — plaintext will template.
- **`scripts/templates/template_guide.html`** — emergency guide HTML template.

## Quick Start

```bash
# Interactive full setup (recommended for first time)
python3 scripts/digital_legacy.py setup

# Or build incrementally
python3 scripts/digital_legacy.py init
python3 scripts/digital_legacy.py add-account
python3 scripts/digital_legacy.py add-subscription
python3 scripts/digital_legacy.py add-wallet

# View your inventory
python3 scripts/digital_legacy.py list

# Generate the encrypted will
python3 scripts/digital_legacy.py generate-will

# Generate the printable emergency guide
python3 scripts/digital_legacy.py emergency-guide

# Decrypt and read the will later
python3 scripts/digital_legacy.py read-will digital_will.enc
```

Example emergency guide output (HTML):

```html
<h1>Digital Emergency Access Guide</h1>
<p>Prepared for: [Trusted Person Name]</p>
<p>From: [Your Name]</p>
<hr>
<h2>If Something Happens to Me:</h2>
<ol>
  <li>Find the file <strong>digital_will.enc</strong> on my computer</li>
  <li>The passphrase hint is: [your hint]</li>
  <li>Run: <code>python3 digital_legacy.py read-will digital_will.enc</code></li>
  <li>Enter the passphrase when prompted</li>
</ol>
```

## Security Model

| Component              | How It Works                                      |
| ---------------------- | ------------------------------------------------- |
| Encryption             | AES-256-GCM                                       |
| Key derivation         | PBKDF2-SHA256, 100,000 iterations                 |
| Passphrase storage     | NOT stored anywhere. You must remember/secure it. |
| Encrypted file format  | Salt + nonce + ciphertext + auth tag              |
| Inventory file         | Plaintext JSON (no secrets — just metadata)       |

> The inventory (`accounts.json`) contains **metadata only**: service names,
> account types, and your wishes. It does NOT contain passwords or seed
> phrases. Those go only in the encrypted will.

## Three Deliverables

1. **`accounts.json`** — plaintext inventory (metadata, no secrets)
2. **`digital_will.enc`** — encrypted instructions (access details, wishes)
3. **`emergency_guide.html`** — printable guide for your trusted person

## Installation (Hermes Agent)

Copy or symlink this directory into your skills folder:

```bash
cp -r digital-legacy ~/.hermes/skills/
```

Hermes auto-discovers skills with a valid `SKILL.md`. See the
[skills docs](https://hermes-agent.nousresearch.com/docs) for details.

## Requirements

- Python 3.8+ (stdlib only — no pip install needed)
- The `hashlib` and `hmac` modules are used for key derivation (stdlib)

## Legal Disclaimer

This tool creates an informational document to help your family access your
digital accounts. It is **not** a legally binding will or estate plan. For
legally enforceable estate planning, consult a qualified attorney in your
jurisdiction.

## License

MIT © Denis Voronin
