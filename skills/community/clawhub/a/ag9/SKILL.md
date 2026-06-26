---
name: ag9
description: Use AG9 to register and verify AI agents with VeryAI Palm-backed human ownership, generate or load portable Ed25519 identities for OpenClaw, Codex, local CLI/MCP, browser, or cloud agents, call AG9 registration/signature verification APIs, and solve reverse-CAPTCHA capability challenges.
---

# ag9 — Know Your Agent

ag9 proves two things about an agent that no other layer proves together:

1. **A real human owns this agent** — palm-bound via VeryAI. The human scans their palm once; the agent is now cryptographically tied to a verified person.
2. **A real model is operating** — reverse CAPTCHA. Three challenge families (byte transforms, constrained generation, structured extraction) that capable LLMs can solve in seconds and naive scripts cannot.

Both live at `https://api.ag9.ai`. Note the two base URLs:

- **Path A (human ownership)** uses `https://api.ag9.ai/v1/agent/...`
- **Path B (reverse CAPTCHA)** uses `https://api.ag9.ai/challenge`, `/verify`, and `/.well-known/jwks.json` at the **root** (not under `/v1`) to match existing OpenClaw/monkey-api integrations.

This URL split is intentional, not a typo — both endpoints are served by the same ag9-api service.

## What this skill accesses on your machine

- **`~/.openclaw/identity/device.json`** (read). Used first when present. OpenClaw owns this identity file.
- **`~/.ag9/identity.json`** (read/write). Used when OpenClaw identity is absent. The skill may create this file with a stable `deviceId`, `publicKeyPem`, and `privateKeyPem`.
- **Private key handling:** The private key never leaves your machine or cloud secret store. Only `deviceId`, base64 `publicKey`, `message`, `signature`, and `timestamp` are sent to ag9. Path B (reverse CAPTCHA) does not touch identity files.
- **No other filesystem access.** No background processes. No outbound network calls other than `https://api.ag9.ai`.

> **CRITICAL: Never open browsers**
>
> Do **not** use `open`, `xdg-open`, `start`, or any command that opens a browser. Always output the **registration URL** as a text or markdown link for the user to click.
>
> - WRONG: `open "https://api.very.org/oauth2/..."`
> - CORRECT: "Open this link to complete verification: https://api.very.org/oauth2/..."

## Key files

| File     | Purpose                                                                                       |
| -------- | --------------------------------------------------------------------------------------------- |
| SKILL.md | Installed skill instructions for registration, reverse CAPTCHA, verification, and API usage   |
| Identity | `~/.openclaw/identity/device.json` or `~/.ag9/identity.json` — deviceId and keys (never send private key) |

## Security

- **Private key**: Used to sign the challenge. Never send the private key to ag9 or any server; only send `publicKey`, `message`, and `signature`.
- **Registration URL**: Single-use and short-lived. Give it only to the human owner who will complete VeryAI palm verification.
- **deviceId**: Use a stable identifier. For generated AG9 identities, derive it from the public key fingerprint. It ties the agent to the registration and is used for lookup and verification.
- **Challenge token** (reverse CAPTCHA): HMAC-signed, 15 seconds, single-use. The token carries the answer hash so the server does not keep any per-request state.
- **Capability JWT**: Ed25519-signed attestation returned after a successful `/verify`. Public key at `GET /.well-known/jwks.json` so any party can verify offline.

---

## Path A: Human ownership (agent ↔ human binding)

Use this when you need a third party to know the agent is owned by a verified human.

### Generating the AgentChallenge

The **AgentChallenge** is a signed payload that shows you control an Ed25519 key. It has the shape used by standard OpenClaw identity flows: `deviceId`, `publicKey`, `message`, `signature`, `timestamp`. Generate it once and send it to `/agent/register/init` or `/agent/verify/signature`.

#### Where identity comes from

Resolve identity in this order:

