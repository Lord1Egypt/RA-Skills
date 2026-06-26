---
name: facebook-account-operations
description: Operating doctrine for Facebook Page automation — careful brand-page pattern via Meta Business Suite, role separation, page-vs-profile-vs-group surface awareness, comment + Messenger ops (Playwright click + type + Enter), moderation discipline (hide vs delete vs ban), and recovery patterns. Use this for any scheduled FB activity (cron, agent, recurring task) where account / page safety and reach matter more than raw output.
---

# Facebook Account Operations

This skill is the operating doctrine for every Facebook automation run on a brand **Page** (recommended), professional or personal account.

**The goal is not to comment fast. The goal is to operate Facebook like a careful, helpful human community manager: stable browser, correct context (Meta Business Suite), useful action, no page restrictions, no reputational risk.**

Drop-in for any niche (legal, medical, software, finance, creator, ecommerce). Replace the placeholders in section 0 with your own values.

---

## 0. Configure for your brand

Before running anything, fill these placeholders in your local copy or your agent's memory:

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<FB_PAGE_NAME>` | "Acme Studio" (the public Page name) | — |
| `<FB_PAGE_ID>` | numeric ID of the Page | — |
| `<META_BUSINESS_ID>` | numeric ID from business.facebook.com → Settings | — |
| `<META_ASSET_ID>` | numeric ID of the FB Page asset in MBS | — |
| `<BROWSER_PROFILE>` | "facebook-live" | — |
| `<BROWSER_PORT>` | "18803" | — |
| `<NICHE_KEYWORDS>` | "lost license OR speeding ticket" | — |
| `<PRIMARY_CTA>` | "WhatsApp / form / app — pick ONE" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/facebook-<brand>" | — |

All shell snippets below assume an [OpenClaw](https://openclaw.ai) browser CLI bound by CDP, but the doctrine works with any browser-automation stack (Playwright, Puppeteer, Chrome MCP). Swap the CLI calls for your own.

### Quick config (copy-paste YAML)

```yaml
brand:
  name: <BRAND_NAME>
  domain: <BRAND_DOMAIN>

facebook:
  page_name: <FB_PAGE_NAME>
  page_id: <FB_PAGE_ID>
  browser_profile: <BROWSER_PROFILE>
  browser_port: <BROWSER_PORT>

meta_business_suite:
  business_id: <META_BUSINESS_ID>
  asset_id: <META_ASSET_ID>
  base_url: https://business.facebook.com/latest/inbox

discovery:
  niche_keywords: <NICHE_KEYWORDS>

cta:
  primary: <PRIMARY_CTA>

workspace:
  dir: <WORKSPACE_DIR>

alerts:
  channel: telegram | slack | discord
  webhook: <YOUR_WEBHOOK_URL>

schedule:
  timezone: Europe/Paris
  windows:
    dm_check:      "6,21,36,51 9-22 * * *"
    comment_check: "9,24,39,54 9-22 * * *"
    browser_health: "0 * * * *"
    daily_recap:   "21:00"
```

### Compatibility

| Stack | Skill install path |
|---|---|
| [Claude Code](https://claude.ai/code) | `~/.claude/skills/facebook-account-operations/` |
| [OpenClaw](https://openclaw.ai) | `~/.openclaw/skills/facebook-account-operations/` |
| ClawHub-published | one-click install via [clawhub.ai](https://clawhub.ai) |
| Cursor / Copilot CLI | drop `SKILL.md` into your project's `.cursorrules` or `AGENTS.md` |
| Any LLM agent reading markdown rules | concatenate `SKILL.md` into your system prompt |

---

## 1. Pages vs personal profile vs groups

Doctrine for brand automation:

- **Page** = the only sanctioned surface for brand activity. Page admins post as the Page, reply as the Page, and the Page has its own analytics + ad surface.
- **Personal profile** = never automate. Personal profiles are governed by Facebook's "authentic identity" policy; automating one is a fast path to a permanent ban.
- **Groups** = automation is allowed only if the brand **owns** the group (Page is the admin). Replying as the Page on third-party groups requires the group to allow Page comments — most do not. Default: do not automate group activity.

This skill covers the **Page surface** exclusively.

### The Meta Business Suite is the canonical surface (same as Instagram)

Everything goes through `business.facebook.com`. Never automate against `facebook.com` directly — the personal-profile DOM is unstable, IP-throttled, and any anti-automation trigger there can poison the Page-admin's personal account.

### Physical profile

A single browser profile per Page-admin account:

- `<BROWSER_PROFILE>` (CDP direct, attached to `http://127.0.0.1:<BROWSER_PORT>`)

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> navigate https://business.facebook.com/latest/inbox/all/?business_id=<META_BUSINESS_ID>&asset_id=<META_ASSET_ID>
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 200
```

### Canonical URLs (per tab)

| Tab | URL fragment |
|---|---|
| All messages (Messenger + IG DMs if cross-linked) | `/latest/inbox/all?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Messenger only (Page DMs) | `/latest/inbox/messenger?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Facebook Page comments | `/latest/inbox/facebook?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Page Insights | `https://business.facebook.com/latest/insights/all_tools?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |
| Page Posts | `https://business.facebook.com/latest/posts?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>` |

