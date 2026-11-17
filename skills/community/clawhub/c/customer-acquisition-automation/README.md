# Customer Acquisition Automation

A desk for collecting public pain-point posts, writing a day's drafts, and parking them in an approval queue. You decide what goes out. The skill does not log into Reddit or X for you, and it does not promise signups.

Typical loop: public leads → channel-native drafts → you confirm → you (or an official API you already set up) send.

## Install

Copy the `customer-acquisition-automation` folder into your agent's skills directory:

- Claude Code: `~/.claude/skills/`
- Codex: `~/.codex/skills/`
- Cursor: `~/.cursor/skills/`

Then say: run today's acquisition pipeline.

## What you get

A CSV lead pool with source URLs, a markdown draft file, and an approval table. Nothing is posted until you say so.

## What you need

Web search and, if you want publishing later, the official API credentials for that network — stored as environment variables, never in this repo.

## Rights

Leads must come from public pages. Drafts are AI-assisted; you are the sender. Do not scrape private contacts. Do not invent prices, gifts, or reviews.

## Full version

This repo is the free lite skill: the core loop (collect → write → approve) only.

The full version on Agensi adds:

- The complete 5-layer pipeline including publish logging and next-day feedback tracking
- Channel-native copy template library (Reddit posts/comments, X threads, outreach DMs, competitor replies)
- Daily approval queue formats (≤10 minutes/day)
- Ready-made CSV templates for lead pool, approval log, publish log, and feedback log
- Compliance rules reference (anti-spam, platform ToS, ad law)

Get it on Agensi: `<AGENSI_SKILL_URL>` — $5.99 one-time, includes future updates.

## More from the same creator

- [ZeroUploadPDF](https://www.zerouploadpdf.dev) — private PDF upload and sharing
- [NoteSpark](https://notespark.dev) — AI note-taking
- [TokSpark](https://tokspark.dev) — content research for AI video

⭐ Star this repo if it saved you time — it helps other creators find it.

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Commercial use is allowed. Credit the source and keep derivatives under the same license.

## Version

0.1.0 — 2026-08-19. Public lite skill (collect → write → approve).