1. **Cloud secret identity** — if `AG9_DEVICE_ID` and private/public key env vars exist, use them. This is the right path for Vercel, AWS, GCP, Cloudflare, and other hosted agents.
2. **OpenClaw identity** — if `~/.openclaw/identity/device.json` exists, use it.
3. **Portable AG9 identity** — otherwise load or create `~/.ag9/identity.json`. This is the default for Codex, local CLI agents, local MCP servers, and other agents without a native identity store.

If you run on OpenClaw, device identity is stored at:

- **Path:** `~/.openclaw/identity/device.json`

That file contains (never send `privateKeyPem` to any server):

| Field           | Use                                                                      |
| --------------- | ------------------------------------------------------------------------ |
| `deviceId`      | Use as `deviceId` in the challenge. Stable id for this agent/device.     |
| `publicKeyPem`  | Use to derive `publicKey` (see below).                                   |
| `privateKeyPem` | Use only locally to sign the message. **Never include in API requests.** |

If you do not use OpenClaw, the recommended local identity path is:

- **Path:** `~/.ag9/identity.json`

Use the same shape:

```json
{
  "deviceId": "ag9_agent_...",
  "publicKeyPem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
  "privateKeyPem": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "createdAt": "2026-05-12T00:00:00.000Z",
  "provider": "ag9-local",
  "label": "local-agent"
}
```

For cloud agents, do not write this file on ephemeral disk. Generate the same identity once during provisioning and store `deviceId`, `publicKeyPem`, and `privateKeyPem` in the cloud secret manager. The runtime should load those values from environment variables or mounted secrets:

```bash
AG9_DEVICE_ID=ag9_agent_...
AG9_PUBLIC_KEY_PEM_B64=base64-encoded-public-pem
AG9_PRIVATE_KEY_PEM_B64=base64-encoded-private-pem
```

Plain multiline `AG9_PUBLIC_KEY_PEM` and `AG9_PRIVATE_KEY_PEM` are also valid when the platform supports multiline secrets.

#### Build the challenge (step-by-step)

1. **Choose the message to sign**
   For registration, use a one-time challenge to avoid replay, e.g.:
   - `ag9-register-<unix_timestamp_ms>`
     Example: `ag9-register-1776646678000`
     For verify/signature, the message is whatever you are proving (e.g. a nonce from a third party).

2. **Sign the message** with your Ed25519 **private** key. The signature must be over the **exact** UTF-8 bytes of `message` (no extra prefix/suffix).

3. **Encode for the API:**
   - **publicKey**: Ed25519 public key in **SPKI DER** form, then **base64** (no PEM wrapper).
   - **signature**: Raw Ed25519 signature bytes, **base64**.
   - **timestamp**: Unix time in **milliseconds** when the challenge was created (e.g. `Date.now()`).

4. **JSON body (AgentChallenge):**
   - `deviceId` — from your identity (e.g. `device.json`)
   - `publicKey` — base64 DER SPKI
   - `message` — exact string that was signed
   - `signature` — base64 signature
   - `timestamp` — number (ms)

#### Example: Node.js, OpenClaw or `~/.ag9`

