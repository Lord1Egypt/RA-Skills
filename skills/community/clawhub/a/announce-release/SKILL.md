---
name: announce-release
description: Turn git commits, a changelog or release notes into launch announcement posts and schedule them with Auto Poster AI. Use when the user ships a release, feature or fix and wants to announce it on social media, from a coding agent or terminal.
---

# Announce a release on social media

Uses the Auto Poster AI MCP tools (`autoposter_*`) plus the local repository.

## Workflow

1. **Find the changes.** Use the tag or range the user gave. Otherwise run `git describe --tags --abbrev=0` and read `git log <last-tag>..HEAD --oneline`. Also read `CHANGELOG.md` or the release notes if they exist.
2. **Filter for users.** Keep changes a user would notice: new features, big fixes, speed gains. Drop refactors, dependency bumps, CI and test commits. If nothing is user-facing, say so and stop.
3. **Lead with the best change.** Pick one headline. Mention at most two more.
4. **Write the posts.** Plain language, what it does for the user, not how it is built. Include the version and the release or docs link if the user gave one. Do not invent a link.
5. **Match the audience.** Developer tool: X, LinkedIn, Bluesky, Threads. Consumer product: add Instagram, TikTok or Facebook, and say if a visual is needed.
6. **Call `autoposter_list_accounts` and `autoposter_get_rules`**, then hand off to `schedule-social-posts` to draft or schedule. Default to draft.

## Rules

- Never post secrets, internal URLs, unreleased feature names or customer names found in commits.
- Do not claim performance numbers that are not in the commits or notes.
- One release, one set of posts. Do not announce the same release twice: check `autoposter_list_posts` with `search` set to the version first.
