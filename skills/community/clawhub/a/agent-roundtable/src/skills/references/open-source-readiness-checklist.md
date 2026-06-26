# Roundtable Open-Source Readiness Checklist

Identified during pre-release review on 2026-05-21. Repository: `/Users/parsifal/Repo/Monorepo/roundtable/`

## 🔴 Must Fix Before Release

### 1. No LICENSE file
README says MIT but no actual LICENSE file in repo. Add `LICENSE` with MIT text.

### 2. Hermes-specific files in repo
These files are Hermes-only and confuse non-Hermes users. Move to a `hermes/` subdirectory or remove from the public repo:
- `src/hermes_cli/roundtable_db.py` — legacy Hermes DB wrapper (replaced by `roundtable.db`)
- `src/tools/roundtable_tools.py` — legacy Hermes tools (replaced by `adapters/hermes.py`)
- `src/toolsets.py` — Hermes toolset config
- `src/skills/SKILL.md` — Hermes skill definition
- `tests/hermes_cli/` — tests for legacy DB
- `tests/tools/` — tests for legacy tools

**Note**: `adapters/hermes.py` IS the correct Hermes integration point and should stay. The above are legacy files from before the standalone refactor.

### 3. build-backend is non-standard
```toml
# Current (broken on some pip versions):
build-backend = "setuptools.backends._legacy:_Backend"

# Should be:
build-backend = "setuptools.build_meta"
```

### 4. .gitignore too minimal
Only has `__pycache__/`. Add:
```
.pytest_cache/
*.egg-info/
dist/
build/
.eggs/
*.pyc
*.pyo
.env
.venv/
venv/
*.db
```

### 5. Internal docs shouldn't be public
Remove or move to a private repo:
- `docs/OPC-EXPERIENCE-REPORT.md` — internal team experience report
- `docs/product/PRD.md`, `ACCEPTANCE-REPORT.md` — internal product docs
- `docs/TECH-DESIGN.md`, `TEST-RESULTS.md` — internal technical docs

Keep: `docs/API.md`, `docs/INTEGRATION.md` — these are user-facing.

## 🟡 Should Fix (Usability)

### 6. Generic adapter missing features
`adapters/generic.py` doesn't support:
- `notifications` parameter in `init()`
- `send_fn` callback
- `advance()` method
- `roundtable_notify()` method

Non-Hermes users can't use notifications or manual round advancement.

### 7. `roundtable_notify` and `roundtable_advance` not in public API
`__init__.py` doesn't export these. Add to `__all__` or document as adapter-only.

### 8. README needs expansion
Missing:
- PyPI badges (version, tests, license)
- Integration examples for LangChain, AutoGen, CrewAI, generic Python
- Notifications feature documentation
- Contributing guide
- Changelog

### 9. Tests depend on Hermes
`tests/tools/test_roundtable_tools.py` imports `from tools.registry import registry` — fails without Hermes installed. Mark as `pytest.mark.skipif` or move to `tests/hermes/`.

## Package Structure (Target)

```
roundtable/
├── LICENSE                    # MIT
├── README.md                  # User-facing docs
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # How to contribute
├── pyproject.toml             # Build config (fix backend)
├── .gitignore                 # Comprehensive
├── src/roundtable/            # Core package only
│   ├── __init__.py
│   ├── core.py
│   ├── db.py
│   ├── models.py
│   ├── exceptions.py
│   ├── notify.py
│   └── adapters/
│       ├── __init__.py
│       ├── generic.py         # Framework-agnostic API
│       └── hermes.py          # Hermes Agent adapter
├── tests/                     # Core tests only (no Hermes deps)
├── docs/
│   ├── API.md                 # Python API reference
│   ├── INTEGRATION.md         # Framework integration guides
│   └── NOTIFICATIONS.md       # Notification system docs
└── examples/
    ├── basic.py               # Simple standalone usage
    ├── with_notifications.py  # Notifications example
    └── hermes_profile.yaml    # Hermes config example
```
