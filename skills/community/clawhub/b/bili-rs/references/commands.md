# bili-rs CLI Commands Reference

Global flags (all subcommands): `--json`, `--yaml`

## Account

| Command | Auth | Notes |
|---------|------|-------|
| `bili login` | None | QR scan → save credential |
| `bili logout` | None | Delete credential file |
| `bili status` | None | Exit 0=logged in, 1=not. `data.authenticated` |
| `bili whoami` | Read | `data.{user, relation.{following,follower}}` |

## Video

```
bili video <BV_OR_URL> [--subtitle/-s] [--subtitle-timeline/-t]
                       [--subtitle-format timeline|srt]
                       [--comments/-c] [--ai] [--related/-r]
```

Auth: Optional (`--ai` needs login). BV extraction regex: `\bBV[0-9A-Za-z]{10}\b`

Output `data`:
```yaml
video: {id, bvid, aid, title, description, duration, url, owner, stats}
subtitle: {available, format, text, items}   # only with -s/-t
ai_summary: "..."                             # only with --ai, needs login + WBI
comments: [...]                               # only with -c, top 10
related: [...]                                # only with -r
warnings: []
```

## User & Search

| Command | Notes |
|---------|-------|
| `bili user <UID_OR_NAME>` | Pure digits → UID lookup; else search first match |
| `bili user-videos <UID_OR_NAME> [-n MAX]` | Default max 10 |
| `bili search <KW> [--type user\|video] [-p PAGE] [-n MAX]` | Default type: user |

## Discovery

| Command | Notes |
|---------|-------|
| `bili hot [-p PAGE] [-n MAX]` | Hot videos |
| `bili rank [--day 3\|7] [-n MAX]` | Rankings |

## Collections

| Command | Notes |
|---------|-------|
| `bili favorites [FAV_ID] [-p PAGE]` | No FAV_ID → list folders; with ID → list videos |
| `bili following [-p PAGE]` | Following list |
| `bili history [-p PAGE] [-n MAX]` | Watch history |
| `bili watch-later` | Watch later list |
| `bili feed [--offset CURSOR]` | Dynamic feed |
| `bili my-dynamics [--offset N] [--top] [-n MAX]` | My dynamics |
| `bili dynamic-post [TEXT] [--from-file PATH]` | TEXT or --from-file required |
| `bili dynamic-delete <ID> [--yes]` | Prompts confirmation without --yes |

## Interactions (all need Write auth)

| Command | Notes |
|---------|-------|
| `bili like <BV_OR_URL> [--undo]` | Like/undo-like |
| `bili coin <BV_OR_URL> [-n 1\|2]` | Add coins |
| `bili triple <BV_OR_URL>` | Like + coin + favorite |
| `bili unfollow <UID> [--yes]` | Prompts confirmation without --yes |

## Audio (requires `--features audio` build)

```
bili audio <BV_OR_URL> [-s SECS] [--no-split] [-o DIR]
```

Flow: fetch cid → get DASH audio URL → stream download → symphonia decode → 16kHz mono WAV segments (`{bvid}_part001.wav` ...)
Without `--no-split`: deletes temp `.m4a` after decoding.
Output: progress bar + file paths to stderr/stdout (no structured envelope).

## Exit Codes

| Case | Code |
|------|------|
| Success | 0 |
| Error (auth fail, API error, etc.) | 1 |
