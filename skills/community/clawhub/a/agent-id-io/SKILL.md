---
name: agent-id-io
version: "1.0.2"
description: >
  OpenClaw skill for the agent-id.io identity and trust service. Use it to
  register an AI agent, authenticate with challenge/response, manage passkeys
  and cryptographic keys, verify domains/repos/websites, handle sponsorships,
  and inspect public agent profiles. Triggers on: "agent-id.io", "register
  agent identity", "authenticate agent", "rotate agent keys", "verify agent
  identity", and "agent sponsorship".
---

# agent-id.io

**What it is:** OpenClaw skill for operating against the `agent-id.io` service. The service provides identity, authentication, verification, and trust primitives for AI agents. Each agent has a self-sovereign Ed25519/X25519 keypair, and authentication uses challenge/response plus passkey-based flows without sending private keys to the server.

**Base URL:** `https://agent-id.io/v1`

## Setup (pinned dependencies)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependency policy:
- Runtime dependencies are pinned in `requirements.txt`
- If you maintain this skill, run `pip-audit` and your preferred test flow before publishing updates

---

## 1. Register a New Agent

Generate keypair locally, then POST to register. The server never receives the private key.

```bash
# Generate Ed25519 signing key + X25519 encryption key
python3 scripts/keygen.py
# → Outputs: agent_keys.json (private, keep secret) + public keys as base64

# Register
curl -s -X POST https://agent-id.io/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "my-agent",
    "public_sign_key": "<base64 Ed25519 pubkey>",
    "public_enc_key":  "<base64 X25519 pubkey>"
  }'
# → { "agent_id": "uuid", "display_name": "...", "created_at": "..." }
```

**Save the `agent_id` and `agent_keys.json` securely.** Lost private key = lost identity.

---

## 2. Authenticate (Get a Token)

Authentication is a two-step challenge/response:

```bash
AGENT_ID="<your-uuid>"

# Step 1: Get challenge
CHALLENGE=$(curl -s -X POST https://agent-id.io/v1/auth/challenge \
  -H "Content-Type: application/json" \
  -d "{\"agent_id\": \"$AGENT_ID\"}" | python3 -c "import json,sys; print(json.load(sys.stdin)['challenge'])")

# Step 2: Sign challenge + verify
python3 scripts/sign_challenge.py "$CHALLENGE" agent_keys.json
# → Outputs the auth/verify payload as JSON

# POST the signed payload
TOKEN=$(curl -s -X POST https://agent-id.io/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d "$(cat signed_challenge.json)" | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")
```

Token is a JWT, valid 15 minutes, not refreshable. Re-authenticate when expired.

**Usage:** `Authorization: Bearer $TOKEN`

---

## 3. Manage Passkeys

Passkeys = the WebAuthn credentials tied to your agent's public key. Free tier: 2 passkeys max.

### Add a passkey
```bash
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/passkeys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "credential_id": "<base64url>",
    "public_key": "<base64url>",
    "attestation_object": "<base64url>"
  }'
```

### List passkeys (via agent profile)
```bash
curl -s "https://agent-id.io/v1/agents/$AGENT_ID"
```

### Delete a passkey
```bash
curl -s -X DELETE "https://agent-id.io/v1/agents/$AGENT_ID/passkeys/<passkey_id>" \
  -H "Authorization: Bearer $TOKEN"
# 204 No Content on success
# 409 last_passkey → cannot delete the only remaining passkey
```

---

## 4. Rotate Cryptographic Keys

Use when private key is compromised or as routine hygiene. Requires signing new key with old private key.

```bash
python3 scripts/rotate_keys.py agent_keys.json
# → Generates new_agent_keys.json + rotation_payload.json

curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/keys/rotate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(cat rotation_payload.json)"
# → { "agent_id": "...", "public_sign_key": "<new>", "rotated_at": "..." }
```

After rotation: replace `agent_keys.json` with `new_agent_keys.json`. Old tokens are still valid until expiry.

---

## 5. Verify Identity

Three verification methods — all start a pending verification, then a check call resolves it.

### Domain TXT verification
```bash
# Start verification
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/domain" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
# → { record_name: "_agent-id.example.com", expected_txt_value: "agent-id-verification=..." }

# Add DNS TXT record, then check
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/domain/check" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

### Code repository
```bash
# Start: provide repo URL + proof file URL
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/code-repo" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/org/repo", "proof_url": "https://raw.githubusercontent.com/org/repo/main/.well-known/agent-id-proof.txt"}'
# → { expected_proof_value: "agent-id-verification=..." }

# Create .well-known/agent-id-proof.txt with exact value, commit, then check
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/code-repo/check" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"proof_url": "..."}'
```

### Website file
```bash
# Start
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/website-file" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"domain": "example.org"}'
# → Proof file expected at https://example.org/.well-known/agent-id-verification.txt

# Create file with exact expected value, then check
curl -s -X POST "https://agent-id.io/v1/agents/$AGENT_ID/verify/website-file/check" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"domain": "example.org"}'
```

---

## 6. Sponsorship

Sponsorship = cryptographic vouching. Sponsor signs the sponsored agent's public key.

```bash
# Request sponsorship from a known agent
curl -s -X POST https://agent-id.io/v1/sponsorship/request \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"sponsor_agent_id": "<sponsor-uuid>"}'

# Sponsor: view pending requests
curl -s https://agent-id.io/v1/sponsorship/requests \
  -H "Authorization: Bearer $SPONSOR_TOKEN"

