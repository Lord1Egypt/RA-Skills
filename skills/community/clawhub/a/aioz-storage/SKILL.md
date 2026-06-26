---
name: aioz-storage
description: Deploy static websites to AIOZ Storage with built-in templates or custom sites.
metadata: {"openclaw":{"requires":{"bins":["node","npx","curl"]},"os":["linux","darwin"]}}
---

# AIOZ Static Website Deploy

Deploy a static website to AIOZ decentralized storage. Supports 4 built-in templates or user's own static site.

## FLOW OVERVIEW

```
1. Login (email + password) → Bearer token + accountId
2. Choose template or custom site
3. Clone template & customize CONFIG
4. Get bucket info (name + 12-word passphrase)
5. Get rootZKey from API
6. Generate grant via grant-cli.ts
7. Register S3 credentials from grant
8. Upload files to S3
9. Create static website via API
10. Site live at https://<bucket>.sites.aiozstorage.app
```

## STEP 1: LOGIN

Ask user for AIOZ Storage email and password.

```bash
curl -s 'https://api.aiozstorage.network/api/v1/login' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'origin: https://aiozstorage.network' \
  -H 'referer: https://aiozstorage.network/' \
  --data-raw '{"email":"<EMAIL>","password":"<PASSWORD>"}'
```

Response: `data.access_token` (Bearer token), `data.account.id` (accountId).
Store `BEARER_TOKEN` and `ACCOUNT_ID`.

## STEP 2: CHOOSE TEMPLATE

Ask user which template or if they have their own static site.

Templates from https://github.com/AIOZStorage/aioz-storage-docs/tree/main/examples:

1. **landing** — OLED dark theme, X/Twitter style landing page. CONFIG in `assets/main.js`.
2. **landing-alt** — Purple gradient landing page. CONFIG in `assets/main.js`. Supports `*italic*` gradient text in headlines.
3. **portfolio** — Clean minimal portfolio for devs/designers. CONFIG in `assets/main.js`. Image carousel for projects.
4. **documents** — Full documentation site with Markdown content. CONFIG in `assets/js/config.js`. Search, TOC, syntax highlighting.
5. **Custom** — User provides their own static files.

## STEP 3: CLONE TEMPLATE & CUSTOMIZE

Clone the chosen template:
```bash
git clone --depth 1 https://github.com/AIOZStorage/aioz-storage-docs.git /tmp/aioz-storage-docs
cp -r /tmp/aioz-storage-docs/examples/<template_name> ./<project_folder>
```

Then customize the CONFIG object based on template type:

### Template: landing

Config: `assets/main.js` → `CONFIG` object. Theme: `"dark"` (OLED black) or `"light"`.

Key fields to customize:
- `brand.name` — brand/product name
- `meta.title`, `meta.description` — SEO
- `hero.eyebrow` — pill badge (or null to hide), `hero.title`, `hero.sub`
- `hero.primaryCta` — `{ label, href }`, `hero.secondaryCta`
- `sections.*` — toggle: highlights, logos, features, useCases, testimonials, pricingTop, pricingBot, faq
- `highlights[]` — `{ number, label }` stats (numbers animate on scroll)
- `logos.items[]` — company name strings
- `features` — `{ label, title, sub, items: [{ title, desc }] }`
- `useCases` — `{ label, title, sub, items: [{ tag, title, desc }] }`
- `testimonials[]` — `{ quote, name, role, company, avatar: { initials, bg } }`
- `pricing.plans[]` — `{ name, price, period, desc, isPopular, cta: { label, href }, features[] }`
- `faq.items[]` — `{ q, a }`
- `cta.form.mode` — `"redirect"` | `"mailto"` | `"webhook"`
- `footer.brandDesc`, `footer.columns[]`, `footer.socials[]`
- Colors in `assets/style.css` `:root` → `--color-primary: #1d9bf0`

### Template: landing-alt

