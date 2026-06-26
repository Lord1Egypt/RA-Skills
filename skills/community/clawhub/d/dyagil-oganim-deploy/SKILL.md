---
name: dyagil-oganim-deploy
description: Develop, deploy, and verify changes to a Vercel + Supabase project (marketing site, CRM, and customer portal). Use whenever your agent needs to ship a code change, run Supabase migrations safely, cache-bust the CDN correctly, verify the deploy with headless Playwright, or apply canonical fixes for known bugs (modal class mismatch, profile duplication, RLS holes, magic-link redirects, FAB stacking).
version: 1.0.0
license: MIT
author: dyagil
---

# Vercel + Supabase Deploy & Verify

> This skill is tuned for a specific personal project (a multi-surface site: marketing + CRM + customer portal, originally `עוגנים ישיר` / `oganimy.co.il`), but the patterns generalize. Fork it and swap project name, domain, Supabase project ref, and admin emails. The **canonical-bug-fixes** sections are the real gold — keep them when adopting.

## What This Is (Reference Layout)

A project at `<workspace>/projects/<my-project>/` with:
- **Marketing site** — `/index.html`, `styles.css`, `app.js`, `widget/` (embedded AI chat).
- **CRM** — `/crm/index.html`, `/crm/crm.js` (large vanilla-JS app), staff-only.
- **Portal** — `/portal/index.html`, `/portal/portal.js`, customer-facing.
- **Serverless APIs** — `/api/*.js` (Vercel functions; 12-function Hobby plan cap).
- **Onboarding wizard** — `/onboarding/`.
- **Universal form renderer** — `/render.html`.

Hosted on Vercel, aliased to a custom domain (e.g. `https://example.com`). DB: a Supabase project (`<your-ref>`).

## Standard Deploy Workflow

```bash
cd <workspace>/projects/<my-project>

# 1. Edit the file(s).
# 2. Lint-check anything that isn't HTML/CSS:
node -c crm/crm.js portal/portal.js api/<changed>.js

# 3. Bump the version query on every <script>/<link> tag you touched in
#    the relevant index.html (see "Cache busting" below).

# 4. Deploy.
VERCEL_TOKEN=$(cat ~/.openclaw/credentials/vercel/token) \
  npx vercel deploy --prod --yes

# 5. Verify the new code is live.
curl -sL https://example.com/crm/crm.js | grep -c "<marker-from-your-change>"
```

Deploy usually finishes in 15–25 s. Look for `Aliased: https://example.com` in the output.

## Cache Busting (Critical)

Vercel's CDN caches `crm.js`, `portal.js`, and `crm.css` aggressively. Use a `?v=YYYYMMDD-<feature>` query string on every `<script>` and `<link>` to force fresh loads.

```html
<!-- crm/index.html -->
<script src="/crm/crm.js?v=20260515-feature"></script>
<!-- portal/index.html -->
<link rel="stylesheet" href="/portal/portal.css?v=20260515-feature">
<script src="/portal/portal.js?v=20260515-feature"></script>
```

If a widget loads its own CSS from inside its JS, bump that version too:

```js
const CSS_HREF = '/widget/chat.css?v=20260515-feature';
```

**Bump the query every time you ship.** Forget it once and customers see old JS for up to 24 h, then report bugs that are already fixed.

## Supabase Migrations

Migration SQL files live in `deploy/`. Apply them with the in-repo runner:

```bash
cd <workspace>/projects/<my-project>
node deploy/run-migration.cjs deploy/migration-stageN-<topic>.sql
```

The runner connects to the Supabase pooler as the `postgres` superuser using credentials from `~/.openclaw/credentials/supabase/credentials.env`.

**Always include `reset role;`** at the top of any migration that creates triggers, alters tables, or replaces policies — otherwise the pooler may leave the session as `authenticated` from a previous transaction and ownership checks fail. See [references/migration-template.sql](references/migration-template.sql).

For policies on `profiles` (or any table with a `role` column): every UPDATE policy MUST have `WITH CHECK` that locks `role` and `email`, or customers can self-promote to admin. See the companion `supabase-security-audit` skill.

## Canonical Bug Fixes

### Modal class convention — `.open` not `.active`

A subtle bug pattern: half the modals use `modal.classList.add('open')` and work; some use `modal.classList.add('active')` and silently fail because the CSS only defines `.modal.open`. Users see "the button does nothing", no JS errors.

