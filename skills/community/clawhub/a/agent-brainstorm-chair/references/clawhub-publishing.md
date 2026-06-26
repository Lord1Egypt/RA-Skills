# ClawHub Publishing — Pitfalls & Workflow

Captured during agent-brainstorm-chair v1.0.0 publishing attempt (2026-05-10).

---

## Prerequisites

### 1. Authentication

```bash
clawhub login           # opens browser for GitHub OAuth
clawhub whoami          # verify: should return username
```

Token stored at: `~/Library/Application Support/clawhub/config.json`

### 2. License Acceptance (WEB-ONLY, FIRST-TIME)

⚠️ **Critical pitfall:** First-time publishers MUST accept the MIT-0 license
through the ClawHub web UI. The CLI has no `--accept-license` flag and
the check is server-side.

**Symptoms if not accepted:**
```
$ clawhub publish ./my-skill ...
- Preparing my-skill@1.0.0
✖ MIT-0 license terms must be accepted to publish skills
Error: MIT-0 license terms must be accepted to publish skills
```

**Solution:**
1. Visit https://clawhub.ai
2. Click "Sign in with GitHub" (top right)
3. After login, the license acceptance page should appear
4. Accept and return to CLI

The license check happens before any file upload — the error appears instantly
even with `--no-input` or piped stdin.

### 3. CLI Detection

The `clawhub` binary is typically at `/opt/homebrew/bin/clawhub` (macOS Homebrew)
or `~/.local/bin/clawhub` (Linux). If not found:

```bash
export PATH="/opt/homebrew/bin:$PATH"
# or install:
brew install openclaw/tap/clawhub
```

---

## Publish Command

```bash
clawhub publish <path-to-skill-folder> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <semver> \
  --changelog "<changes>"
```

The path must be a folder containing at minimum a `SKILL.md` with YAML frontmatter.

### Frontmatter Requirements

```yaml
---
name: <slug>
description: "<one-line>"
metadata:
  clawhub:
    tags: [tag1, tag2]
    ecosystems: [hermes, openclaw]
    auto_detect: true
---
```

### Post-Publish Verification

```bash
clawhub inspect <slug>      # verify metadata
clawhub search <slug>       # should appear in results
```

### Update Existing Skill

```bash
clawhub publish ./skill-dir --slug <slug> --version <new-version> --changelog "..."
```

---

## API Reference

### List Skills

```bash
curl -s "https://clawhub.ai/api/v1/skills" | jq '.items[] | {slug, displayName, tags}'
```

### Inspect Skill

```bash
clawhub inspect <slug>
```

---

## Known Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| License not accepted | "MIT-0 license terms must be accepted" | Accept via web UI |
| Path not a folder | "Path must be a folder" | Use absolute path |
| Token expired | "Unauthorized" | `clawhub login` again |
| `clawhub: command not found` | Shell error | Install or add to PATH |
| `__pycache__` uploaded | Wasted bytes | `find . -name '__pycache__' -exec rm -rf {} +` before publish |
