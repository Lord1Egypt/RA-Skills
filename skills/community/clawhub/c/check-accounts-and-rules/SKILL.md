---
name: check-accounts-and-rules
description: Show which social accounts are connected to Auto Poster AI, who is signed in, and each platform's character limits and media rules. Use when the user asks what accounts they have, which platforms are connected, which workspace this is, or whether a post fits a platform's limits.
---

# Check accounts, profile and platform rules

Uses `autoposter_list_accounts`, `get_profile` and `autoposter_get_rules`.

## Tasks

- **Which accounts are connected:** `autoposter_list_accounts`. Show platform, account name and ID in a short table. The IDs are what the posting tools need.
- **Who am I signed in as:** `get_profile`. Returns the profile for the current credentials. Use it to confirm the right user and workspace before posting.
- **Will this fit:** `autoposter_get_rules`. Gives character limits, media format requirements and guidelines per platform. Compare the user's text against the limit and report the count and the limit. Offer a shortened version if it is over.
- **Which platform can do X:** answer from the rules output (video length, image count, formats), not from memory.

## Rules

- Platforms and limits change. Always read them from the tools, never quote a limit from memory.
- If `autoposter_list_accounts` returns nothing, tell the user to connect an account in Auto Poster AI. You cannot connect accounts.
- If the expected platform is missing, say so. Do not post to a different platform instead.