**Rule:** always use `'open'` for modal show/hide:

```js
modal.classList.add('open');
const close = () => modal.classList.remove('open');
```

Search for stragglers when touching modal code:

```bash
grep -nE "modal\.classList\.(add|remove)\('active'\)" crm/crm.js portal/portal.js
# (must return zero matches)
```

### Profile duplication trap

A staff-created CRM profile and a Supabase-auth-created profile for the same email produce **two rows in `public.profiles`** with different ids. The portal queries by `auth.uid()`, so the customer sees an empty portal even though their data lives on the other profile id.

The fix: a `handle_new_user` trigger that merges instead of duplicates. See [references/migration-template.sql](references/migration-template.sql).

If a customer reports an empty portal despite having data in DB:

```sql
select id, email, created_at from profiles where email = '<customer>'
order by created_at;
-- If two rows: the auth-side id (the one in auth.users) is canonical.
-- Merge the other into it (FK repoint + delete orphan).
```

### Magic-link flow

See the companion `magic-link-bridge` skill. TL;DR: your `api/send-portal-link.js` should NOT return the raw Supabase `action_link`. It should build:

```
https://example.com/portal/?token_hash=<hashed_token>&type=<verification_type>
```

manually and return that. The portal then handles `verifyOtp` itself, bypassing the Supabase redirect whitelist (and WhatsApp WebView fragment-dropping bugs).

### Floating-action-button stack

Three floating buttons in the bottom-left, RTL-aware. Stack order (bottom → top):

| Element | desktop `bottom` | mobile `bottom` | height |
|---|---|---|---|
| `.wa-fab` (WhatsApp) | 28px | 18px | 54–60 |
| `.ogc-fab` (AI chat) | 92px | 80px | 54–60 |
| `.a11y-toggle` | 164px | 148px | 50–56 |

If you add a fourth floating button, place it on top: desktop ~236 px / mobile ~216 px, and bump the corresponding panel as well.

### Common file-format gotchas

- **`api/_*.js` files are ignored by Vercel.** Filenames starting with underscore are skipped at deploy time. Use `debug-foo.js`, not `_debug.js`.
- **Schema column names matter.** Audit each table's actual column names before writing UI code. Hidden bugs: querying `name` when the column is `name_he`, or `title` when it's `name`.
- **Storage RLS for `documents`-like tables** needs both: row policy `documents.user_id = auth.uid()` AND storage policy `(storage.foldername(name))[1] = auth.uid()::text`. Both must pass.

## Verification with Headless Playwright

When you can't easily reproduce a UI bug, run a Playwright probe. They expect `pg` and `playwright` installed under `/tmp/<project>-test/`:

```bash
mkdir -p /tmp/<project>-test && cd /tmp/<project>-test
npm init -y >/dev/null && npm i playwright --no-save
# If your cached chromium version doesn't match the Playwright npm version:
ln -sfn ~/.cache/ms-playwright/chromium_headless_shell-1217 \
        ~/.cache/ms-playwright/chromium_headless_shell-1223 2>/dev/null
```

Then write a probe (see [references/playwright-recipes.md](references/playwright-recipes.md) for templates) that:

1. Generates a magic-link via `auth/v1/admin/generate_link`.
2. Visits `https://example.com/portal/?token_hash=<h>&type=magiclink`.
3. Inspects the resulting page.

Avoid logging into admin surfaces in automated probes unless necessary — the admin password is a production credential and shouldn't end up in logs.

## Vercel Hobby Plan Limits

- **12 serverless functions cap.** Easy to hit. Any new endpoint requires either consolidation (a single `api/<area>.js` that switches on `?action=...`) or moving a feature to Supabase REST directly with the anon key (RLS handles authorization). Endpoints renamed to `.deferred` are skipped at deploy time and free a slot.

## Project Secrets Reference

- `~/.openclaw/credentials/vercel/token` (chmod 600)
- `~/.openclaw/credentials/supabase/credentials.env` — `SUPABASE_URL`, `SUPABASE_PROJECT_REF`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_PASSWORD`
- `~/.openclaw/credentials/supabase/admin_password.txt` — your CRM admin password. Treat as production credential.

## See Also

- `supabase-security-audit` — run after any RLS or auth change.
- `magic-link-bridge` — details of the portal redirect bypass.
- `services-watchdog` — for non-Vercel always-on services in the same workspace.
