# Publishing the Buck Mason Stylist Skill

This skill is **Buck Mason / Pima.io–specific by design**: it talks to the
private `pima.io` MCP server and is hard-wired to Buck Mason's product taxonomy,
brand voice, and store footprint. It is not intended to be generic.

The goal of publishing is **discoverability inside the OpenClaw / ClawHub
community directory** so other Buck Mason internal tools, agents, and team
members can `clawhub install nickmerwin/buck-mason-stylist-skill` instead of
cloning the Pima repo.

**Live at:** <https://clawhub.ai/nickmerwin/buck-mason-stylist-skill> (v0.1.0,
published 2026-05-01).

## Why ClawHub (and not anthropics/skills)

| | ClawHub (openclaw) | anthropics/skills |
|---|---|---|
| Audience | Multi-CLI (Claude Code + Codex + Gemini + others) | Claude-only reference / examples |
| Listing model | Registry-backed; `clawhub` CLI installs | Submit a PR; users clone the folder |

| Private/brand-specific skills allowed | **Yes — "unlisted" mode** keeps it off browse/search but installable by direct URL | No — repo is for "demonstration and educational purposes" |
| Versioning | Built-in — published tarballs, `clawhub install nickmerwin/buck-mason-stylist-skill@1.2.0` | Folder snapshots, no version semantics |

ClawHub is the right home for a brand-specific skill. anthropics/skills would
require us to genericize away the Buck Mason specifics, which defeats the
purpose.

## Distribution shape — Buck Mason / Pima.io only

### What stays Buck-Mason-specific (do NOT genericize)
- All `/mcp/*` endpoints — hard-coded to `pima.io` host (no `MCP_BASE_URL` env)
- Brand voice ("considered, modern American classics, tonal, soft-shouldered…")
- Store footprint (Abbot Kinney, Century City, Bloomingdale's, etc.)
- Product taxonomy (Como Cashmere, Capitola Linen, OG-107 Fatigue, Hollywood Pleated…)
- Sizing conventions (BM unstructured carry-on jackets use tee sizes XS–XXL, not 38R/40R/42R)
- The whole `references/` package — references real BM SKUs and category names

### What's required to install
- The pima.io MCP is path-tenanted (`/mcp/buckmason/...`); the skill calls it
  directly with no extra setup.
- The user's own `OPENAI_API_KEY` for default Premium virtual try-on lookbooks
  (org-verified for `gpt-image-2`). Other workflows and fallback lookbook tiers
  work without it.
- A Cloudflare KV namespace id (`lookbook_votes_kv_id` or
  `LOOKBOOK_VOTES_KV_ID`) when deploying the default voting-enabled Pages
  lookbook.
- macOS or Linux with `magick` (ImageMagick 7), `jq`, `curl`, `python3` +
  `python-pptx`, and `Pillow`. `stripe/link-cli` is required only for the
  fully-agent-driven MPP checkout path.

These dependencies must be documented in the SKILL.md frontmatter
(`metadata.openclaw.requires`) AND in a top-level "What you need" section so
ClawHub reviewers can approve permissions without back-and-forth.

## Publish flow

1. **Add ClawHub manifest** at the skill root: `clawhub.json`
   ```json
   {
     "name": "buck-mason-stylist",
     "namespace": "pima",
     "version": "0.1.0",
     "visibility": "public",
     "homepage": "https://github.com/buckmason/buck-mason-stylist-skill",
     "primaryEnv": [],
     "optional_env": ["OPENAI_API_KEY"],
     "requires": {
       "binaries": ["magick", "jq", "curl", "python3"],
       "python": ["python-pptx", "Pillow"]
     },
     "categories": ["commerce", "image-generation", "lookbook"],
     "tags": ["buck-mason", "pima", "stylist", "shopping", "stock", "mcp"]
   }
   ```

2. **Update SKILL.md frontmatter** to include the ClawHub-required fields:
   ```yaml
   ---
   name: buck-mason-stylist
   description: Buck Mason shopping stylist — checks online + nearby-store stock,
     suggests outfits, generates gpt-image-2 virtual try-on lookbooks with
     voting-enabled hosted HTML,
     and runs fully-agent-driven MPP checkouts via link-cli.
     Talks to the pima.io MCP at /mcp/buckmason/*.
   compatibility:
     mcp_servers: [pima-mcp]
     binaries: [magick, jq, curl, python3]
   ---
   ```

3. **Add 3–5 screenshots** at `1920x1080` PNG showing: the lookbook PPT,
   a generated try-on image, a stock-check console output. ClawHub requires
   these for the listing page.

4. **Add a permission justification** for any external network calls
   (`pima.io`, `cdn.shopify.com`, `api.openai.com`, `ntfy.sh`). Reviewers
   will reject otherwise.

5. **Publish**:
   ```bash
   clawhub login --token "$CLAWHUB_TOKEN" --no-browser
   clawhub skill publish . --version 0.1.0
   ```
   The `clawhub` CLI requires Node ≥ 20.12. Visibility is read from
   `clawhub.json#visibility` (currently `public`). The published listing is at
   <https://clawhub.ai/nickmerwin/buck-mason-stylist-skill>, indexed in browse
   /search under the `commerce` and `lookbook` categories.

6. **Install instructions** (works for anyone — no Buck Mason credentials needed):
   ```bash
   clawhub install nickmerwin/buck-mason-stylist-skill
   export OPENAI_API_KEY=<your verified-org key>
   ```

## Listed vs unlisted

Because the MCP is now key-less and the catalog endpoints are intentionally
public, this skill is safe to **list publicly** on ClawHub — no credentials
leak from a public install. The trade-off:

| | Listed (public) | Unlisted (direct-URL only) |
|---|---|---|
| Discoverability | On browse / search / categories | Only via direct URL |
| Risk | External agents can hit `pima.io/mcp/buckmason/*` for stock + MPP checkout challenges | Same — the MCP itself is public, so listing doesn't change attack surface |
| Use case | Brand evangelism, reference for other commerce skills | Internal tooling beta, pre-launch |

Recommendation: **publish listed** (`"visibility": "public"`) once the skill
is stable. The MCP is built to take public traffic; ClawHub install volume
on a niche brand-specific commerce skill will be modest; and the listing
becomes free distribution + a credible reference implementation that other
brands can fork.

## Versioning + CI

- Tag `clawhub.json#version` with semver; bump on every change to prompts,
  references, or MCP contract
- Future: add a Pima CI step that runs `clawhub skill publish` on tags matching
  `buck-mason-stylist-v*` so the registry stays in sync with `master`
