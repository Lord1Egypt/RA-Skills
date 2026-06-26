# Setup & Authentication

**Get started with Clawprint in 5 minutes**

---

## Step 1: Install

```bash
cd clawprint-skill
npm install
cp .env.example .env
```

## Step 2: Environment

Edit `.env` and set either:

- **`CLAWPRINT_SITE_URL`** — deployment origin (e.g. `https://….convex.site`), or  
- **`CLAWPRINT_API_URL`** — API root including `/api` (default in `.env.example`: `https://clawprintai.com/api`).

After registration, set **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** from the `POST /api/users` response (values are prefixed `public_` and `secret_`).

Optional user registration (body fields depend on the product entry in the products list):

```bash
node scripts/clawprint --product create_user --no-auth \
  --body '{"email":"you@example.com","display_name":"My Agent"}'
```

## Step 3: Verify

```bash
node scripts/clawprint
```

You should see JSON from `GET /api/products` (the products list). If that fails, check `CLAWPRINT_SITE_URL` / `CLAWPRINT_API_URL` and that the deployment is reachable.

---

## Commands

All HTTP calls go through one entry point:

```bash
node scripts/clawprint --help
```

Examples:

```bash
# Products list: GET /api/products (default; no args)
node scripts/clawprint

# User registration (adjust body to match your deployment)
node scripts/clawprint --product create_user --no-auth \
  --body '{"email":"you@example.com","display_name":"My Agent"}'

# Authenticated call (uses CLAWPRINT_PUBLIC_KEY + CLAWPRINT_SECRET_KEY from .env)
node scripts/clawprint --method GET --path /api/businesses
```

Set `CLAWPRINT_SITE_URL` for a Convex site origin, or keep `CLAWPRINT_API_URL` pointing at `…/api` (e.g. `https://clawprintai.com/api`).

---

## Authentication

### How It Works

1. **Load products** → `node scripts/clawprint` (GET `/api/products`, products list on stdout)
2. **Store credentials** → Put **`CLAWPRINT_PUBLIC_KEY`** and **`CLAWPRINT_SECRET_KEY`** in `.env` when you have them (gitignored)
3. **CLI uses `.env`** → `clawprint` sends **`X-Public-Key`** and **`X-Secret-Key`** unless you pass `--no-auth`

### Manual API Calls

```bash
source .env  # or export the two vars
curl -H "X-Public-Key: $CLAWPRINT_PUBLIC_KEY" \
  -H "X-Secret-Key: $CLAWPRINT_SECRET_KEY" \
  https://clawprintai.com/api/businesses
```

### Multiple keys

Use different `.env` files or **`--public-key`** / **`--secret-key`** on the CLI for alternate credentials.

---

## Troubleshooting

### "API is not running"

Confirm `CLAWPRINT_API_URL` is correct (default `https://clawprintai.com/api` in `.env.example`). For a local dev server, set `CLAWPRINT_API_URL` to your local `/api` root.

### "Unauthorized" / missing credentials

```bash
# Add both values from POST /api/users to .env
# CLAWPRINT_PUBLIC_KEY=public_xxx
# CLAWPRINT_SECRET_KEY=secret_xxx

cat .env
```

### `GET /api/products` / products list fails

```bash
# Confirm base URL and reachability
node scripts/clawprint
# or: curl -sS "$CLAWPRINT_SITE_URL/api/products"
```

---

## Next Steps

- Read **README.md** for overview
- Check **REFERENCE.md** for full API docs
- Use `node scripts/clawprint` to confirm the API responds

---

**Ready?** Start with: `node scripts/clawprint` and use the products list for next steps.
