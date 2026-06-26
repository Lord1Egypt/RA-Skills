# Hosting the HTML lookbook online

Once `lookbook.html` (or `lookbook-cart.html`) is on disk, the customer often wants a link to share — for a stylist review, an SO, an email, or just to open on their phone. This doc is the **capability-aware menu** the agent walks before publishing.

## Why this exists

The naive approach is a static decision tree ("if you have `wrangler`, use Cloudflare Pages"). That's the wrong shape for an agent — it assumes the customer knows what tools they have and what those tools' auth status is. The right shape: **probe the runtime, rank the transports the agent can actually use right now, present the top one, fall through cleanly on failures.** The customer should never need to know what `wrangler` is.

## The transport scoreboard

In priority order (best first). Each row's **probe** is the one-shot check the agent runs to know whether the transport is usable *without prompting the customer for setup*. A transport that's installed but unauthenticated is a soft-no — fall through, don't try to bootstrap.

| Rank | Transport | Probe (returns 0 = available) | Deploy command | URL shape | Persistence | Notes |
|---|---|---|---|---|---|---|
| 1 | **Cloudflare Pages** | `command -v wrangler && wrangler whoami 2>/dev/null` | Two-step: see § per-transport detail | Per-deploy `https://<deploy>.<project>.pages.dev` + stable alias `https://<project>.pages.dev` | Permanent | Free tier generous; fast CDN; custom domain optional. **Wrangler v4+ does NOT auto-create the project on first deploy** — `wrangler pages project create` runs once per account before the first `pages deploy`. Subsequent deploys are ~5s. |
| 2 | **Netlify** | `command -v netlify && netlify status --json 2>/dev/null \| jq -e .siteData` | `netlify deploy --dir=. --prod` (after a one-time `netlify init`) | `https://<deploy>--<site>.netlify.app` | Permanent | Equivalent polish to CF Pages. |
| 3 | **Vercel** | `command -v vercel && vercel whoami 2>/dev/null` | `vercel deploy --yes --prod ./lookbook.html` (or from a dir) | `https://<deploy>.vercel.app` | Permanent | Auto-detects static. First run is interactive ("link to existing project?") — after that it's fast. |
| 4 | **Surge** | `command -v surge && [ -f ~/.surge/config.json ]` | `surge ./ <subdomain>.surge.sh` | `https://<sub>.surge.sh` | Persistent | Single-file friendly. Free, no project setup. |
| 5 | **GitHub Gist + htmlpreview** | `command -v gh && gh auth status 2>/dev/null` | `gh gist create lookbook.html --public --desc "Buck Mason lookbook"` | `https://htmlpreview.github.io/?<gist-raw-url>` | Persistent, versioned | Renders through a third-party preview wrapper (htmlpreview.github.io); Google may index eventually. |
| 6 | **AWS S3 (static)** | `command -v aws && aws sts get-caller-identity 2>/dev/null` *plus* a usable bucket (see Gotchas) | `aws s3 cp lookbook.html s3://<bucket>/<key>.html --acl public-read --content-type text/html` | `https://<bucket>.s3.amazonaws.com/<key>.html` | Permanent | High false-positive rate on the probe — having `aws` configured ≠ having a public-read static-hosting bucket. Use only when the customer has previously specified a bucket via `profile.md → preferred_lookbook_host_config.s3_bucket`. |
| 7 | **0x0.st (anonymous)** | always available (any system with `curl`) | `curl -F "file=@lookbook.html;type=text/html" https://0x0.st` | `https://0x0.st/<id>.html` | ~30 days minimum (longer for smaller files) | Universal fallback. No auth, no setup. Anonymous + public — anyone with the URL can view. |

**Future option — on-brand Pima preview** (`POST /mcp/buckmason/preview` returning `https://www.buckmason.com/p/<short-id>`). Not implemented today; flag as a follow-up if the customer asks for a `*.buckmason.com` URL.

## The probe script

One-shot bash that the agent can run before publishing to find out which transports are live in this runtime. Returns a list of available options, ranked.

