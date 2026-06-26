# amber-hunter Release Checklist

Every version bump (even patch releases) must update these files:

## 1. `amber_hunter.py` — version strings
```
Line ~3:   # Amber-Hunter vX.Y.Z  (header comment)
Line ~405: app = FastAPI(title="Amber Hunter", version="X.Y.Z")
Line ~1802: "version": "X.Y.Z",  (status endpoint)
Line ~1819: "version": "X.Y.Z",  (root endpoint)
```

## 2. `SKILL.md` — documentation
```
Header line: > Version: X.Y.Z | YYYY-MM-DD
Section header: ## API Endpoints (vX.Y.Z)
Any inline (vX.Y.Z) annotations added for new endpoints
```

## 3. `CHANGELOG.md` — release history
```
Add new entry at TOP:
## [vX.Y.Z] — YYYY-MM-DD
### Added / Fixed / Changed...
---
(existing entries below)
```

## DO NOT Change (historical record only)
- Version comments in `core/db.py` — e.g., `# v1.2.8+: ...`
- Version comments in `proactive/scripts/proactive-check.js`
- Section comment version markers in `amber_hunter.py` — e.g., `# ── v1.2.8: ...`

## Update If Applicable
- `install.sh` — only if install process changed
- `CLAUDE.md` — only if security practices changed
- User-facing docs in `amber-site/` — only if UI/UX changed
- `onboarding.html` — only if onboarding flow changed

## Security Check Before Release
```bash
# Verify no hardcoded credentials
grep -r "ghp_\|sk-\|YOUR_KEY\|api_key.*=" . --include="*.py" --include="*.sh" | grep -v ".git"
# Confirm no personal paths
grep -r "/Users/leo\|/home/leo\|anKe\|ankechen" . --include="*.py" --include="*.sh" | grep -v ".git"
```
