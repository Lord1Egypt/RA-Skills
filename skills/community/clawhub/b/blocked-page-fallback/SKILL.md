---
name: blocked-page-fallback
description: Recover when a web page is thin, blocked, JS-heavy, region-limited, or fetch-incompatible by switching to lawful fallback paths instead of stopping early.
---

# Blocked Page Fallback

Use this skill when normal web fetch/search is not enough, but the goal may still be reachable through alternate lawful paths.

## Do Not Do

- do not bypass login
- do not evade anti-bot or access controls
- do not brute-force endpoints

## Fallback Ladder

### 1. Broaden discovery

- search multiple engines
- use site-specific search
- try alternate titles, aliases, slugs, and locale variants

### 2. Switch transport

- if plain fetch is thin, use a browser-rendered path
- if browser path is noisy, pivot back to targeted fetch on discovered links

### 3. Pivot source types

Try allowed alternatives:

- official docs or help centers
- official API or export surfaces
- feeds, sitemaps, changelogs, or release notes
- search-engine cached snippets where available
- public mirrors or archive copies that are openly reachable
- reputable secondary databases

### 4. Use structural clues

If the exact page is blocked, search by:

- page title fragments
- quoted snippets
- IDs, handles, usernames, product codes, or canonical names
- internal link labels and breadcrumb terms

### 5. Keep going until confidence is earned

Do not stop after:

- one blocked fetch
- one empty browser render
- one weak search pass

Stop when:

- authoritative or converging sources answer the question
- the remaining blocker is concrete and real
- additional paths are now duplicative

## Output Pattern

Return:

1. primary path that failed
2. fallback paths attempted
3. which fallback produced signal
4. best answer now available
5. what would require user-authorized login or a first-party API