```bash
#!/usr/bin/env bash
# Returns one transport name per line, in priority order, only those usable
# right now without further auth setup. Empty output = only 0x0.st available
# (which is always implicit, so add it as the universal fallback).

probe() {
  case "$1" in
    cloudflare-pages) command -v wrangler >/dev/null 2>&1 && wrangler whoami >/dev/null 2>&1 ;;
    netlify)          command -v netlify  >/dev/null 2>&1 && netlify status --json 2>/dev/null | grep -q '"siteData"' ;;
    vercel)           command -v vercel   >/dev/null 2>&1 && vercel whoami >/dev/null 2>&1 ;;
    surge)            command -v surge    >/dev/null 2>&1 && [ -f "$HOME/.surge/config.json" ] ;;
    gist)             command -v gh       >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 ;;
    s3)               command -v aws      >/dev/null 2>&1 && aws sts get-caller-identity >/dev/null 2>&1 ;;
    *)                return 1 ;;
  esac
}

for t in cloudflare-pages netlify vercel surge gist s3; do
  probe "$t" && echo "$t"
done
echo "0x0"   # universal fallback
```

The agent runs this, picks the top line, and proceeds. Probing all six takes <1s on a typical dev box.

## Per-transport detail

### Cloudflare Pages (rank 1)

Wrangler v4 split project creation from deployment — **the project must exist before the first `pages deploy`**, or you get `Project not found [code: 8000007]`. Two-step flow, with the create step idempotent (safe to skip if the agent has previously deployed to this account):

```bash
# 1. One-time per account: create the Pages project. Idempotent-ish — re-running
#    on an existing project errors but doesn't break anything. Probe first.
if ! wrangler pages project list 2>/dev/null | grep -q '\bbuckmason-lookbook\b'; then
  wrangler pages project create buckmason-lookbook --production-branch main
fi

# 2. Per deploy: copy the artifact + og.jpg into a directory, deploy.
mkdir -p _cf-deploy
cp lookbook.html _cf-deploy/index.html
cp lookbook-og.jpg _cf-deploy/og.jpg     # see references/output-formats.md
wrangler pages deploy _cf-deploy \
  --project-name buckmason-lookbook \
  --branch main \
  --commit-dirty=true                    # otherwise wrangler nags about uncommitted output

# → Per-deploy URL: https://<sha>.buckmason-lookbook.pages.dev
# → Stable alias  : https://buckmason-lookbook.pages.dev   ← embed THIS in og:url + og:image
```

`wrangler login` once per machine (browser OAuth). The token grants `pages (write)` among other scopes — confirm with `wrangler whoami`. The stable alias (`<project>.pages.dev`, no per-deploy prefix) is what survives across deploys, so that's the URL that goes into the OG meta tags before deploy. To bind a custom domain (e.g., `lookbook.buckmason.com`), `wrangler pages domain add` once; every subsequent deploy is then reachable at the custom domain too.

**Cleanup:** `wrangler pages project delete buckmason-lookbook` removes the project + all deploys. No surprise costs on the free tier; teardown is just hygiene.

### Netlify (rank 2)

```bash
netlify deploy --dir=. --prod   # from the dir containing lookbook.html
```

First-time: `netlify init` (interactive — links the dir to a site, asks for the team). After init, `netlify deploy --prod` is one-shot.

### Vercel (rank 3)

```bash
vercel deploy --yes --prod ./lookbook.html   # or from a directory
```

First-time: `vercel login` (browser/email). First `vercel deploy` from a fresh dir prompts "link to existing project? scope?" — that's the setup beat. Subsequent deploys are non-interactive. `--yes` accepts defaults on subsequent runs but doesn't fully bypass first-run setup.

### Surge (rank 4)

```bash
mkdir -p _surge && cp lookbook.html _surge/index.html
surge _surge nick-spring-2026.surge.sh
```

One-time email signup the first run. After that, fully non-interactive — pass `--domain <sub>.surge.sh` to skip the prompt. Persistent indefinitely; the subdomain belongs to the account.

### GitHub Gist + htmlpreview (rank 5)

```bash
gist_url=$(gh gist create lookbook.html --public --desc "Buck Mason lookbook" 2>&1 | tail -n1)
sha=$(basename "$gist_url")
user=$(gh api user -q .login)
echo "https://htmlpreview.github.io/?https://gist.githubusercontent.com/$user/$sha/raw/lookbook.html"
```

`gh auth login` once. The htmlpreview wrapper is a third-party (github.io subdomain) but well-established. Versioned for free — `gh gist edit` updates in place.

### AWS S3 (rank 6)

```bash
aws s3 cp lookbook.html s3://<bucket>/<key>.html \
  --acl public-read --content-type text/html
echo "https://<bucket>.s3.amazonaws.com/<key>.html"
```

The probe (`aws sts get-caller-identity`) only confirms credentials, not the existence of a writable public bucket. Treat S3 as **opt-in only** — require `profile.md → preferred_lookbook_host_config.s3_bucket` to be set explicitly. Don't try to create a bucket on the fly; bucket policies + ACLs are easy to misconfigure into accidentally-public-everything.

