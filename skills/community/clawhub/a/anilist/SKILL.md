---
name: anilist-cli
version: 0.3.2
description: CLI for searching, retrieving anime and manga information, interacting with user profile and lists on Anilist, and more.
allowed-tools: Bash
emoji: 📺
metadata:
  openclaw:
    install:
      - kind: node
        package: "@mtsku/anilist-cli"
        bins: [anilistcli]
    requires:
      bins: [node]
---

# AniList CLI Skill

Use this skill for direct AniList CLI workflows. This guide is for LLM/agent execution only.

## Installation Check

1. Check availability:
   - `command -v anilistcli`
2. If missing, install:
   - `npm install -g @mtsku/anilist-cli`
3. Verify:
   - `anilistcli --help`

## Command Map

- Discovery:
  - `anilistcli discover seasonal --season WINTER --year 2026 -n 20`
  - `anilistcli discover upcoming -n 15`
- Airing:
  - `anilistcli airing upcoming --hours 48 -n 25`
  - `anilistcli airing next "<title>"`
  - `anilistcli airing mine --hours 72 --limit 50`
- Search/media:
  - `anilistcli search anime "<query>" -n 5`
  - `anilistcli media recs "<title>" -n 10`
  - `anilistcli media relations "<anilist-url-or-title>"`
- Profile/social:
  - `anilistcli profile [username]`
  - `anilistcli friends [username] -n 50`
- List management:
  - `anilistcli mine summary --hours 72 -n 10`
  - `anilistcli list view --type anime --status-in "CURRENT,PLANNING"`
  - `anilistcli planning add "<title>"`
  - `anilistcli status set "<title>" CURRENT`
  - `anilistcli progress set "<title>" 12`

## Auth Setup

- Set token:
  - `anilistcli auth set-token "<token>"`
- Verify auth:
  - `anilistcli auth where`

## Output Mode

- Use `--json` for machine-readable output.
- Public read endpoints work without auth.
- For mutations, run `--dry-run` first unless explicit write execution is requested.
- Quote title inputs that include spaces.
