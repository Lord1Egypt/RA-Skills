# Facebook Account Operations

> Operating doctrine for Facebook Page automation — careful brand-page pattern via Meta Business Suite, role separation, page-vs-profile-vs-group surface awareness, comment + Messenger ops, moderation discipline (hide vs delete vs ban), and recovery patterns.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](#changelog)

A Claude Code / OpenClaw skill for running Facebook brand **Pages** safely. Battle-tested in a regulated-field operation, ported to be domain-agnostic.

**Why most Facebook automation gets the Page restricted**: it scripts personal-profile-style actions against the Page surface, ignoring the "Posting as: Page" toggle and the Page Quality dashboard. This doctrine doesn't.

---

## What's in the box

- **Pages-only doctrine**: explicit rules against automating personal profiles (fast-track to permanent ban) and third-party groups
- **3-role mental model** for any FB Page (`fb-post` / `fb-engage` / `fb-stealth`)
- **MBS-first**: every reactive op (Messenger, Page comments) goes through `business.facebook.com`
- **Page-Quality-phased posting**: Phase A (Page < 30d, yellow/red quality, or < 100 followers) → Phase B (full doctrine) — with **manual override path** for grandfathered Pages
- **Zero-outgoing-link policy** in comments; max 1 URL in DMs
- **Page moderation discipline**: Hide vs Delete vs Ban — with the "prefer Hide over Delete" rule and `fb-banned-users.md` tracking
- **The MBS comment-Reply navigation bug + workaround** (`@username` prefix + page-level textarea + send-arrow click)
- **24h Messenger window awareness** (out-of-window outbound needs message-tag templates)
- **Strict reply qualification**: skip testimonials-without-link-back, recognize existing clients, 7-day per-user cap
- **Hard quotas** for Pages, calibrated to avoid Page Quality drops
- **Anti-spam triggers**: same-opening-phrase ban, shorteners ban, "as Page" admin-toggle drift check
- **Full recovery playbook**: Page Quality drops, Page restrictions, MBS soft logouts, admin-account "in review", comment automod removals
- **Memory file inventory** for stateful agents (including the `fb-banned-users.md` register)
- **Mandatory recap pattern** with Page Quality in the recap line

---

## Install

### Via ClawHub

The skill is designed to be published on ClawHub — install in one click from your agent once published.

### Manual copy

```bash
mkdir -p ~/.claude/skills/facebook-account-operations
cp SKILL.md ~/.claude/skills/facebook-account-operations/
```

Or for OpenClaw:

```bash
mkdir -p ~/.openclaw/skills/facebook-account-operations
cp SKILL.md ~/.openclaw/skills/facebook-account-operations/
```

---

## Quick start

1. Open `SKILL.md` and fill the placeholders in **Section 0** (brand, Page name + ID, `<META_BUSINESS_ID>`, `<META_ASSET_ID>`, browser profile, port, niche keywords, primary CTA, workspace dir).
2. Verify Page Quality (MBS → Page → Page Quality) is **green** before turning on any cron.
3. Verify the "Posting as: <Page>" chip is set in MBS — it sometimes reverts to the personal admin account after a session refresh.
4. Wire your crons (e.g. DM check `6,21,36,51`, comment check `9,24,39,54`, hourly browser-health).
5. **Start in Phase A** until page_age ≥ 30 days AND followers ≥ 100 AND no warning in 30 days. Don't shortcut.

Shell snippets in the skill use the [OpenClaw](https://openclaw.ai) browser CLI as an example automation stack. Swap them for Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool — the doctrine is stack-agnostic.

---

## Who is this for

Any niche where the brand needs a stable, on-policy Page presence with a real DM + comment moderation loop:

- **Legal services** (origin of the doctrine — works under strict bar association rules)
- **Medical / health** practitioners with public-content strategies
- **Financial advisors** subject to compliance constraints
- **Local businesses** with active comment-section community management
- **Agencies** managing client Pages

Anywhere Page Quality = business reach.

---

## Repository structure

```
facebook-account-operations/
├── SKILL.md         # the skill (full doctrine)
├── README.md        # this file
├── LICENSE          # MIT-0
└── CHANGELOG.md     # version history (TBD)
```

---

## Companion skills

- **instagram-account-operations** — same MBS backbone, IG-specific doctrine.
- **tiktok-account-operations** — for TikTok ops.
- **whatsapp-account-operations** — for BSP-API-driven WhatsApp Business ops (the downstream conversion channel).
- **[reddit-account-operations](https://github.com/AlexBloch-IA/reddit-account-operations)** + **[twitter-account-operations](https://github.com/AlexBloch-IA/twitter-account-operations)** — same doctrine family on other platforms.

---

## License

Released under **MIT-0** (MIT No Attribution). Use, fork, adapt, redistribute. No attribution required.