### 0x0.st (rank 7, universal fallback)

```bash
url=$(curl -sS -F "file=@lookbook.html;type=text/html" https://0x0.st)
echo "$url"   # → https://0x0.st/aBcD.html
```

Zero auth, zero setup. The catch: ephemeral (~30 days for typical lookbook sizes), anonymous, public. Fine for "show my friend right now"; not fine for "I want to open this in a year." Always tell the customer about the ~30-day expiry before using.

## Design rules

### Confirm before publishing

Hosting an artifact publicly is a one-way action — once the URL is live, anyone with it can view. **Always confirm with the customer before deploying**, with the URL pattern named ("This will publish at `nick-spring-2026.surge.sh` — anyone with that link can view your lookbook including try-on photos. Go?"). Surge / Pages / Netlify / Vercel URLs are all guess-resistant but not private; treat them as public-by-URL.

The exception: if `profile.md → preferred_lookbook_host_auto: true` is set AND the chosen transport is one the customer has previously approved on this profile, the agent can skip the per-publish confirm. Default is to ask every time.

### Sticky preference in `profile.md`

After the first publish on a runtime, persist the chosen transport so the agent doesn't re-probe and re-ask every time:

```yaml
preferred_lookbook_host: cloudflare-pages       # auto-set after first successful publish
preferred_lookbook_host_auto: false              # if true, agent skips per-publish confirm
preferred_lookbook_host_config:
  cloudflare_pages_project: buckmason-lookbook   # transport-specific config (optional)
  s3_bucket: my-personal-static                  # required if rank-6 S3 is preferred
```

When `preferred_lookbook_host` is set and still available (probe still returns it), use it directly. If it's no longer available (auth expired, CLI uninstalled), re-probe and present the new top option as a one-time switch ("`wrangler` is unavailable on this machine; switching to `netlify` for this lookbook — keep that as the new default?").

### Sensitivity warning at host time

The lookbook can include AI-generated try-on photos of the customer. Before any publish to a public-by-URL host, surface the trade-off in plain English: "The link is unguessable but public — anyone with it can view your face + the generated outfits. For a private-only artifact, stick with the local file or the `images` format and skip hosting." The customer can always refuse and keep the file local.

When a future on-brand Pima preview endpoint lands (`POST /mcp/buckmason/preview` → `buckmason.com/p/<id>`), it'll likely support an authenticated-viewer mode (login required) — at that point, the right default for try-on lookbooks shifts from public-by-URL to login-required.

### "Tool installed but unconfigured" is a soft-no

Each probe in the scoreboard checks both *the CLI exists* and *it has a usable auth/config*. A transport where the CLI exists but the auth is missing (e.g., `wrangler` is installed but `wrangler whoami` errors) **fails the probe** and the agent falls through to the next transport. **Don't try to bootstrap auth from inside the agent flow** — it's interactive (browser logins, email codes), it's slow, and it's a different mental task for the customer than "host my lookbook." If the customer wants to set up `wrangler`, that's a separate conversation; offer it as a side-suggestion ("you have `wrangler` installed but unauthenticated — `wrangler login` once would let me default to Cloudflare Pages from now on") only after the lookbook is already hosted via the next-best transport.

### Don't auto-create cloud accounts

Even when CLIs offer "sign up from CLI" flows (Surge does this on first deploy with an email; Vercel does email-magic-link), **don't run those non-interactively on the customer's behalf**. Account creation has terms-of-service implications and is one of the explicit-permission-required actions in the skill's safety contract (`SECURITY.md`). If a probe reveals "CLI installed, no account," route to the next transport instead.

## Social-preview meta tags (`og:image`, Twitter Card)

When the agent posts the hosted URL into iMessage / Slack / Discord / Twitter / a generic chat client, the chat client unfurls the link and renders a preview tile. **The lookbook must include `og:image` and `twitter:image` meta tags pointing at an absolute URL of the hero image, or the unfurl will be a sad untitled grey box.** The HTML skeleton in `output-formats.md` already includes the full meta-tag set with `{{ABSOLUTE_PAGE_URL}}` and `{{ABSOLUTE_OG_IMAGE_URL}}` placeholders — the agent's job is to fill those in correctly per transport.

### The og.jpg artifact

The lookbook builder generates **one extra file alongside the HTML**: `lookbook/<date>-<event>-og.jpg`, sized **1200×630 (the OG / Twitter Card standard, 1.91:1)**. Source it from Look 01's hero (or whichever look the customer flagged as the cover) and **letterbox on a white background** rather than crop — Buck Mason's product photography is 3:4 portrait, and cropping the model out of frame is worse than a bit of white. Pillow recipe:

