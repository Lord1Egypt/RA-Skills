# Portability Checklist

Use this checklist when building or reviewing skills for cross-agent compatibility.

## Must-Have (fail if missing)

- [ ] **No hardcoded paths in scripts** — use `$SKILL_DATA_DIR` + fallback
- [ ] **XDG fallback** — `~/.config/<skill-name>/` as default when `$SKILL_DATA_DIR` is unset
- [ ] **Credentials support env var** — token/key available via environment variable
- [ ] **Output to stdout** — no platform messaging API calls

## Should-Have (warn if missing)

- [ ] **Credential files have `chmod 0o600`** — owner read/write only
- [ ] **SKILL.md uses `<DATA_DIR>` placeholder** — not platform-specific paths
- [ ] **Setup scripts support `--no-browser`** — for headless/SSH machines
- [ ] **User-Agent is generic** — no platform names

## Info (flag for awareness)

- [ ] **Platform CLI dependencies documented** — e.g. "requires `clawhub` CLI"
- [ ] **No platform SDK imports** — pure stdlib + common packages

## The Pattern

```python
import os

# Data dir resolution
DATA_DIR = os.path.expanduser(
    os.environ.get("SKILL_DATA_DIR", "~/.config/my-skill")
)
CREDS_PATH = os.path.join(DATA_DIR, "credentials.json")

# Save with restricted permissions
def save_credentials(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CREDS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(CREDS_PATH, 0o600)

# Env var override for tokens
def get_token():
    return os.environ.get("MY_TOKEN") or load_from_file(CREDS_PATH)
```
