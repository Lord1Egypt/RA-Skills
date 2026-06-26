# CodivUpload Social Manager (via codivupload.com)

Autonomously manage social media posting via the [CodivUpload](https://codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-hero-product) API — schedule, publish, cross-post, and analyze content across YouTube, Instagram, Facebook, X, TikTok, Threads, and Pinterest from one OpenClaw skill.

[![ClawHub](https://img.shields.io/badge/ClawHub-codivupload--social--manager-cyan)](https://clawhub.ai/codivion/codivupload-social-manager)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Codivion/codivupload-skills/blob/main/LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-7%2B-green)](https://codivupload.com/use-case/ai-skills/openclaw?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=platforms-badge)
[![MCP](https://img.shields.io/badge/MCP-supported-violet)](https://www.npmjs.com/package/codivupload-mcp)
[![Get an API key — Starter $20/mo](https://img.shields.io/badge/Get_an_API_key_%E2%80%94_Starter_%2420%2Fmo-codivupload.com-indigo?style=for-the-badge)](https://app.codivupload.com/en/auth/login?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=hero-cta-badge)

> **Start free, upgrade when you want the agent to do it for you.** [Sign up for free](https://codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=hero-free-cta) — no credit card — and try CodivUpload from the **web dashboard**: 10 uploads/month across all 7+ launched platforms (YouTube, Instagram, Facebook, X, TikTok, Threads, Pinterest), drag-and-drop calendar, AI captions. When you're ready for your **OpenClaw agent to schedule + cross-post + run livestreams for you**, upgrade to **Starter** — $20/mo (or $200/yr — 2 months free), API access included. Pro / Business / Enterprise unlock more profiles, team seats, livestreams, and analytics. [See full pricing →](https://codivupload.com/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=pricing-callout)

> **Prefer to test the API with your agent first? Start a 7-day free trial.** $0.00 due today, card collected for auto-renewal after the trial. Cancel anytime during the 7 days — no charge. One trial per customer lifetime. Available on every paid plan, monthly or yearly. Pick this if you want full API + MCP access for your OpenClaw agent before committing to a subscription. [Start trial →](https://app.codivupload.com/en/dashboard/subscription?trial=1&utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=hero-trial-cta)

> **Quick start — two paths to get an API key:**
>
> **A) Trial path (recommended for "try first, decide later"):** sign up at [codivupload.com](https://codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=quick-start-trial-signup) → open Dashboard → Subscription → toggle **Free Trial = ON** → pick Starter (or Pro/Business/Enterprise) → click **Start 7-day free trial** ($0.00 charged today, card required for auto-renewal) → create a profile → connect a social account → generate an API key → `openclaw config set CODIVUPLOAD_API_KEY=<YOUR_API_KEY>` → ready. You have **full API + MCP access immediately** — same as a paid subscription. Cancel anytime in the 7 days from the Stripe Customer Portal for $0 charge.
>
> **B) Direct subscribe path (if you already know you want it):** sign up at [codivupload.com](https://codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=quick-start-signup) → subscribe to Starter ($20/mo or $200/yr) → create a profile → connect a social account → generate an API key → `openclaw config set CODIVUPLOAD_API_KEY=<YOUR_API_KEY>` → ready.
>
> Both paths grant identical access. Full step-by-step in the Setup section below.

### Try this on day 1 (after setup)
Once you've completed the 5-minute setup, paste these prompts to your OpenClaw agent — each one runs through the full skill:

- *"List my CodivUpload profiles and which platforms are connected on each."* — sanity-checks your key + profile + connected accounts in one call.
- *"Schedule this video to post on TikTok, Instagram, and YouTube tomorrow at 9am — caption: 'Quick productivity tip'."* — exercises cross-platform fan-out + scheduling.
- *"What's the best time to post for my Instagram audience?"* — pulls 90-day analytics to recommend a slot.
- *"Set up a 24/7 YouTube live stream with this MP4 source URL."* — kicks off the BYOP / managed live stream flow with the explicit stop instruction surfaced.

---

## Setup — your first 5 minutes

CodivUpload is a service running at `codivupload.com`; this skill is the OpenClaw client for that service. Before the agent can post anything, you need an **account + a profile + connected social accounts + an API key**, in that order. Steps 1-4 happen in your browser on the dashboard; step 5 is one terminal command.

### 1. Create a CodivUpload account (Free is fine to start, Starter unlocks the skill)
Sign up at **[app.codivupload.com/en/auth/login](https://app.codivupload.com/en/auth/login?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-step-1-signup)** (email + password, or Google OAuth). The **Free plan** activates automatically — **$0, no credit card, 10 uploads/month** across all 7+ launched platforms. Try CodivUpload from the **web dashboard** first if you want — drag-and-drop calendar, AI caption generation, scheduled posts.

When you're ready for **your OpenClaw agent to do the work for you** (schedule, cross-post, run livestreams via API), upgrade to **Starter** — **$20/mo** or **$200/yr** (2 months free yearly). API access starts at Starter. Upgrade from Dashboard → Subscription, or directly via **[codivupload.com/pricing](https://codivupload.com/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-step-1-upgrade-starter)**. ~2 min total.

### 2. Create a profile
Profiles are CodivUpload's grouping concept: one profile = one brand or client, with many social accounts attached. The skill posts AS a profile (not directly to a social account).

Go to **Dashboard → Profiles → New profile** at **[app.codivupload.com/en/dashboard/profiles](https://app.codivupload.com/en/dashboard/profiles?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-step-2-profile-create)**. Pick a `username` (lowercase, no spaces) — this is the `profile_name` the agent will use. Examples: `acme_brand`, `client_bloomskin`, `personal`. ~1 min.

### 3. Connect social accounts to the profile
Open your profile from **[app.codivupload.com/en/dashboard/profiles/all](https://app.codivupload.com/en/dashboard/profiles/all?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-step-3-profile-list)**. On the profile detail screen, click each platform's logo (YouTube, Instagram, Facebook, X, TikTok, Threads, Pinterest) you want the agent to post to. An OAuth popup for that platform authorizes the connection; CodivUpload stores the token AES-256-GCM-encrypted server-side. ~30 sec per platform.

**Per-platform notes:**
- **Instagram + Facebook:** must be a Business or Creator account linked to a Facebook Page (Meta API limitation — Personal accounts can't post via any third-party tool).
- **TikTok:** Direct Post permission may take 24-48h on new accounts; Draft mode (`tiktok_post_mode=DRAFT`) works immediately.
- **YouTube:** the shared OAuth covers ~10K units/day across all CodivUpload users combined. For dedicated quota, set up [BYOP](https://codivupload.com/blog/youtube-byop-setup?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=byop-info-readme) — your own Google Cloud project tied to your account.
- **X (Twitter):** shared OAuth works on X's free dev tier via CodivUpload's own X app. For high volume, [BYOK](https://codivupload.com/blog/x-byok-setup?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=byok-info-readme) requires X Basic ($100/mo on X's side).

### 4. Generate an API key
Go to **Dashboard → Settings → API Keys → New key** at **[app.codivupload.com/en/dashboard/api-keys](https://app.codivupload.com/en/dashboard/api-keys?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=readme-step-4-api-key-create)**. Pick the narrowest scope that fits (see [Configuration](#configuration) below — for most users, **per-workspace** is the right default). Give the key a descriptive name (e.g. `openclaw-mac-laptop`) so it's easy to revoke later. The key shows **once** on creation — copy it immediately (format: `cdv_<40 chars>`). ~30 sec.

### 5. Set the key in OpenClaw config
```bash
openclaw config set CODIVUPLOAD_API_KEY=<YOUR_CODIVUPLOAD_API_KEY>
```
The skill reads the key from this config layer only. Never paste the key into the chat window with your AI agent — if it ends up in chat logs, rotate it from Dashboard → API Keys → Revoke + reissue. ~5 sec.

### 6. First prompt
Try a no-op verification first — ask your agent:
> "List my CodivUpload profiles and which platforms are connected on each."

This calls `GET /v1/profiles` once and tells you in one shot whether the key is valid, whether the profile exists, and which platforms are wired up. From there, real posting prompts work — see [Usage examples](#usage-examples) below.

### Optional — install the MCP server
Speeds up agent token usage; the skill works without it.
```bash
npm install -g codivupload-mcp@2.0.0   # exact pin
```

---

A comprehensive social media manager skill for OpenClaw. Turns your local AI assistant into an autonomous social media manager for **YouTube, Instagram, X (Twitter), Facebook, TikTok, Threads, and Pinterest** — **7+ platforms launched** (with Bluesky in active rollout).

## YouTube · Instagram · X · Facebook — first-class support

This skill puts the **most-used platforms** front and center, with deeper integration than any rival skill:

### YouTube
- **Schedule + publish** long-form videos, Shorts, livestreams
- **24/7 managed live streams** with the managed live stream relay (zero CPU on your machine)
- **BYOP** (Bring Your Own Project) → unlimited daily upload quota via your own Google Cloud project (vs shared 10K-unit limit on rival skills)
- **Made-For-Kids** (MFK / COPPA) flag handled correctly per upload
- Premiere scheduling, end screens, cards
- Bulk upload 60+ Shorts per day per channel with BYOP

### Instagram
- **Reels + Stories + Carousels + Feed posts** — full coverage
- Auto-schedule without the push-notification-on-phone dance
- Business + Creator account support (no Personal-account limitation)
- Per-post platform overrides (caption, hashtags, first-comment)
- Cross-post tag, location, music sync
- Up to 10-image carousels with mixed photo + video

### X (Twitter)
- **Long-form posts** (25K chars on X Premium / Premium+)
- **Threads** with native reply chains, polls, scheduled
- **BYOK** (Bring Your Own Keys) → unlimited free-tier posts via your own X Developer App (rival skills cap you on shared keys)
- Quote posts, reposts, image/video attachments
- X Premium feature awareness — agent suggests Premium tier when needed

### Facebook
- **Page posts** (Personal not supported by Meta API anywhere — this is API-level, not skill-level)
- Reels, video, image, link previews
- Multi-page support for agencies (manage 100+ Pages)
- Scheduled posts via Meta Graph API (proper, not browser automation)
- Group posting via authenticated Page admin

Plus **TikTok, Threads, and Pinterest** all launched with the same depth. **Bluesky** is in active rollout — skill auto-detects new platforms via the API.

## Why this skill (vs alternatives)

| Capability | CodivUpload Skill | Post Bridge Skill | Other social skills |
|---|---|---|---|
| **Platform count (launched)** | **7+** | 5 | 3-7 |
| **MCP server** | ✅ `codivupload-mcp` | ❌ | ❌ |
| **24/7 live streaming** | ✅ Managed live stream relay | ❌ | ❌ |
| **BYOP** (dedicated YouTube quota) | ✅ | ❌ | ❌ |
| **BYOK** (dedicated X rate limit) | ✅ | ❌ | ❌ |
| **Agency multi-tenant** | ✅ Workspace cascade + RBAC | ❌ | ❌ |
| **Whitelabel branded OAuth** | ✅ Pro+ | ❌ | ❌ |
| **TypeScript SDK** | ✅ npm: `codivupload` | ❌ | partial |
| **Python SDK** | ✅ PyPI: `codivupload` | ❌ | partial |
| **Free plan (dashboard only, no API)** | ✅ 10 uploads/mo, all launched platforms, no credit card | varies | varies |
| **API access starts at** | Starter ($20/mo · $200/yr 2 months free) | varies | varies |
| **MIT-licensed skill artifact** | ✅ Fork-friendly | ✅ | ✅ |
| **Active development** | Weekly releases | varies | varies |

**Bottom line:** CodivUpload Skill is the only OpenClaw skill that turns your local AI agent into a **full-stack social media operations system** — not just a basic scheduler. Live streams, agency workspaces, BYOP/BYOK, MCP-native — all in one skill.

## What this skill does

When installed, your OpenClaw agent (running locally on Mac / Linux / Windows) gains the ability to:

- **Schedule posts** to any of the 7+ launched social platforms (with Bluesky in active rollout) — platform-specific overrides per platform
- **Help draft and queue** YouTube Shorts, TikToks, and Reels via the REST API (the skill defaults to scheduled / draft modes; bulk operations require explicit user confirmation up front)
- **Set up 24/7 YouTube live streams** with managed live stream relay (always confirmation-gated; the skill includes the `DELETE /v1/livestreams/{id}` stop instruction whenever it starts a stream)
- **Pull cross-platform analytics** for engagement, growth, best-time-to-post (read-only)
- **Manage agency client profiles** with whitelabel branding
- **Use BYOP** (Bring Your Own Project) for dedicated YouTube quota
- **Use BYOK** (Bring Your Own Keys) for dedicated X rate limits

The skill prefers calling [CodivUpload's MCP server](https://www.npmjs.com/package/codivupload-mcp) when configured, falling back to direct REST API calls otherwise.

### Safety defaults baked into the skill
SKILL.md ships with a **Safety & confirmation defaults** section (read by the LLM at activation) that requires explicit user confirmation before any immediate publish, bulk operation (≥3 posts), live stream start, profile/account change, or spending-impacting action. The skill prefers scheduled/draft modes over immediate publish, prefers single-platform smoke tests before fan-out, and never logs or echoes the API key. See `SKILL.md` → "Safety & confirmation defaults" for the full list.

## Installation

```bash
# Drop SKILL.md into your OpenClaw skills workspace
mkdir -p ~/.openclaw/workspace/skills/codivupload
cp SKILL.md ~/.openclaw/workspace/skills/codivupload/SKILL.md

# Optional: install the MCP server (gives the agent direct tool access).
# IMPORTANT: use an EXACT version pin — no caret, no tilde, no `latest`.
# A credentialed runtime (the MCP server inherits CODIVUPLOAD_API_KEY)
# should never resolve a floating range.
npm install -g codivupload-mcp@2.0.0

# Verify before relying on it:
npm view codivupload-mcp publisher        # → codivion <accounts@codivion.com>
npm view codivupload-mcp@2.0.0 dist.integrity
# expected: sha512-pK0r8XkR2M/brfn1Nsy6Uh7nGDx5qpx9h3pLgZljYkU3pv0BXKb7uJapBOFL11mBIQhWAl0hASxxCSLE11SDfA==
```

The skill works **without** the MCP server (it falls back to direct REST API + the official TypeScript / Python SDKs) — install only if you want fewer agent tokens spent on tool descriptions. Skip it to keep the supply-chain surface to zero. **Avoid `npx -y codivupload-mcp` without a pinned exact version** — `-y` auto-accepts whatever the registry resolves, which is a bad fit for a credentialed runtime.

## Configuration

Set your CodivUpload API key in OpenClaw config (this is the only place the skill reads it from — the skill never asks for the key in chat and never echoes it back):

```bash
openclaw config set CODIVUPLOAD_API_KEY=<YOUR_CODIVUPLOAD_API_KEY>
```

### Issue the **narrowest** key the skill needs (this is the most important security setting)

The CodivUpload API enforces per-key scope **server-side** — pick the narrowest tier that fits your use case:

| Tier | Authority | When to use | How to create |
|---|---|---|---|
| **Single-platform** | Publish to ONE platform on ONE profile. No analytics, no profile mgmt, no billing. | Skill will only post to (e.g.) Instagram for one brand. | Dashboard → API Keys → New → Limit platform + profile |
| **Per-workspace (RECOMMENDED DEFAULT)** | Publish + analytics within ONE workspace. No cross-workspace, no billing. | Skill manages one brand or one client across multiple platforms. | Dashboard → Workspaces → \[workspace\] → API Keys → New |
| **Posting-only** | Publish + analytics across all workspaces. **No** profile mgmt, **no** billing. | Power user with multiple brands but doesn't want the agent touching settings. | Dashboard → API Keys → New → Toggle off "Profile management" + "Billing actions" |
| **Global account key** | Everything: publish across all workspaces, profile mgmt, billing changes. | **Avoid for agent use.** Only when you intentionally want the agent to add seats / change plan. | Dashboard → API Keys → New (default) |

**The skill expects a per-workspace key by default.** If you provide a global account key, the skill will warn you before allowing any billing-impacting or cross-workspace action and require explicit acknowledgement. This is the only effective mitigation against an over-broad credential — confirmation gates are second-line; **scope is first-line**.

If you ever paste the key into chat by mistake, rotate it from Dashboard → API Keys → Revoke + reissue. Full credential-handling rules are spelled out in `SKILL.md` → "Required key scope" + "Credential handling" so the agent enforces them on your behalf.

If you don't have an account yet, sign up at [codivupload.com](https://codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=config-section-signup). The **Free plan** covers **10 uploads/month** via the web dashboard (no credit card, no API). This skill calls the REST API, so you'll need **Starter** or higher — $20/mo or $200/yr with 2 months free. Full tier breakdown on [codivupload.com/pricing](https://codivupload.com/pricing?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=config-section-pricing).

## Usage examples

After installation, you can ask your OpenClaw agent things like:

```
"Schedule this video to post on TikTok, Instagram, and YouTube tomorrow at 9am"
"Cross-post my latest blog announcement to X and Threads"
"Pull engagement stats for my Instagram for the last 30 days"
"Set up a 24/7 YouTube live stream with this MP4 source"
"List my connected social profiles"
"What's the best time to post for my TikTok audience?"
```

The skill will activate automatically when these phrases match the trigger description in `SKILL.md`.

## How it integrates with OpenClaw

OpenClaw's skill system reads the YAML frontmatter to determine **when** to activate this skill, then injects the markdown body as context for the LLM (Claude / GPT / local model). The body includes:

- Complete API contract for `POST /v1/posts`
- Platform-specific override parameters (per-platform tables)
- Worked examples for common patterns (cross-post, scheduling, BYOP, live stream)
- MCP integration setup if available
- Error handling + retry guidance

The agent uses this knowledge to either:
1. **Call MCP tools directly** if `codivupload-mcp` is registered as an MCP server (each tool call is subject to OpenClaw's per-tool approval prompt + the skill's confirmation gates).
2. **Generate `curl` / SDK code for the user to review and run** — the skill's safety defaults instruct the LLM to surface every publish/bulk/livestream command to the user for explicit confirmation before any execution via OpenClaw's `exec` tool. Raw, un-confirmed execution of publishing commands is **disallowed by SKILL.md**.

## Files in this package

```
openclaw-skill/
├── SKILL.md          # Main skill definition (YAML frontmatter + agent instructions)
└── README.md         # This file
```

## Compatibility

- **OpenClaw**: All recent versions (skills system stable since v0.1)
- **Operating systems**: macOS, Linux, Windows
- **Backing LLMs**: Works with Claude (3.5+), GPT-4o+, local models with tool-use support
- **Optional MCP server**: `codivupload-mcp` (`npx codivupload-mcp` to test)

## Related

- **CodivUpload MCP server**: [npmjs.com/package/codivupload-mcp](https://www.npmjs.com/package/codivupload-mcp)
- **CodivUpload TypeScript SDK**: [npmjs.com/package/codivupload](https://www.npmjs.com/package/codivupload)
- **CodivUpload Python SDK**: [pypi.org/project/codivupload](https://pypi.org/project/codivupload/)
- **REST API docs**: [docs.codivupload.com](https://docs.codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=related-api-docs)
- **Claude / ChatGPT / Cursor / Zed Skills version**: see the sibling directories in the same repo — [Codivion/codivupload-skills](https://github.com/Codivion/codivupload-skills) (per-platform skill files for the launched platforms)

## License

The skill artifact (this file + SKILL.md) is MIT-licensed — fork it, adapt it, ship it.

## Support

- Docs: [docs.codivupload.com](https://docs.codivupload.com?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw-onboarding&utm_content=support-docs)
- Issues: [github.com/Codivion/codivupload-skills/issues](https://github.com/Codivion/codivupload-skills/issues)
- Email: support@codivupload.com