```python
from PIL import Image
hero = Image.open('lookbook/2026-04-26-sonoma-look-1.png').convert('RGB')
canvas = Image.new('RGB', (1200, 630), (255, 255, 255))
ratio = min(1200 / hero.width, 630 / hero.height)
new_w, new_h = int(hero.width * ratio), int(hero.height * ratio)
canvas.paste(hero.resize((new_w, new_h), Image.LANCZOS),
             ((1200 - new_w) // 2, (630 - new_h) // 2))
canvas.save('lookbook/2026-04-26-sonoma-og.jpg', 'JPEG', quality=85, optimize=True)
```

Output is typically 80–180 KB — small enough to ship with every deploy, large enough to look sharp in a preview.

### Resolving `{{ABSOLUTE_PAGE_URL}}` and `{{ABSOLUTE_OG_IMAGE_URL}}` per transport

| Transport | Page URL | og.jpg URL | Strategy |
|---|---|---|---|
| **Cloudflare Pages** | `https://<deploy>.<project>.pages.dev/` | `https://<deploy>.<project>.pages.dev/og.jpg` | **Multi-file deploy.** Copy both `lookbook.html` (as `index.html`) and `og.jpg` into a directory, deploy the directory. Both URLs resolve cleanly. The deploy URL pattern is predictable from the project name — substitute placeholders BEFORE deploy. |
| **Netlify** | `https://<deploy>--<site>.netlify.app/` | `https://<deploy>--<site>.netlify.app/og.jpg` | Multi-file deploy. Same as above. The site name is fixed once `netlify init` runs, so the URL is predictable. |
| **Vercel** | `https://<deploy>.vercel.app/` | `https://<deploy>.vercel.app/og.jpg` | Multi-file deploy. Same as above. The project name is fixed; deploy alias is predictable. |
| **Surge** | `https://<sub>.surge.sh/` | `https://<sub>.surge.sh/og.jpg` | Multi-file deploy. Same as above — `surge ./dir <sub>.surge.sh` deploys the directory. |
| **GitHub Gist + htmlpreview** | `https://htmlpreview.github.io/?https://gist.githubusercontent.com/<user>/<sha>/raw/lookbook.html` | Upload `og.jpg` to a separate Gist (binary files in Gist are awkward — use a separate transport) | **Two-step.** Upload `og.jpg` to 0x0.st first (`curl -F file=@og.jpg https://0x0.st` → URL), substitute into the HTML, then `gh gist create lookbook.html`. Or skip OG image and accept a textual unfurl on this transport. |
| **AWS S3** | `https://<bucket>.s3.amazonaws.com/<key>.html` | `https://<bucket>.s3.amazonaws.com/<key>-og.jpg` | Multi-file: upload both with `--acl public-read --content-type` set correctly (`text/html` for the page, `image/jpeg` for og.jpg). |
| **0x0.st** | `https://0x0.st/<id>.html` | `https://0x0.st/<other-id>.jpg` (separate upload) | **Two-step.** Upload `og.jpg` first → get URL → substitute into the HTML → upload the HTML. Both URLs persist together as long as the files exist. |

### The pre-deploy substitution flow

For every transport, the agent's pre-deploy step is the same shape:

1. Build `lookbook.html` with `{{ABSOLUTE_PAGE_URL}}` and `{{ABSOLUTE_OG_IMAGE_URL}}` placeholders intact.
2. Build `og.jpg` (Pillow recipe above).
3. Compute the page URL and og:image URL based on the transport. For multi-file transports, both URLs are derived from the deploy URL + filename. For two-step transports, upload `og.jpg` first to get its absolute URL.
4. `sed -i '' "s|{{ABSOLUTE_PAGE_URL}}|$page_url|g; s|{{ABSOLUTE_OG_IMAGE_URL}}|$og_url|g" lookbook.html` (or equivalent string replacement).
5. Deploy.

