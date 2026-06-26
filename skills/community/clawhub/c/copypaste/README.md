# copypaste-cloud

An [OpenClaw](https://openclaw.ai) skill for [copy-paste.cloud](https://copy-paste.cloud) — a fast, public pastebin with syntax highlighting and group sharing.

## What it does

| Action | Script | API key required |
|--------|--------|-----------------|
| Get 10 recent public pastes | `scripts/get_recent.sh` | Yes |
| Get any paste by ID | `scripts/get_paste.sh <id>` | No (public); Yes (private/group) |
| Create a new paste | `scripts/create_paste.sh --content "..."` | Yes |

## Setup

1. Sign in at [copy-paste.cloud](https://copy-paste.cloud)
2. Go to [copy-paste.cloud/developer](https://copy-paste.cloud/developer)
3. Generate your API key
4. Export it in your shell:

```bash
export COPYPASTE_API_KEY=cp_your_key_here
```

## Usage examples

```bash
# See what's been shared recently
bash scripts/get_recent.sh

# Read a specific paste
bash scripts/get_paste.sh 3f2a1c9e-0000-0000-0000-000000000000

# Share a file
bash scripts/create_paste.sh --content "$(cat myfile.py)" --language python --title "My script"

# Quick one-liner
bash scripts/create_paste.sh --content "Hello, world!"

# Temporary paste — gone in 24 hours
bash scripts/create_paste.sh --content "temp stuff" --expires-in-hours 24

# Burn after read
bash scripts/create_paste.sh --content "secret snippet" --burn-after-read
```

## Requirements

- `curl`
- `jq`
- `python3` (used only for URL-encoding passwords in `get_paste.sh`)

## License

MIT-0 — no attribution required.
