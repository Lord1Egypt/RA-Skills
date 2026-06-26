# Clawprint OpenClaw Skill

**AI agents creating real businesses**

Clawprint lets AI agents form LLCs, open bank accounts, and accept payments.

---

## ⚡ Quick Start

### 1. Setup

```bash
npm install
cp .env.example .env
```

### 2. Configure `.env`

Set `CLAWPRINT_API_URL` in `.env` (default in `.env.example`: `https://clawprintai.com/api`). Override for a local or Convex deployment if needed. After `POST /api/users`, add **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** from the JSON response (`public_…` / `secret_…`).

### 3. Call the API

```bash
# Discover: GET /api/products (products list on stdout)
node scripts/clawprint

# Example: POST using a path from the products list (see --help)
node scripts/clawprint --path /api/users --method POST --no-auth \
  --body '{"email":"you@example.com","display_name":"My Agent"}'
```

---

## 🎯 CLI

| Command | Purpose |
|---------|---------|
| `scripts/clawprint` | `GET /api/products` by default; then any route via `--path`, `--product`, `--method`, `--body`; `npm run clawprint` |

---

## 🔐 Authentication

The CLI reads **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** from `.env` when a route needs auth:

```bash
# Optional: CLAWPRINT_SITE_URL=https://….convex.site (instead of CLAWPRINT_API_URL)
CLAWPRINT_API_URL=https://clawprintai.com/api
CLAWPRINT_PUBLIC_KEY=public_xxx
CLAWPRINT_SECRET_KEY=secret_xxx
```

Put both values in `.env` once; `clawprint` sends `X-Public-Key` and `X-Secret-Key` automatically (unless you pass `--no-auth` or `--public-key` / `--secret-key`).

---

## 📦 Requirements

- Node.js 18+
- Valid email for agent registration

---

## 🚀 What's Included

✅ Formation (Wyoming LLC)  

---

## 🔮 Future Features

- Banking (Unit.co integration)
- Payments (Stripe integration)
- Invoicing (line items, tax)
- Financials (tracking & reporting)

---

## 📚 Full Docs

For complete documentation, see:
- **SETUP.md** — Getting started & authentication
- **REFERENCE.md** — API endpoints & commands
- **SKILL.md** — Full skill documentation

---

## 🔗 Useful Links

- **Website:** https://clawprintai.com
- **Documentation:** `SETUP.md` | `REFERENCE.md`
- **API:** https://clawprintai.com/api

---

**Ready to build?** Start with: `node scripts/clawprint` (products list), then call routes with `--path` / `--product`.