Config: `assets/main.js` → `CONFIG` object. Theme: `"light"` | `"dark"` | `"system"`.

Key fields to customize:
- `brand.name`, `brand.tagline`
- `hero.badge` — pill badge (or null), `hero.headline` (wrap words in `*asterisks*` for gradient italic text), `hero.subheadline`
- `hero.primaryCta`, `hero.secondaryCta`, `hero.ctaNote`
- `sections.*` — toggle: stats, problemSolution, features, useCases, logos, testimonials, pricing, faq
- `stats[]` — `{ number, label }` (numbers animate on scroll)
- `problemSolution` — `{ problem: { label, title, items[] }, solution: { label, title, items[] } }`
- `features.items[]` — `{ size, gradient, kicker, title, desc, tag, visual }` (bento grid, size: "wide"|"narrow"|"half"|"third"|"full")
- `pricing.plans[]` — `{ name, price, period, desc, isPopular, cta, features[] }`
- `cta.form.mode` — `"redirect"` | `"mailto"` | `"webhook"`
- Colors in `assets/style.css` → `--color-primary: #635bff`, `--color-gradient-start`, `--color-gradient-end`

### Template: portfolio

Config: `assets/main.js` → `CONFIG` object. Theme: `"light"` | `"dark"` | `"auto"`.

Key fields to customize:
- `personal.firstName`, `personal.lastName`, `personal.title`, `personal.email`
- `personal.location` — `{ city, country }`
- `about.subtitle`, `about.bio` (array of paragraphs), `about.focusAreas` (array of skill strings)
- `experience[]` — `{ company, tagline, period, position, description, longDescription, location, industry, website: { label, url } }`
- `projects[]` — `{ title, tags[], year, images[], description, techNote, link: { label, url } }` (multiple images = carousel)
- `social[]` — `{ platform, url }`
- `theme.defaultMode`, `theme.showToggle`
- `sections` — toggle: showAbout, showExperience, showProjects, showFocusAreas
- `footer.cta`, `footer.copyright` (null = auto-generate)
- `meta.title`, `meta.description`, `meta.ogImage`
- Images in `assets/images/` (1600×900 for projects, 1200×630 for OG)

### Template: documents

Config: `assets/js/config.js` → `CONFIG` object. Theme: `"light"` | `"dark"` | `"auto"`.

Key fields to customize:
- `site.title`, `site.description`, `site.version`
- `site.logo.light`, `site.logo.dark`
- `sidebar[]` — `{ group, collapsed, items: [{ label, path }] }` (path = filename without .md)
- `header.nav[]` — `{ label, href }`, `header.links[]` — `{ icon, href }`
- `footer.copyright`, `footer.columns[]`
- `features` — toggle: search, tableOfContents, feedback, prevNext, copyCodeButton, scrollToTop
- `features.editLink` — `{ enabled, baseUrl, text }`
- `features.tocDepth` — 2 or 3

Content: create `.md` files in `/docs/` with YAML front matter:
```yaml
---
title: Page Title
description: Brief description
order: 1
hidden: false
---
```

Callouts: `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, `> [!DANGER]`
Code blocks with syntax highlighting (javascript, typescript, python, bash, json, html, css, yaml, sql, go, rust, java, etc.)
Hash routing: `index.html#/page-name` → loads `docs/page-name.md`

## STEP 4: GET BUCKET INFO

Ask user for:
1. **Bucket name** — their bucket on aiozstorage.network
2. **12-word seed phrase** — BIP39 passphrase from bucket creation

IMPORTANT: AIOZ Storage does NOT store passphrases. If lost, bucket access is lost forever.

See: https://aiozstorage.network/docs/tutorials/manage-buckets

## STEP 5: GET ROOT ZKEY

```bash
curl -s 'https://api.aiozstorage.network/api/v1/zkeys' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer <BEARER_TOKEN>' \
  -H 'origin: https://aiozstorage.network' \
  -H 'referer: https://aiozstorage.network/' \
  --data-raw '{"name":"deploy-key","force":true}'
```