# Sponsor: approve (sign requester's public_sign_key with your private key)
python3 scripts/sign_sponsorship.py <requester_public_sign_key_base64> agent_keys.json
curl -s -X POST "https://agent-id.io/v1/sponsorship/requests/<request_id>/approve" \
  -H "Authorization: Bearer $SPONSOR_TOKEN" -H "Content-Type: application/json" \
  -d '{"sponsor_signature": "<base64 Ed25519 sig>"}'
```

---

## 7. Look Up Agents (Public, No Auth)

```bash
# Get agent profile
curl -s "https://agent-id.io/v1/agents/<agent_id>"

# Get agent's public keys
curl -s "https://agent-id.io/v1/agents/<agent_id>/keys"

# List agents sponsored by a specific agent
curl -s "https://agent-id.io/v1/agents?sponsor=<sponsor_agent_id>"
```

---

## 8. Derive SSH + PGP Keys from Master Seed

The Ed25519 master seed is the single source of truth. All other keys are derived deterministically — **one backup covers everything**.

```bash
# Derive SSH + PGP keys from agent_keys.json master seed
python3 scripts/derive_keys.py agent_keys.json --out-dir ~/.ssh

# Outputs:
#   ~/.ssh/id_agent_ed25519      (SSH private key, OpenSSH format, chmod 600)
#   ~/.ssh/id_agent_ed25519.pub  (SSH public key)
#   ~/.ssh/agent_pgp_private.asc (PGP private key, ASCII-armored)
#   ~/.ssh/agent_pgp_public.asc  (PGP public key)

# Import PGP key to GPG keyring
gpg --import ~/.ssh/agent_pgp_private.asc
```

**Key hierarchy:**
```
master_seed (Ed25519 seed, 32 bytes)
├── HKDF(info="agent-id/ssh-ed25519") → SSH Ed25519 key
└── HKDF(info="agent-id/pgp-ed25519") → PGP Ed25519 key
```

Keys are deterministic: the same `agent_keys.json` always produces the same SSH + PGP keys. Safe to regenerate anytime from backup.

---

## 9. Secure Key Storage

The agent is responsible for keeping the master keyfile secure. Treat `agent_keys.json` like a private key — it IS one.

Security warning: inline environment variable assignments like `AGENT_KEY_PASSPHRASE=... python3 ...` are less safe. They can be exposed through `/proc/<pid>/environ`, shell history, process logging, or terminal scrollback.

**Encrypt the keyfile (AES-256-GCM + scrypt):**
```bash
# Encrypt (preferred: interactive prompt, avoids exposing the passphrase inline)
python3 scripts/secure_keyfile.py encrypt agent_keys.json
# → creates agent_keys.json.enc
rm agent_keys.json  # delete plaintext

# Decrypt on use (preferred: interactive prompt)
python3 scripts/secure_keyfile.py decrypt agent_keys.json.enc --out /tmp/keys.json
python3 scripts/authenticate.py /tmp/keys.json --save-token /tmp/agent_token.jwt
rm /tmp/keys.json /tmp/agent_token.jwt  # delete immediately after use

# Less safe fallback: passphrase via environment variable
AGENT_KEY_PASSPHRASE="<strong-passphrase>" python3 scripts/secure_keyfile.py encrypt agent_keys.json
AGENT_KEY_PASSPHRASE="<strong-passphrase>" python3 scripts/secure_keyfile.py decrypt agent_keys.json.enc --out /tmp/keys.json
```

**Where the passphrase lives:**
- A secret manager you already trust
- An environment variable injected at runtime, for example `AGENT_KEY_PASSPHRASE`
- Never hardcoded, never in config files, never in git

**Storage pattern:**
- Keep `agent_keys.json.enc` as the portable encrypted artifact
- Store the passphrase separately from the encrypted file
- If you sync backups offsite, encrypt first and verify restore steps periodically

**Backup strategy:**
- The encrypted `agent_keys.json.enc` can be stored anywhere you already trust for encrypted backups
- The passphrase must be stored separately from the keyfile
- Losing both = permanent identity loss

---

## Scripts

All scripts are in `scripts/`. See each file's header for usage.

| Script | Purpose |
|--------|---------|
| `scripts/register.py` | Full registration incl. PoW challenge/solve |
| `scripts/authenticate.py` | Auth flow → JWT token (`--save-token` or `--print-token`) |
| `scripts/keygen.py` | Generate Ed25519 + X25519 keypair → `agent_keys.json` |
| `scripts/sign_challenge.py` | Sign auth challenge manually → `signed_challenge.json` |
| `scripts/rotate_keys.py` | Generate new keypair + rotation signature |
| `scripts/sign_sponsorship.py` | Sign requester's pubkey for sponsorship approval |
| `scripts/derive_keys.py` | Derive SSH + PGP keys from master seed (HKDF) |
| `scripts/secure_keyfile.py` | Encrypt/decrypt agent_keys.json (AES-256-GCM + scrypt) |

---

## Error Handling

Key errors to handle:

| Error | Meaning | Action |
|-------|---------|--------|
| `409 conflict` | Key already registered | Generate new keypair |
| `409 passkey_limit_reached` | Free tier: max 2 passkeys | Delete old or upgrade |
| `409 last_passkey` | Cannot delete last passkey | Add another first |
| `403 agent_revoked` | Identity revoked | Call `POST /agents/{id}/unrevoke` |
| `400 invalid_challenge` | Challenge expired (>60s) | Re-fetch challenge |
| `401 unauthorized` | Token expired or invalid | Re-authenticate |

For full API reference: `references/api.md`