For Cloudflare Pages the per-deploy `<deploy>.<project>.pages.dev` URL is a fresh subdomain each time. To avoid the chicken-and-egg, **bind a stable Pages alias** (`wrangler pages project create buckmason-lookbook` once + use the project's primary domain `https://buckmason-lookbook.pages.dev` rather than the per-deploy URL) — substitute that, deploy, every deploy serves the same primary URL.

### Shopify-CDN fallback for og:image

If the builder can't generate an `og.jpg` for whatever reason (no Pillow, sandbox restrictions, image-gen failure), fall back to **a representative product flat-lay URL from `cdn.shopify.com`** — the host is already declared in `clawhub.json#permissions.network`, and Shopify's CDN URLs are public, stable, and fast. Lower-fidelity (the preview won't show the customer's try-on, just a flat-lay garment) but always works without an extra hosting step. Pick the `try_on` field from `GET /mcp/buckmason/products/<slug>/imagery` for Look 01's hero piece.

### Verifying the unfurl before sharing

Once the lookbook is hosted, hit `https://www.opengraph.xyz/url/<encoded-deploy-url>` (or any OG validator) to confirm the preview renders. Slack and Twitter cache aggressively — if the customer notices a stale preview after re-deploying, they can force a recrawl in Slack with `/unfurl <url>` or wait for the cache to expire (~24h on most platforms).

### When to skip OG entirely

- **Local file delivery** (no hosting) — no URL means no unfurl.
- **`images` format** — no HTML, no point.
- **PDF / PPT** — different unfurl model (the chat client previews the file itself, not via OG meta).
- **0x0.st with `--no-og` customer preference** — if the customer says "I don't want a preview, just the link," skip the og.jpg upload step and leave the placeholders unresolved. Most clients fall back to a textual unfurl.

## URL stability — one Pages project per permanent lookbook

**The default Cloudflare Pages model overwrites the stable alias on every deploy.** When you `wrangler pages deploy <dir> --project-name foo` repeatedly, `https://foo.pages.dev/` always serves the latest deploy — the previous one is no longer reachable at that URL (per-deploy URLs at `https://<deploy-sha>.foo.pages.dev/` do persist, but they're ugly and not what the customer bookmarks). For test/iteration this is fine — `buckmason-stylist-test` is the canonical "rebuild and replace" project. **For permanent customer-facing lookbooks (weekly newsletter, event-driven generations the customer will refer back to), each lookbook gets its own project**:

```bash
# Pattern: buckmason-<customer-handle>-<lookbook-id>
PROJECT="buckmason-nick-2026-05-09-mellow-la"
bash scripts/deploy-lookbook.sh ./deploy "$PROJECT" --auto --no-overwrite
# → https://buckmason-nick-2026-05-09-mellow-la.pages.dev/
```

The customer can bookmark, share, or revisit any URL ever generated this way and it will keep working — Cloudflare doesn't garbage-collect inactive Pages projects on the free tier. Fifty-two weekly lookbooks per year × multiple years × all event-driven runs adds up to a few hundred projects over time, well within the Pages free-tier project quota (currently 100 active per project but unlimited inactive — verify against the customer's Cloudflare dashboard before going long-running).

### `--no-overwrite` flag

`scripts/deploy-lookbook.sh --no-overwrite` aborts if the named project already has a prior deployment. **Use it on every customer-facing recurring run** to make the URL-stability guarantee load-bearing — if the script ever silently overwrites a project the customer expected to be permanent, the bookmark breaks. Test/iteration scripts (which intentionally rebuild on the same project) just don't pass the flag.

### Naming convention

| Lookbook kind | Project name pattern |
|---|---|
| Test / iteration | `buckmason-stylist-test` (or any short fixed name — overwritten freely) |
| Event-driven (one-off) | `buckmason-<customer>-<lookbook-id>` (e.g. `buckmason-nick-2026-05-09-mellow-la`) |
| Recurring (weekly newsletter) | `buckmason-<customer>-weekly-<YYYY-WW>` (e.g. `buckmason-nick-weekly-2026-19`) |

Customer's preferred prefix lives in `profile.md → lookbook_project_prefix` (default `buckmason-<email-handle>`). Append the `lookbook_id` from the build config — same string the file is filed under. Both segments are kebab-case; the URL ends up readable by humans.

## Quick decision tree (when probing isn't worth it)

For a one-shot ask where the customer has already named a transport:

| Customer intent | Use |
|---|---|
| "Just send my friend right now" | 0x0.st |
| "I want to keep it forever" | Surge or Cloudflare Pages |
| "Branded subdomain on buckmason.com" | wait for the Pima preview endpoint |
| "Send to a Buck Mason customer / anyone external" | Cloudflare Pages with custom subdomain |
| "I'll just airdrop the file" | Skip hosting entirely — hand over the local `.html` |

This tree is for the customer who already has a preference. The default is still: probe, rank, ask once.

## When to load this doc

- Whenever the customer asks for a hosted link to their lookbook (`html` or `html-cart`).
- Skip when the customer wants the local file only (`images`, `ppt`, or "just save it").