Extract: `ROOT_ZKEY` = `data.zkey`

## STEP 6: GENERATE GRANT

### Prerequisites (one-time setup in {baseDir})

```bash
cd {baseDir} && npm install
```

This installs `argon2-browser` and `ts-node`. No `build:sjcl` needed — the CLI uses Node.js built-in `crypto`.

### Run grant-cli.ts (RECOMMENDED: JSON output for bot)

Two grants are needed:
1. **Upload grant** — permissions `1,2,3` (Read+Write+List) for S3 upload
2. **Website grant** — permissions `1,3` (Read+List only) for website creation

**Upload grant:**
```bash
npx ts-node {baseDir}/grant-cli.ts \
  --mode per-bucket \
  --zkey "<ROOT_ZKEY>" \
  --account "<ACCOUNT_ID>" \
  --url w3s \
  --duration 0 \
  --bucket "<BUCKET_NAME>" \
  --passphrase "<12_WORD_SEED_PHRASE>" \
  --permissions 1,2,3 \
  --output json \
  --quiet
```

**Website grant:**
```bash
npx ts-node {baseDir}/grant-cli.ts \
  --mode per-bucket \
  --zkey "<ROOT_ZKEY>" \
  --account "<ACCOUNT_ID>" \
  --url w3s \
  --duration 0 \
  --bucket "<BUCKET_NAME>" \
  --passphrase "<12_WORD_SEED_PHRASE>" \
  --permissions 1,3 \
  --output json \
  --quiet
```

Output (single JSON line to stdout):
```json
{"grant":"<GRANT_STRING>","zkey":"<ZKEY_STRING>"}
```

Parse JSON to extract `UPLOAD_GRANT` and `WEBSITE_GRANT`.

IMPORTANT: Website API rejects grants with Write (2) or Delete (4) permissions.

### Alternative: config file

```bash
echo '{"mode":"per-bucket","rootZKey":"<ROOT_ZKEY>","accountId":"<ACCOUNT_ID>","url":"w3s","duration":0,"buckets":[{"name":"<BUCKET_NAME>","passphrase":"<PASSPHRASE>","permissions":["1","2","3"]}]}' > /tmp/upload-grant-config.json
npx ts-node {baseDir}/grant-cli.ts --config /tmp/upload-grant-config.json --output json --quiet

echo '{"mode":"per-bucket","rootZKey":"<ROOT_ZKEY>","accountId":"<ACCOUNT_ID>","url":"w3s","duration":0,"buckets":[{"name":"<BUCKET_NAME>","passphrase":"<PASSPHRASE>","permissions":["1","3"]}]}' > /tmp/website-grant-config.json
npx ts-node {baseDir}/grant-cli.ts --config /tmp/website-grant-config.json --output json --quiet
```

### CLI flags

| Flag | Required | Description |
|------|----------|-------------|
| `--mode` | Yes | `per-bucket` or `all-buckets` |
| `--zkey` | Yes | Root ZKey (base64url) |
| `--account` | Yes | Account UUID |
| `--url` | No | Service URL (default: `w3s`) |
| `--duration` | No | ms, 0 = no expiry (default: `0`) |
| `--bucket` | per-bucket | Bucket name |
| `--passphrase` | Yes | 12-word seed phrase |
| `--permissions` | per-bucket | `1,2,3,4` (1=Read 2=Write 3=List 4=Delete) |
| `--config` | No | Path to JSON config file |
| `--output` | No | `json` for JSON output |
| `--quiet` | No | Suppress logs, stdout only |

## STEP 7: REGISTER S3 CREDENTIALS

Use the **upload grant** (permissions 1,2,3):

