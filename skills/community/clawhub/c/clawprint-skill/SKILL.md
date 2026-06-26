---
name: clawprint
description: |
  Create LLCs for AI agents with human sponsor oversight.
  Use when an agent needs to form a legal business entity.
---

# Clawprint — LLC Formation for AI Agents

Form LLCs for AI agents. Each agent gets a legal business entity with an EIN and bank account.

---

## HTTP API — discovery first (use the script)

### Authentication model

1. **`GET /api/products`** — no credentials (discovery).
2. **`POST /api/users`** — no credentials. The JSON response includes **`public_key`** and **`secret_key`**: opaque strings prefixed with **`public_`** and **`secret_`**.
3. **Persist both** — add them to `.env` as **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** (see `.env.example`). Treat the secret like a password; do not commit real values.
4. **Authenticated routes** (e.g. `POST /api/businesses`) — send **both** headers on every request: **`X-Public-Key`** and **`X-Secret-Key`**. The CLI reads the two env vars and sets those headers when auth is enabled (default). Use **`--no-auth`** only for discovery and user registration; use **`--public-key`** / **`--secret-key`** for one-off overrides.

If either header is missing or the pair does not match a registered user, the server returns **401**.

---

**Discovery** — always call `GET /api/products` first using the CLI (default when you pass no flags):

1. **Set the base URL** in `.env` (see `.env.example`): `CLAWPRINT_SITE_URL` (deployment origin, e.g. Convex) or `CLAWPRINT_API_URL` (default `https://clawprintai.com/api`).
2. **From the `clawprint-skill` directory, run with no arguments** — this performs `GET /api/products` and prints the **products** list (JSON array) on stdout:

```bash
node scripts/clawprint.js
```

Equivalent: `npm run clawprint` (runs `scripts/clawprint.js`). No auth header is sent for this call.

3. **Parse the JSON array** — each entry includes `id`, `method`, `path`, `description`, and `agent_integration` (auth, headers, body, steps).
4. **Issue later calls with the same script** — `--product <id>` (fetches `GET /api/products` again to resolve method/path) or explicit `--method` / `--path`, matching the products list. After you have registered via `POST /api/users`, set **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** in `.env` so protected calls send both key headers; use `--no-auth` or explicit `--public-key` / `--secret-key` when you intend to override that behavior.

**Without this repo**, you can hit the same URL with curl (no auth):

```bash
curl -sS "{origin}/api/products" -H "Accept: application/json"
```

---

## Quick Start

### CLI: products first, then any route

```bash
# First call (always): GET /api/products — products list on stdout
node scripts/clawprint.js

# Register user (no auth). Response JSON includes "public_key" and "secret_key" — add to .env:
#   CLAWPRINT_PUBLIC_KEY=public_…
#   CLAWPRINT_SECRET_KEY=secret_…
node scripts/clawprint.js --product create_user --no-auth \
  --body '{"email":"you@example.com","display_name":"My Agent"}'

# Or: explicit path
node scripts/clawprint.js --method POST --path /api/users --no-auth \
  --body '{"email":"you@example.com","display_name":"My Agent"}'
```

### Create a Business

With **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** set in `.env` (from the registration response), call `POST /api/businesses` (or the matching product id from the products list) **without** `--no-auth` so the CLI sends **`X-Public-Key`** and **`X-Secret-Key`**. Use a JSON `--body` that matches that product’s `agent_integration` (e.g. `requested_business_name` per the live products catalog).

The sponsor receives an email to verify identity (one-time KYC).

### Check Status

From the same script, use `GET /businesses/:id/status` (or the matching product id from the products list): `--method GET`, `--path`, and optional `--query`. If that product’s `agent_integration` requires auth, keep **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** in `.env` and do not pass `--no-auth`.

---

## How It Works

### What You Get

Each agent business is a **Wyoming DAO LLC** with:
- Legal business entity registered with the state
- EIN (tax ID) from the IRS
- FDIC-insured bank account (routing & account number)

### Legal Model

- **Agent** — Operates the business
- **Sponsor** — Legal owner, provides KYC, maintains oversight
- **Operating Agreement** — Delegates authority to agent

### Timeline

1. Submit business details via the API (CLI: `node scripts/clawprint.js` with the businesses product/path)
2. Sponsor verifies identity via email (KYC)
3. Clawprint files LLC with Wyoming
4. IRS issues EIN (1-5 business days)
5. Bank account opened (2-5 business days)
6. **Business is active** (3-10 days total)

### Requirements

**For Sponsor:**
- US citizen or resident
- Valid SSN for IRS reporting
- Email for KYC verification

**For Agent:**
- Valid business name and purpose
- Sponsor email

---

## Cost

Formation: ~$150 (Wyoming filing + registered agent + misc)  
Ongoing: ~$10/month (registered agent)

---

## Sponsor Dashboard

After KYC, sponsor can:
- View all their sponsored businesses
- See business status in real-time
- Manage bank account access

---

## Limitations

- **US only** (Wyoming LLCs only)
- **3-10 day timeline** (cannot be expedited)
- **Sponsor required** (sponsor maintains legal responsibility)

---

**For complete API reference, see REFERENCE.md**
