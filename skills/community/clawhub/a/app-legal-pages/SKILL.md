---
name: app-legal-pages
description: Generate and deploy app Privacy Policy and Terms of Service static websites from an app feature document. Use when a user provides app requirements/feature docs and wants production-ready legal pages published via GitHub + Cloudflare Pages, including draft generation, consistency checks, and deployment-ready output URLs.
---

# App Legal Pages

Generate a complete legal mini-site for an app:

- `index.html` (legal home)
- `privacy.html` (Privacy Policy)
- `terms.html` (Terms of Service)
- `styles.css` (shared styles)

## Workflow

1. Collect required legal/product inputs.
2. Generate draft legal pages from feature documentation.
3. Run strict consistency checker.
4. Present generated pages for user review/approval.
5. Check Cloudflare deployment auth readiness.
6. Ask user to complete auth if missing.
7. Auto-deploy to Cloudflare Pages after explicit confirmation.
8. Return final public URLs.

## 1) Collect Inputs

Collect or confirm:

- App name
- Company/entity name (or individual publisher name)
- Contact email
- Governing law jurisdiction (country/region, optional; only if explicitly provided)
- Effective date
- App feature document (markdown/text)
- Data behavior details:
  - Analytics events
  - Crash/error logs
  - Identifiers (device/user IDs)
  - Third-party SDKs/services
  - Permissions used (camera/location/photos/mic/contacts/tracking/notifications)

If facts are unknown, pause and ask for missing inputs before generation. Do not output placeholder markers (no TODO/TEMP strings in final pages).
Never assume jurisdiction, region, analytics/tracking, sharing, or permission usage unless explicitly stated in the input document or user prompt.
Generate policy clauses from explicit product claims first (e.g., offline-only, no cloud, no tracking, no analytics), and avoid introducing contradictory generic legal boilerplate.

## 2) Generate Draft Site

Run:

```bash
python3 scripts/generate_legal_site.py \
  --input /path/to/app-feature.md \
  --out ./out/legal-site \
  --app-name "Your App" \
  --company "Your Company" \
  --base-email "chentuan7963@gmail.com" \
  --email-tag "quillnest" \
  --effective-date "2026-03-03" \
  --jurisdiction "California, United States"
```

Email rule:
- Prefer plus-address derivation from GitHub/base email + app tag.
- Example: `chentuan7963@gmail.com` + `quillnest` => `chentuan7963+quillnest@gmail.com`.
- Use `--email` only when you explicitly want a fixed address.

Language rule:
- Generate English-only legal pages by default.
- Exclude non-English feature bullets from Feature Context to keep language consistent.

The script auto-detects likely data categories/permissions from the feature text. Manually review and adjust output if app behavior is more specific than heuristic detection.

## 3) Run Strict Consistency Checker

Run before publishing:

```bash
python3 scripts/check_consistency.py \
  --feature /path/to/app-feature.md \
  --privacy ./out/legal-site/privacy.html \
  --terms ./out/legal-site/terms.html
```

The checker fails on:
- Placeholder tokens (TODO/TEMP/FIXME)
- Contradictions against explicit product claims (offline/no-cloud/no-tracking/no-analytics)
- EXIF mention in feature doc without corresponding privacy disclosure
- Governing-law section in Terms when jurisdiction is not explicitly provided

## 4) Validate Draft Quality

Check before publishing:

- `privacy.html` and `terms.html` both exist.
- App/company/email/effective date are consistent across pages.
- Privacy disclosures match only explicitly stated permissions and data behavior (no inferred tracking/region claims).
- User rights and contact/deletion request path are present.
- No unverifiable legal claims.
- Final pages contain no placeholder markers (forbidden: TODO/TEMP/FIXME).

If the app uses sensitive permissions or SDKs, verify these are explicitly disclosed in Privacy Policy.

## 5) Review Gate (Mandatory)

Before deployment, share generated files with the user and ask for explicit approval to deploy.
Do not deploy automatically without user confirmation.

## 6) Check Deployment Auth

Run auth readiness check:

```bash
python3 scripts/deploy_cloudflare_pages.py --check-auth --site-dir ./out/legal-site --project-name your-project-name --production-branch main
```

Auth is valid when either:
- `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` are set, or
- `wrangler whoami` succeeds.

If auth is missing, ask the user to authenticate:

```bash
wrangler login
```

## 7) Auto-Deploy to Cloudflare Pages

After explicit approval + auth ready:

```bash
python3 scripts/deploy_cloudflare_pages.py \
  --site-dir ./out/legal-site \
  --project-name your-project-name \
  --production-branch main
```

Or use one-shot pipeline:

```bash
python3 scripts/run_pipeline.py \
  --feature /path/to/app-feature.md \
  --out ./out/legal-site \
  --app-name "Your App" \
  --company "Your Company" \
  --base-email "you@gmail.com" \
  --email-tag "yourapp" \
  --effective-date "2026-03-05" \
  --project-name your-project-name \
  --production-branch main \
  --confirm-deploy
```

## 8) Returnables

Return:

- Cloudflare Pages site URL
- Privacy Policy URL (`<site>/privacy.html`)
- Terms of Service URL (`<site>/terms.html`)
- Auth mode used (`api-token` or `wrangler-login`)

## Guardrails

- Do not claim legal compliance guarantees.
- Keep wording plain and readable.
- Keep deterministic page structure for easy future edits.
- Recommend human legal review before production app-store submission.
