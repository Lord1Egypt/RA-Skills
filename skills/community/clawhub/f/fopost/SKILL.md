---
name: fopost
description: Draft, schedule and publish social media posts with FoPost across X, LinkedIn, Instagram, Facebook, Threads, TikTok, YouTube, Bluesky, Pinterest, Reddit, Mastodon, Discord, Slack, Telegram, Google Business and more, upload media, run the posting queue, and read analytics. Use when asked to post, schedule, queue, cross-post, check a social account or report on social performance.
homepage: https://fopost.com/docs/cli
metadata:
  openclaw:
    emoji: "📣"
    homepage: https://fopost.com/docs/cli
    primaryEnv: FOPOST_API_KEY
    requires:
      env:
        - FOPOST_API_KEY
      anyBins:
        - fopost
        - fopost-cli
    envVars:
      - name: FOPOST_API_KEY
        required: true
        description: FoPost API key, created in the dashboard under Developers → API Keys.
      - name: FOPOST_BASE_URL
        required: false
        description: API address. Leave unset to use the default.
    install:
      - kind: brew
        formula: fopost/tap/fopost
        bins: [fopost]
      - kind: go
        module: github.com/fopost/fopost-cli@latest
        bins: [fopost-cli]
---

# FoPost

FoPost publishes to every major social network from one place. This skill drives it through the
`fopost` command-line tool. Every post starts as a draft, and nothing reaches a network until the
person says so.

**Already connected to FoPost's MCP server?** If tools such as `list_accounts` and
`create_draft_post` are available, use them instead of the command line. They run the same
actions with the same approval rules.

## 1. Set up

Install the CLI if `fopost --version` fails:

```bash
brew install fopost/tap/fopost
# or, with Go installed (the binary is then named fopost-cli):
go install github.com/fopost/fopost-cli@latest
```

Authenticate with an API key. The person creates one at https://fopost.com/dashboard/api-keys
(Developers → API Keys) and gives it the scopes the task needs (`posts`, `accounts`, `labels`,
`analytics`; `publish` only if you may publish).

```bash
export FOPOST_API_KEY=fp_...   # preferred for agents, nothing is written to disk
fopost auth status             # confirms the key works and shows the workspace
```

If `auth status` fails, stop and ask for a key. Do not try any other command first.

**Always pass `--json`.** Every command takes it and prints the full resource, which is what you
parse. Tables are for people.

## 2. The approval rule

Publishing is public and cannot be taken back cleanly. So:

1. Create posts as **drafts** (the default when no schedule is given).
2. Run `fopost posts preflight <post-id>` and fix what it reports.
3. Show the person the text, the accounts and the time.
4. Only after they say yes: publish, schedule or queue it.

Never pass `--publish`, `--schedule-at` or `--schedule queue` on the first `posts create` unless
the person explicitly asked for that exact post to go out without review.

## 3. Core workflow

```bash
# Which accounts can post? Skip anything not healthy.
fopost accounts list --json
fopost accounts health --json

# Draft (text from a flag, a file or stdin)
fopost posts create --account acc_1 --account acc_2 --text "Shipping today" --json
fopost posts create --group grp_1 --text-file post.md --json
fopost posts create --account acc_1 --text "New photos" --media a.jpg --media b.png --json

# Check it against every target network
fopost posts preflight post_123 --json

# After approval, one of:
fopost posts publish post_123 --json                      # now
fopost posts publish post_123 --account acc_1 --json      # only some of its accounts
fopost posts create ... --schedule-at "2026-12-01 09:00"  # a time (local unless it carries an offset)
fopost posts create ... --schedule queue                  # the next free queue slot

# Did it go out?
fopost posts deliveries post_123 --json
```

`--publish`, `--schedule-at`, `--schedule queue` and `--draft` are alternatives; pass one.
`posts publish --dry-run` validates without sending anything.

## 4. Commands you will use most

| Task | Command |
| --- | --- |
| Workspaces the key reaches | `fopost workspaces list --json` |
| Act on another workspace | add `--workspace ws_123` to any command |
| Accounts and groups | `fopost accounts list`, `fopost account-groups list` |
| One account's own numbers | `fopost accounts metrics <account-id>` |
| List posts | `fopost posts list --status scheduled --from 2026-12-01 --to 2026-12-07 --json` |
| One post | `fopost posts get <post-id> --json` |
| Copy a post into a new draft | `fopost posts duplicate <post-id>` |
| Stop deliveries not yet sent | `fopost posts cancel <post-id>` |
| Take a live post down | `fopost posts unpublish <post-id> --yes` |
| Delete a post | `fopost posts delete <post-id> --yes` |
| Upload media first | `fopost media upload clip.mp4 --json` |
| Largest file allowed | `fopost media limits --json` |
| Queue times | `fopost queue slots list`, `fopost queue preview --count 10` |
| Add a weekly slot | `fopost queue slots create --weekday 1 --time 09:00 --timezone Europe/Berlin` |
| Labels (campaigns) | `fopost labels list`, then `posts create --label <label-id>` |
| Headline numbers | `fopost analytics overview --days 30 --json` |
| Best posts | `fopost analytics top-posts --days 30 --limit 10 --json` |
| Daily series | `fopost analytics time-series --days 30 --json` |

Destructive commands (`unpublish`, `delete`, `queue slots delete`, `media delete`) ask for
confirmation. In a script, pass `--yes`, and only after the person confirmed.

## 5. Recipes

**Same idea, several networks.** Write one draft per network shape rather than one caption for
all: a short X post, a longer LinkedIn post, a caption with hashtags for Instagram. Create each
draft for its own accounts, preflight each, then ask for one approval covering the set.

**A week of posts.** Read `fopost queue preview --count 20 --json` and
`fopost posts list --status scheduled --json` first, so you fill free slots instead of stacking
posts. Create every post as a draft, show the list (day, time, account, first line), and after
one approval schedule each with `--schedule queue` or its own `--schedule-at`.

**Media.** `--media` uploads local files to the media library and attaches them. Check
`fopost media limits` before uploading video. Video-only networks (TikTok, YouTube) need a
video; text-only networks ignore images.

**Weekly report.** `analytics overview`, `analytics top-posts` and
`posts list --status failed` for the same window. Report numbers you fetched, never estimates.

## 6. Errors and exit codes

Each failure prints one line and exits with a code you can branch on:

| Code | Meaning | What to do |
| --- | --- | --- |
| 2 | Usage error | Fix the flags; the message names the problem |
| 3 | Authentication | Key missing, wrong or revoked: ask for a new one |
| 4 | Payment required | The workspace needs a card or more balance; tell the person |
| 5 | Forbidden | The key lacks a scope (often `publish`) |
| 6 | Not found | Wrong id, or it belongs to another workspace |
| 7 | Rate limited | Wait, then retry once |
| 8 | Validation | The API rejected the content; read the message, fix the post |
| 9, 10 | Server or network | Retry once; if it fails again, report it |

`posts preflight` exits non-zero when any target is blocked; its JSON lists the issues per
account.

## 7. Network-specific settings

Reddit subreddits and flairs, YouTube playlists, Pinterest boards, TikTok music and creator
limits, Instagram Reel audio, Bluesky languages and Google Business profiles each have their
own commands. See [references/networks.md](references/networks.md).

## Links

- Docs: https://fopost.com/docs/cli
- API reference: https://fopost.com/docs/api/overview
- CLI source: https://github.com/fopost/fopost-cli
- Support: https://fopost.com/contact
