---
name: ad-engine
description: Assemble modular ads from Supabase components and deploy to Facebook Ads Manager via the Marketing API. Supports preview, single/batch deploy, and status tracking. Uses ad_components table for A/B testing at scale.
---

# Ad Engine — Facebook Ads Deployment

Assemble ads from database components and deploy to Facebook. Reads from Supabase `ad_components` + `messages` tables, assembles full ad copy, uploads images, and creates Campaign → Ad Set → Ad in Facebook Ads Manager.

## First-Time Setup

**1. Facebook prerequisites (one-time, manual):**
- Facebook Business Manager account
- Ad Account created
- Facebook Page connected
- Facebook Developer App with `ads_management` permission
- Long-lived access token (generate at developers.facebook.com)

**2. Store credentials:**
```bash
python3 scripts/fb_deploy.py --setup
```
Prompts for access token, ad account ID, and page ID. Validates against FB API and saves to `~/.config/ad-engine/fb_config.json`.

## Usage

**Preview assembled ads (no deployment):**
```bash
# Preview a single ad
python3 scripts/fb_deploy.py --preview --message-id 8555

# Preview all draft ads for a campaign
python3 scripts/fb_deploy.py --preview --campaign-id 43

# Preview as JSON
python3 scripts/fb_deploy.py --preview --campaign-id 43 --json
```

**Deploy a single ad:**
```bash
python3 scripts/fb_deploy.py --deploy \
  --message-id 8556 \
  --image /path/to/security-audit-ad.png \
  --landing-url "https://calendly.com/your-link" \
  --objective messages
```

**Deploy all draft ads for a campaign:**
```bash
python3 scripts/fb_deploy.py --deploy \
  --campaign-id 43 \
  --image-dir /path/to/ad-images/ \
  --landing-url "https://calendly.com/your-link" \
  --objective messages
```

**Dry run (preview what would be created):**
```bash
python3 scripts/fb_deploy.py --deploy \
  --campaign-id 43 \
  --image-dir /path/to/images/ \
  --landing-url "https://calendly.com/link" \
  --dry-run
```

**Check deployed ad status + live metrics:**
```bash
python3 scripts/fb_deploy.py --status --campaign-id 43
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--preview` | One of | Preview assembled ads without deploying |
| `--deploy` | these | Deploy ads to Facebook |
| `--status` | three | Check status of deployed ads |
| `--setup` | | Configure Facebook credentials |
| `--message-id` | For single | Specific message ID to preview/deploy |
| `--campaign-id` | For batch | All draft ads in a campaign |
| `--image` | Deploy single | Image file path |
| `--image-dir` | Deploy batch | Directory of images (matched by angle name in filename) |
| `--landing-url` | Deploy | Booking/landing page URL |
| `--objective` | No | `leads` (default), `messages`, or `link_clicks` |
| `--dry-run` | No | Preview deployment without creating anything |
| `--json` | No | Output as JSON |

## Image Naming Convention

When using `--image-dir` for batch deploy, name images by angle:
```
security-audit-ad.png      → matches angle "security_audit"
setup-is-hell-ad.png       → matches angle "setup_is_hell"
dm-trigger-checklist.png   → matches angle "dm_trigger"
anti-wrapper-graveyard.png → matches angle "anti_wrapper"
```

## How It Works

1. Reads message from Supabase `messages` table (content_type = 'fb_ad')
2. Reads component references from message's `extra_data.components`
3. Resolves component keys → actual text from `ad_components` table
4. Slots components into framework template using `{{merge_tags}}`
5. Uploads image to Facebook → gets image_hash
6. Creates Campaign (if new) → Ad Set (if new) → Ad Creative → Ad
7. Updates message status to 'deployed' with FB IDs stored in extra_data

## Database Schema

See `AD_ENGINE_SPEC.md` for full schema documentation.

## Dependencies

- `psycopg2-binary` — Supabase Postgres connection
- `facebook-business` — Facebook Marketing API SDK
- `requests` — HTTP client
- All auto-installed on first run.
