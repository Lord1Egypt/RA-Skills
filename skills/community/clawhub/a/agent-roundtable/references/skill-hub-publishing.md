# Skill Hub & Package Publishing Notes

Use this checklist when preparing `agent-roundtable` for **ClawHub / OpenClaw**, **Hermes Skill Hub**, and **PyPI** releases.

## 1. Authoritative Files & Sync

- **Skill source of truth**: `src/skills/SKILL.md` (`name: agent-roundtable`, `version: <semver>` matching `package.json` and `pyproject.toml`)
- **Synced root copy**: `SKILL.md` (auto-generated via `./scripts/sync_skill.sh src2root`; `references/` is rewritten to `src/skills/references/`)
- **Wheel-bundled MCP skill**: `src/roundtable/skills/mcp-roundtable/SKILL.md` (`name: mcp-roundtable`)
- **ClawHub ignore file** is `src/skills/.clawhubignore`. Both ClawHub and Hermes Skill Hub publish the self-contained `src/skills/` bundle.

Always edit `src/skills/SKILL.md`, then sync and verify:

```bash
./scripts/sync_skill.sh src2root
./scripts/sync_skill.sh check
```

Keep the skill bundle generic and secret-free: never commit private chat IDs, bearer tokens, webhook URLs, local `/Users/...` paths, or internal acceptance artifacts.

## 2. Automated Release Gate (Recommended)

Run the repository preflight gate before tagging or publishing:

```bash
scripts/release/preflight-check.sh
```

> Note: Ensure `package.json`, `src/roundtable/web/package.json`, `pyproject.toml`, `src/roundtable/__init__.py`, `SKILL.md`, and `src/skills/SKILL.md` all carry the exact same version before running `preflight-check.sh` or tagging `vX.Y.Z` (`.github/workflows/release.yml` runs on `v*` tags).

## 3. Manual Channel Commands & Pitfalls

```bash
hermes skills publish --help
clawhub publish --help
clawhub whoami
```

- **Hermes Skill Hub**:
  ```bash
  hermes skills publish src/skills --to github --repo <target-repo>
  ```
- **ClawHub / OpenClaw** (from repo root, matching `release.yml`):
  ```bash
  clawhub publish src/skills --slug agent-roundtable --name "Roundtable" --version "<version>" \
    --tags discussion,multi-agent,collaboration,code-review,roundtable
  ```
  - **MIT-0 license gate**: `clawhub publish` requires server-side MIT-0 acceptance on the ClawHub website for the logged-in account (no `--accept-license` CLI flag exists).
  - **PyPI (`agent-roundtable`)**: Built separately via `python -m build` and uploaded via `twine upload dist/*` (automated in `.github/workflows/release.yml`).

## 4. Hygiene Validation Snippet

```bash
python3 - <<'PY'
from pathlib import Path
import re

for path in [Path("src/skills/SKILL.md"), Path("SKILL.md")]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n") and "\n---\n" in text[4:], f"missing frontmatter in {path}"
    for key in [
        "name: agent-roundtable",
        "description:",
        "version:",
        "platforms:",
        "metadata:",
        "hermes:",
        "openclaw:",
        "requires:",
    ]:
        assert key in text, f"{path}: missing {key}"
    for pat in [r"Bearer\s+[A-Za-z0-9._-]+", r"oc_[0-9a-f]{20,}", r"ou_[0-9a-f]{20,}", r"sk-[A-Za-z0-9]{20,}"]:
        assert not re.search(pat, text, flags=re.I), f"{path}: secret-like pattern {pat}"
print("SKILL.md hygiene OK")
PY
```

## 5. Authorization Gate

Never execute a live publish without explicit user confirmation of:
1. Target ClawHub / PyPI account authentication (`clawhub whoami` / Trusted Publisher).
2. Target Hermes Skill Hub GitHub repository.
3. Organization vs. personal ownership.