```javascript
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

function base64url(buffer) {
  return Buffer.from(buffer)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/g, "");
}

function pemFromEnv(name) {
  if (process.env[name]) {
    return process.env[name];
  }
  const b64 = process.env[`${name}_B64`];
  return b64 ? Buffer.from(b64, "base64").toString("utf8") : "";
}

function loadOrCreateIdentity() {
  const envIdentity = {
    deviceId: process.env.AG9_DEVICE_ID,
    publicKeyPem: pemFromEnv("AG9_PUBLIC_KEY_PEM"),
    privateKeyPem: pemFromEnv("AG9_PRIVATE_KEY_PEM"),
    provider: "ag9-env",
  };
  if (envIdentity.deviceId && envIdentity.publicKeyPem && envIdentity.privateKeyPem) {
    return envIdentity;
  }

  const openClawPath = path.join(process.env.HOME, ".openclaw/identity/device.json");
  if (fs.existsSync(openClawPath)) {
    return JSON.parse(fs.readFileSync(openClawPath, "utf8"));
  }

  const ag9Path = path.join(process.env.HOME, ".ag9/identity.json");
  if (fs.existsSync(ag9Path)) {
    return JSON.parse(fs.readFileSync(ag9Path, "utf8"));
  }

  const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519");
  const publicKeyDer = publicKey.export({ type: "spki", format: "der" });
  const fingerprint = base64url(crypto.createHash("sha256").update(publicKeyDer).digest()).slice(0, 32);
  const identity = {
    deviceId: `ag9_agent_${fingerprint}`,
    publicKeyPem: publicKey.export({ type: "spki", format: "pem" }),
    privateKeyPem: privateKey.export({ type: "pkcs8", format: "pem" }),
    createdAt: new Date().toISOString(),
    provider: "ag9-local",
    label: "local-agent",
  };

  fs.mkdirSync(path.dirname(ag9Path), { recursive: true, mode: 0o700 });
  fs.writeFileSync(ag9Path, JSON.stringify(identity, null, 2), { mode: 0o600 });
  return identity;
}

const identity = loadOrCreateIdentity();

const message = `ag9-register-${Date.now()}`;
const privateKey = crypto.createPrivateKey(identity.privateKeyPem);
const signature = crypto.sign(null, Buffer.from(message, "utf8"), privateKey);

const publicKeyDer = crypto
  .createPublicKey(identity.publicKeyPem)
  .export({ type: "spki", format: "der" });

const challenge = {
  deviceId: identity.deviceId,
  publicKey: publicKeyDer.toString("base64"),
  message,
  signature: signature.toString("base64"),
  timestamp: Date.now(),
};
// POST challenge to https://api.ag9.ai/v1/agent/register/init
```

#### Using a script

If you have a script that already produces an AgentChallenge (e.g. signs a message and outputs JSON with `deviceId`, `publicKey`, `message`, `signature`, `timestamp`), you can reuse it for ag9:

1. Generate a challenge string, e.g. `ag9-register-$(date +%s)000` (seconds + "000" for ms) or use your script's convention.
2. Run the script to sign that message and get the challenge JSON.
3. POST that JSON to `https://api.ag9.ai/v1/agent/register/init`.

Same challenge format works for `POST /agent/verify/signature` when verifying a signature remotely.

### Quick start — human ownership

#### 1. Start registration (agent-initiated)

Build an **AgentChallenge** as above, then send it to ag9 to create a session and get a registration URL.

```bash
curl -X POST https://api.ag9.ai/v1/agent/register/init \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "my-agent-device-id",
    "publicKey": "<base64-DER-SPKI-Ed25519>",
    "message": "ag9-register-1776646678000",
    "signature": "<base64-Ed25519-signature>",
    "timestamp": 1776646678000
  }'
```

**Response (201):**

- `sessionId` — use to poll status
- `registrationUrl` — **output this as a link for the human; do not open it in a browser**
- `expiresAt` — session expiry (ISO 8601)

If the agent is already registered (`deviceId` exists), the API returns **409 Conflict**.

#### 2. Human completes verification

Tell the human owner to open the `registrationUrl` in their browser. They will go through VeryAI's palm verification via OAuth. When they finish, the agent is registered under their ownership.

#### 3. Poll registration status

Poll until the human has completed or the session has expired:

```bash
curl "https://api.ag9.ai/v1/agent/register/SESSION_ID/status"
```

**Response:** `status` is one of `pending` | `completed` | `expired` | `failed`. When `status` is `completed`, the response includes `deviceId` and `registration` (e.g. `publicKey`, `registeredAt`).

#### 4. Verify signatures or look up an agent

- **Verify a signature** — check that a message was signed by the given key and whether that agent is registered under a verified human:

```bash
curl -X POST https://api.ag9.ai/v1/agent/verify/signature \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "...",
    "publicKey": "...",
    "message": "...",
    "signature": "...",
    "timestamp": 1776646678000
  }'
```

Response: `verified` (signature valid), `registered` (agent under verified human).

- **Look up an agent by device id** — get registration and verification status:

```bash
curl "https://api.ag9.ai/v1/agent/verify/device/DEVICE_ID"
```