### Roles (mental separation, single physical profile)

#### Role: `fb-post`

Page cockpit (acting AS THE PAGE, not as the admin's personal account). Use for:
- Messenger DM replies in MBS.
- Page comment replies in MBS.
- Page posts (text, photo, link) via MBS Publishing Tools.
- Page Insights snapshots.

Default page: MBS `inbox/all`.

#### Role: `fb-engage`

Discovery. Use for:
- Reading comments under your own Page posts (in MBS).
- Inspecting a candidate user's profile before replying (open `facebook.com/<user>` in a separate tab — DO NOT act from there).

Default page: MBS `inbox/facebook` (comments).

#### Role: `fb-stealth`

Quiet maintenance. Use for:
- Checking Page Quality (MBS → Page → Page Quality).
- Reading audience demographics.
- Page-level settings (admin roles, page restrictions).

Default page: MBS dashboard.

### Operational law

- `fb-post` = act AS THE PAGE via MBS.
- `fb-engage` = discover, never act outside MBS.
- `fb-stealth` = maintain quietly.
- Stability matters more than speed.
- After every run, return to MBS `inbox/all`.

---

## 2. Session check (run first on every cron)

Same as Instagram — see `instagram-account-operations` §2. The MBS session covers both IG and FB assets when both are linked to the same `<META_BUSINESS_ID>`.

If you only manage a FB Page (no IG asset), the same login + navigation pattern applies; replace `inbox/all` with `inbox/messenger` for the smoke test.

---

## 3. Phase gating (Page restrictions awareness)

Facebook Pages do not have karma; they have:
- **Page Quality** score (MBS → Page → Page Quality): green / yellow / red.
- **Restrictions** — applied at Page level. A restricted Page cannot run ads, cannot use Messenger templates, sometimes cannot post.
- **Standard account-level holds** (very young Page-admin account, recent guidelines violations).

Phases:

- **Phase A** (Page < 30 d, OR last 30 d had a Page-level warning / Restriction, OR < 100 followers): inbound DM/comment replies inside MBS only. No outbound DMs. No comment-on-other-Pages. No new ads.
- **Phase B** (Page ≥ 30 d, Page Quality = green, ≥ 100 followers, admin account in good standing): all crons authorized.

Always read `<WORKSPACE_DIR>/memory/fb-state.md` at start.

### Manual override (advanced)

Same as IG — append `YYYY-MM-DD - phase=B (manual override)` to `fb-state.md` for grandfathered, verified Pages. Document the rationale in `fb-learnings.md`.

---

## 4. Qualification of an inbound DM or comment

A DM or comment is repliable only if **all** of:

- The thread has at least one user-authored message.
- The user is not banned from your Page (`fb-banned-users.md`).
- The comment is on a Page post (not on a shared link to your Page).
- Phase B authorized for brand-mentioning replies.
- The message is a real question or intent in your domain.
- Same user not already replied-to in the last 7 days (`fb-reply-log.md`).

If any check fails: skip.

### Special: existing client recognized

If the user is in `fb-clients-known.md`, redirect to your client support channel (NOT `<PRIMARY_CTA>` for prospects).

### Special: a public testimonial / positive comment

Do **NOT** redirect to `<PRIMARY_CTA>`. Reply with a public thank-you. No CTA, no link.

---

## 5. Reply templates

### Phase A

Plain, helpful, no brand mention, no link.

### Phase B

DM reply structure:
```
[Acknowledge the situation in 1 sentence, neutral tone.]

[General framework in 2-3 short paragraphs.]

[Concrete next step — point to <PRIMARY_CTA>. ONE channel only.]
```

Page-comment reply structure (Page comments are public — keep them short and bold-typo-free):
```
@<UserName> [contextual acknowledgement]. [Indirect signal — "DM us" or "form on Page"].
```

### Brand link policy

- Comment body: NO URL. "DM us" or "form on Page" only.
- DM body: max ONE URL, ONE channel (`<PRIMARY_CTA>`).
- Never shorteners — FB marks them as spam and Page Quality drops.

---

## 6. Original posting cadence

Out of scope for the live reactive crons. Recommended rhythm for a Phase B Page:

- **3-5 posts/week**. Mix: 1 text-only (high reach if good), 2 image/carousel, 1 video.
- **No "post & ghost"** — every Page post gets replies within 2 hours of going live.
- **Avoid burst posting** (> 3 posts within 24 h). Reach gets distributed across same-day posts.
- **Pin your evergreen content** to the top of the Page (one Pin slot).

### Boost vs ads

- **Boost** = the simple, in-feed promotion button. Use for an isolated organic post that is over-performing.
- **Ads (Ads Manager)** = full targeting + creative + funnel. Use for systematic acquisition. Out of scope here.

Never boost a comment-reply. Boost only top-level Page posts.

---

## 7. Quotas (hard limits)

| Action | Phase A limit | Phase B limit |
|--------|---------------|---------------|
| DMs handled / 24 h | 20 | 80 |
| DMs handled / cron run | 4 | 10 |
| Comment replies handled / 24 h | 30 | 120 |
| Comment replies handled / cron run | 5 | 12 |
| Outbound DMs / day (proactive) | 0 | 0 — Page Messenger outbound is heavily restricted; rely on templates with opt-in only |
| Page posts / day | 1 | 3 |
| Comments on other Pages | 0 | 5 (sober, on-topic, no link) |
| Actions in same conversation | min 60 s apart | min 30 s apart |
| Actions globally | min 30 s apart | min 15 s apart |

Quota tracking: read `fb-reply-log.md` at start of every run.

---

## 8. Anti-spam triggers

### Content

| Avoid | Use instead |
|-------|-------------|
| `<BRAND_NAME>` more than once per reply | (max one mention) |
| URLs in comment bodies | (never) |
| Multiple URLs in a single DM | (max 1) |
| "Click here", "DM me", "WhatsApp me" all together | (one CTA, one channel) |
| Emojis in regulated niches | (drop them) |
| All caps for emphasis | (use sparingly) |
| Shorteners (bit.ly / tinyurl) | (use the canonical URL) |
| Tagging unrelated Pages | (never — it spams the tagged Page) |

### Behavioral

- Replying within 15 s of a comment landing → bot-like; wait ≥ 1 min.
- Same opening phrase across multiple replies → flagged. Vary openings.
- > 12 actions in 10 min → rate limit.
- Identical DM body to > 3 users in 24 h → near-instant Page restriction.
- Page admin acting from the personal profile (instead of "as Page") under a Page post → "this comment looks like spam" toast.

---

## 9. Operational flow inside Meta Business Suite

Same backbone as Instagram §9. FB-specific notes below.

### DM (Messenger) check / reply (validated)

URL: `https://business.facebook.com/latest/inbox/messenger?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>`

The flow is identical to the IG-DM flow in `instagram-account-operations` §9 (Playwright `click + type + press Enter`). Differences:

- Messenger threads include the user's **Facebook profile** in the right sidebar — useful for the qualification step (see §4).
- The "Mark as Done" button under the Messenger thread is a useful workflow signal — click it after a reply to keep the inbox clean and improve next-cron-run targeting.
- **24h customer-service window**: Page Messenger has a 24h reply window — after 24 h of user silence, only message-tag templates can be sent (`HUMAN_AGENT`, `CONFIRMED_EVENT_UPDATE`, etc.). Out of scope for this skill — if you need post-24h outbound, use the Conversations API with an approved tag.

### Page comment reply (validated — with workaround)

URL: `https://business.facebook.com/latest/inbox/facebook?asset_id=<META_ASSET_ID>&business_id=<META_BUSINESS_ID>`

Same SPA bug as IG comments: clicking the per-comment "Reply" link sometimes navigates the right pane to a different post. Same workaround:

1. Find the page-level comment textarea **at the bottom** of the right pane.
2. Type `@<UserName> your reply`.
3. Click the send-arrow button (not Enter).

This posts a top-level comment under the same post but tagged at the parent — which is sufficient for visibility and notification.

### Page moderation: hide vs delete vs ban

When a comment is offensive, spammy, or off-topic:

| Action | Effect | When |
|---|---|---|
| **Hide** | Comment stays visible to the author + their friends, invisible to everyone else | Default for most low-quality comments — author doesn't notice, no escalation |
| **Delete** | Comment removed | Only for clearly offensive content or doxxing |
| **Ban user from Page** | User can no longer comment or DM the Page | Only for repeated harassment after a Hide |

Doctrine: **prefer Hide over Delete**. Hidden comments don't trigger the author to recomment angrily.

Maintain `<WORKSPACE_DIR>/memory/fb-banned-users.md` with one row per ban, the date, and the trigger comment URL.

### Selectors quick-reference (FB-specific)

| Element | Selector |
|---|---|
| Messenger DM textbox | `[contenteditable='true']` |
| Messenger DM send | `press Enter` |
| Messenger "Mark as Done" | `[aria-label*='Mark as done'], [aria-label*='Marquer comme termin']` |
| Page-comment textarea | `textarea[placeholder*='comment'], textarea[placeholder*='commentaire']` |
| Page-comment send | the SVG arrow button to the right of the textarea |
| Comment "Hide" | `[aria-label*='Hide'], [aria-label*='Masquer']` (in the comment overflow menu) |
| Comment "Delete" | `[aria-label*='Delete'], [aria-label*='Supprimer']` |
| Ban user from Page | per-user overflow → "Ban" / "Bloquer" |

### Exit codes (recommended convention)

Same as `instagram-account-operations` §9.

### Gotchas

- **Page Quality drop after a single misstep**: FB is more aggressive on Pages than on IG accounts. A handful of hidden-by-FB-automod comments can drop Page Quality from green to yellow within 24 h. Audit weekly.
- **Localized labels**: `Reply` / `Répondre`, `Hide` / `Masquer`, `Delete` / `Supprimer` — maintain a label map.
- **MBS "as Page" indicator**: a tiny chip at the top-right shows you're replying as the Page (not as your personal admin account). Verify on every cron — sometimes MBS reverts to the personal account after a session refresh.
- **Cron timeout**: ≥ 1200 s — MBS pages on FB-comments tab can take 5-8 s to render fully.

---

## 10. Page state management

File: `<WORKSPACE_DIR>/memory/fb-state.md`

For each day:
- Phase (A / B).
- Followers count.
- Page Quality score (green/yellow/red).
- Last Page-level warning / Restriction.
- Posts published today.

File: `<WORKSPACE_DIR>/memory/fb-banned-users.md`
File: `<WORKSPACE_DIR>/memory/fb-clients-known.md`

Update at the end of every run that touched a moderation action.

---

## 11. Recovery & blockers

| Issue | Action |
|-------|--------|
| `status: stopped` | Report, stop. |
| Login form on MBS | Session expired, alert, stop. |
| Page Quality drops to yellow | Flip to Phase A. Alert. Audit hidden / deleted comments. |
| Page Quality drops to red | Stop all crons. Manual review. Likely a posting policy violation. |
| "Page restricted" banner | Stop all outbound activity. Inbound DM reply only if MBS allows. Alert. |
| MBS "Something went wrong" | Refresh once. Persist → stop and alert. |
| Comment "Reply" causes page navigation | Use `@username` workaround. |
| Personal admin account in "review" status | Stop. Pages are admin-owned — if the admin is restricted, the Page is at risk. |

---

## 12. Mandatory recap (alert channel + memory)

Same format as `instagram-account-operations` §12, with `Page Quality: green/yellow/red` added to the recap line.

---

## 13. Memory files inventory

| File | Purpose | Update cadence |
|------|---------|----------------|
| `fb-recaps.md` | Per-run logs | Every cron run |
| `fb-post-log.md` | Page posts (URL, type, date, reach) | Each posting run |
| `fb-reply-log.md` | DM + comment replies sent | Each reply pass |
| `fb-state.md` | Daily phase + Page Quality + warnings | Daily Metrics Recap |
| `fb-banned-users.md` | Users banned from the Page | Each ban |
| `fb-clients-known.md` | Existing clients to NEVER pitch | Ad hoc |
| `fb-ideas.md` | Content backlog | Weekly Planning |
| `fb-learnings.md` | Patterns (what reached, what got hidden) | Weekly + ad hoc |
| `fb-alerts-sent.md` | Anti-doublon hot-lead alerts | Each alert |

---

## 14. Account identity guardrails

- The Page persona is the brand — speak as the brand, sign as the brand.
- Page admins: never reply from the personal profile under a Page post. Always switch the "Posting as" dropdown to the Page.
- Bio (Page About): one paragraph + the single `<PRIMARY_CTA>` link. No emoji walls.
- Never reply to a DM that asks for expert-grade advice on a specific case — redirect to `<PRIMARY_CTA>`.
- Never share private client details on a public comment.
- Never reuse strict CRM templates as Page content.
- Never promise an outcome.
- Never charge or solicit payment via Page Messenger (compliance + Page restrictions).
- If asked "are you a bot?": sober ambiguous line + redirect.

---

## 15. Phase A → Phase B transition

When the Daily Metrics Recap detects (page_age_days ≥ 30) AND (followers ≥ 100) AND (page_quality = green) AND (no warning in 30 d):

1. Append to `fb-state.md`: `YYYY-MM-DD - phase=A - PHASE_B_THRESHOLD_REACHED`.
2. Send a distinct alert: `🎉 FB Page ready for Phase B — flip outbound crons manually after review`.
3. Manual user flip.
4. First week of Phase B: cap reply pass at **4 replies/run**.
5. Daily check on Page Quality. Any drop reverts to Phase A.

---

## 16. Stability discipline

- Read the UI before clicking.
- Verify "Posting as: <Page>" on every cron run.
- One click → verify with a snapshot.
- Close stale tabs at the end of every run.
- Never fake a successful reply.

**Better silence than spam. Better a blockage report than a fake success.**

---

## 17. First-run checklist

- [ ] Section 0 placeholders filled.
- [ ] FB Page created, classified correctly (Business, Local Business, Professional Service, etc.).
- [ ] Page linked to a Meta Business asset (MBS → Business Settings → Pages → Add).
- [ ] `<META_BUSINESS_ID>`, `<META_ASSET_ID>`, `<FB_PAGE_ID>` extracted.
- [ ] Page About + intro: one paragraph + single `<PRIMARY_CTA>` link.
- [ ] Browser profile launched, logged into facebook.com.
- [ ] Navigating to MBS `inbox/messenger` renders the conversation list.
- [ ] Page Quality score = green.
- [ ] `<WORKSPACE_DIR>/memory/` exists with the 9 memory files.
- [ ] Alert channel webhook tested.
- [ ] Phase A confirmed: only inbound DM cron enabled.
- [ ] At least 14 days of manual posting + replies before turning on the cron.

Init memory:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && touch fb-recaps.md fb-post-log.md fb-reply-log.md fb-state.md fb-banned-users.md fb-clients-known.md fb-ideas.md fb-learnings.md fb-alerts-sent.md
```

---

## 18. FAQ

**Q: Do I need OpenClaw to use this skill?**
A: No. OpenClaw browser CLI is the example stack — the doctrine works with Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool.

**Q: Can I use the Facebook Pages API instead?**
A: Partially. The Pages API + Conversations API covers Messenger sending (within and outside the 24h window via message tags), comment moderation, and Page posting. The doctrine in this skill is the **fallback for accounts without API access, or for cases where MBS UI features are essential** (Page Quality dashboard, link previews, audience insights).

**Q: My Page got restricted during testing. What now?**
A: Stop everything. Manual review of the last 50 actions in `fb-reply-log.md`. Wait for the restriction to expire (or appeal manually). Once cleared, restart at Phase A with stricter quotas.

**Q: Does this cover Facebook Groups?**
A: Only if you own the group (the Page is the admin). Replying as the Page in a third-party group requires the group setting "Allow Pages to post" — most groups do not allow this. Default: skip groups.

**Q: What about Marketplace / Events / Shop?**
A: Out of scope. Marketplace and Shop have separate UIs and separate sanction patterns; Events run through the standard Page + Ads stack but with a manual posting cadence.

**Q: Boost vs Ads Manager — which does this skill cover?**
A: Neither. Both are out of scope. This skill is organic + reactive ops only.

**Q: What if my admin account is suspended (not just the Page)?**
A: Stop everything. A suspended admin account puts the Page at risk. Manual review only. Document the last 20 admin-account actions, not just Page actions, in `fb-learnings.md`.