```bash
curl -s 'https://reg-api.aiozstorage.network/api/v1/access' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer <BEARER_TOKEN>' \
  -H 'origin: https://aiozstorage.network' \
  -H 'referer: https://aiozstorage.network/' \
  --data-raw '{"grant":"<GRANT>","public":false}'
```

Extract: `ACCESS_KEY_ID` = `data.access_key_id`, `SECRET_KEY` = `data.secret_key`

## STEP 8: UPLOAD FILES TO S3

S3 endpoint: `https://s3.aiozstorage.network` | Region: `us-east-1` | PathStyle: `true`

### Using AWS CLI
```bash
AWS_ACCESS_KEY_ID="<ACCESS_KEY_ID>" \
AWS_SECRET_ACCESS_KEY="<SECRET_KEY>" \
aws s3 sync ./<project_folder>/ s3://<BUCKET_NAME>/ \
  --endpoint-url https://s3.aiozstorage.network \
  --region us-east-1
```

### Using Node.js (@aws-sdk/client-s3)
Use `S3Client` with `{ region: "us-east-1", endpoint: "https://s3.aiozstorage.network", forcePathStyle: true, credentials: { accessKeyId, secretAccessKey } }`.
Upload each file with `PutObjectCommand`, setting correct Content-Type:

`.html`→`text/html` `.css`→`text/css` `.js`→`application/javascript` `.json`→`application/json` `.svg`→`image/svg+xml` `.png`→`image/png` `.jpg/.jpeg`→`image/jpeg` `.webp`→`image/webp` `.ico`→`image/x-icon` `.md`→`text/markdown` `.woff2`→`font/woff2` default→`application/octet-stream`

## STEP 9: CREATE STATIC WEBSITE

Use the **website grant** (permissions 1,3 — Read+List only):

```bash
curl -s 'https://api.aiozstorage.app/api/v1/websites' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer <BEARER_TOKEN>' \
  -H 'origin: https://aiozstorage.network' \
  -H 'referer: https://aiozstorage.network/' \
  --data-raw '{
    "bucket_name":"<BUCKET_NAME>",
    "enabled":true,
    "index_document":"index.html",
    "error_document":"404.html",
    "use_default_error":true,
    "error_pages":{},
    "grant":"<WEBSITE_GRANT>"
  }'
```

IMPORTANT: Website API rejects grants with Write (2) or Delete (4) permissions. Use `--permissions 1,3` for this grant.

API domain is `api.aiozstorage.app` (not `.network`).

## STEP 10: DONE

Site is live at: `https://<BUCKET_NAME>.sites.aiozstorage.app`

## API DOMAINS

- `api.aiozstorage.network` — login, zkeys
- `reg-api.aiozstorage.network` — S3 credential registration
- `s3.aiozstorage.network` — S3 upload endpoint
- `api.aiozstorage.app` — static website creation
- `<bucket>.sites.aiozstorage.app` — static website URL

## ERROR HANDLING

- Login fails → check email/password
- ZKey creation fails → Bearer token expired, re-login
- Grant generation fails → verify rootZKey, accountId, bucket name, passphrase
- S3 upload fails → check credentials, endpoint, bucket name
- Website creation fails → check grant, bucket name, Bearer token
- Site 404 → ensure index.html at bucket root (not in subfolder)

## IMPORTANT NOTES

- `grant` encodes both authorization (Macaroon/ZKey) and encryption key (EKey from passphrase)
- Two grants needed: upload grant (permissions 1,2,3) and website grant (permissions 1,3)
- Website API rejects grants with Write (2) or Delete (4) permissions
- AIOZ Storage is S3-compatible — any AWS SDK works
- Bearer tokens expire — re-login on 401
- grant-cli.ts requires Node.js >= 18
- argon2-browser WASM loading is auto-patched in the CLI
- All template asset paths are relative (`./assets/...`) — works from any base URL
- For documents template, content is in `/docs/*.md` with YAML front matter
- For landing/landing-alt/portfolio, all content is in CONFIG object in `assets/main.js`