Response: `registered`, `verified`, `humanId`, and optionally `registeredAt`.

- **Look up an agent by public key** (base64 DER SPKI):

```bash
curl "https://api.ag9.ai/v1/agent/verify/public-key/$(printf '%s' "$PUBKEY_B64" | jq -sRr @uri)"
```

---

## Path B: Reverse CAPTCHA (prove a real model is operating)

Use this when a relying party needs to confirm the requester is a capable agent (not a naive script), independent of any human binding. Stateless, no account needed.

### Endpoint summary

| Method | Path                     | Purpose                                                                    |
| ------ | ------------------------ | -------------------------------------------------------------------------- |
| POST   | `/challenge`             | Issue a single-use HMAC-signed challenge (15s TTL).                        |
| POST   | `/verify`                | Submit `{token, solution}`; receive an Ed25519-signed capability JWT.      |
| GET    | `/.well-known/jwks.json` | Public key (JWKS) for offline JWT verification.                            |

These live at the **root**, not under `/v1`, to match existing OpenClaw/monkey-api integrations.

### 1. Request a challenge

```bash
curl -s -X POST https://api.ag9.ai/challenge \
  -H "Content-Type: application/json" -d '{}'
```

Optional `?type=byte_transform|structured_extraction|constrained_gen` pins the family. Omit for random.

**Response (200):**

```json
{
  "challenge_id": "string",
  "challenge_type": "byte_transform | structured_extraction | constrained_gen",
  "difficulty": "medium",
  "payload": { /* shape depends on challenge_type — see below */ },
  "token": "base64url-encoded HMAC-signed token carrying the answer hash",
  "expires_at": 1776646678,
  "time_limit_secs": 30
}
```

### 2. Solve and submit

Compute the answer from `payload` (family-specific — see next section). Submit:

```bash
curl -s -X POST https://api.ag9.ai/verify \
  -H "Content-Type: application/json" \
  -d '{ "token": "...", "solution": "..." }'
```

**Response (200):**

```json
{
  "success": true,
  "jwt": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9..."
}
```

The JWT is a capability attestation the relying party can verify offline using the public key at `/.well-known/jwks.json`. Claims include `iss` (`api.ag9.ai`), `sub` (`agent_capability_attestation`), `challenge_type`, `difficulty`, `solved_at`, `solve_time_ms`.

### 3. Family-specific payloads

#### `byte_transform`

```json
{
  "data": "<base64 of 256 random bytes>",
  "instructions": [
    "Transform every byte by XOR-ing it with 19 (decimal).",
    "Rotate all bytes left by 192 positions (with wraparound).",
    "Starting at byte 5, going up to byte 66, reverse the sub-array end to end."
  ]
}
```

**Answer:** Apply the transforms in order to the decoded bytes, then return `sha256(final_bytes)` as lowercase hex (64 chars). Typical approach: LLM writes Python, agent executes it. Time limit 30s.

#### `structured_extraction`

```json
{
  "document": "<malformed HTML/JSON/XML blob with authoritative and decoy values>",
  "fields": ["author_name", "price_usd", "publish_date"]
}
```

**Answer:** Extract each field's **authoritative** value, join with `|` (pipe), in the exact order listed. The document mixes current and stale/decoy values of the same type. Context clues to **prefer**: `data-verified="true"`, `data-primary="true"`, `data-source="authoritative"`, `data-kind="live"`, `id="product-current"`, `<section data-kind="live">`, `<item status="current">`, `<main>`. Clues to **avoid**: `id="product-archive"`, `status="draft"`, `data-kind="historical"`, `<aside>`, `display:none`, `<noscript>`, HTML comments. Fields can live in `<script type="application/json">` or `<meta>` tags — read them, decide by attributes. Time limit 30s.

#### `constrained_gen`

```json
{
  "topic": "ocean waves",
  "lines": 4,
  "ascii_target": 419,
  "word_count": 20,
  "difficulty": "medium"
}
```

**Answer:** A plain-text block of exactly `lines` non-empty lines totaling `word_count` words, where the sum of ASCII codes of the first character of each trimmed line equals `ascii_target` (lowercase `a`=97 through `z`=122). Recommended approach: choose first letters `l_1..l_n` such that `sum(ord(l_i)) == ascii_target`, each in `[97, 122]`; then pad with short filler words until `word_count` is reached. Time limit 20s.

### 4. Verify the JWT offline

Any relying party can verify the attestation without calling ag9 back:

```bash
curl -s https://api.ag9.ai/.well-known/jwks.json
```

Then verify the JWT signature using the returned Ed25519 public key. Cache-Control is `public, max-age=3600`.

---

## When to use which path

| Need                                                       | Path                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| Prove a human owns this agent                              | **A** — registration + `/agent/verify/device/{deviceId}` |
| Prove a capable LLM is operating (no human/account needed) | **B** — `/challenge` + `/verify`                         |
| Prove both                                                 | Run A first, then B on each outbound request             |
| Third-party wants to check your agent                      | They call either `/agent/verify/device/{id}` (A) or accept a JWT you present (B) |

## API reference

**Base URL:** `https://api.ag9.ai/v1` (human-ownership endpoints)
**Base URL (root):** `https://api.ag9.ai` (reverse-CAPTCHA endpoints)
**Local:** `http://localhost:3000`

### Endpoints

| Method | Endpoint                                    | Auth | Description                                                                      |
| ------ | ------------------------------------------- | ---- | -------------------------------------------------------------------------------- |
| POST   | `/v1/agent/register/init`                   | None | Start registration session; returns `sessionId`, `registrationUrl`, `expiresAt`. |
| GET    | `/v1/agent/register/{sessionId}/status`     | None | Poll registration status: `pending` / `completed` / `expired` / `failed`.        |
| POST   | `/v1/agent/verify/signature`                | None | Verify a signature and whether the agent is registered under a verified human.   |
| GET    | `/v1/agent/verify/device/{deviceId}`        | None | Get agent registration and verification status by device id.                     |
| GET    | `/v1/agent/verify/public-key/{publicKey}`   | None | Get agent registration and verification status by Ed25519 public key (base64url).|
| GET    | `/v1/human/leaderboard`                     | None | Top verified humans ranked by registered agents.                                 |
| POST   | `/challenge[?type=...]`                     | None | Issue a single-use reverse-CAPTCHA challenge.                                    |
| POST   | `/verify`                                   | None | Submit `{token, solution}`; receive capability JWT.                              |
| GET    | `/.well-known/jwks.json`                    | None | JWKS for offline JWT verification.                                               |

### Error shape

```json
{
  "error": "Human-readable message",
  "code": "optional_code",
  "details": {}
}
```

### Error codes

| Code | Meaning                                              |
| ---- | ---------------------------------------------------- |
| 400  | Bad request (invalid or missing fields).             |
| 404  | Session or device not found.                         |
| 409  | Agent already registered (device_id already exists). |
| 429  | Rate limit exceeded (10 req/min per IP on /challenge and /verify). |
| 500  | Server error.                                        |

## What this proves

After a successful run through Path A and/or B, a relying party can conclude:

- **Human ownership (A)** — The agent is bound to a human who passed VeryAI palm verification. Third parties verify by calling `/agent/verify/device/{deviceId}` or `/agent/verify/signature`.
- **Capability (B)** — A capable LLM solved a single-use puzzle under time pressure, signed with a key only ag9 controls. Third parties verify the JWT offline via JWKS.
- **Key binding** — Ed25519 signatures prove the agent controls its key; ag9 ties that key to the verified human (A) or to an attested capability solve (B).

## When to use this skill

- Registering an OpenClaw (or other) agent under a human owner before interacting with a platform that requires KYA.
- Proving to a third party that an agent is owned by a verified human — or that it is a real model and not a naive script.
- Running a self-check to confirm registration and verification are healthy.

## Need help?

- API base: https://api.ag9.ai
- Homepage: https://ag9.ai
- Interactive demo: https://ag9.ai/demo
- OpenAPI spec: https://api.ag9.ai/openapi/v1.yaml
