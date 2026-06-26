# Roundtable Open-Source Readiness Checklist

Identified during review on 2026-05-21. Boss decided to delay release pending fixes.

## 🔴 Must Fix Before Release

1. **No LICENSE file** — README says MIT but no LICENSE file exists. Add MIT license with 摸鱼科技 / your_github_username copyright.

2. **Hermes-specific files polluting repo** — These are legacy and should be deleted:
   - `src/hermes_cli/roundtable_db.py` (old DB wrapper, replaced by adapters/hermes.py)
   - `src/tools/roundtable_tools.py` (old tools, replaced by adapters/hermes.py)
   - `src/toolsets.py` (Hermes toolset config)
   - `tests/hermes_cli/` (old tests)
   - `tests/tools/` (old tests)
   - `src/skills/SKILL.md` (Hermes skill definition — lives in ~/.hermes/skills/ separately)

3. **pyproject.toml build-backend non-standard** — Uses `setuptools.backends._legacy:_Backend`, should be `setuptools.build_meta`. Breaks on some pip versions.

4. **.gitignore nearly empty** — Only has `__pycache__/`. Needs: `.pytest_cache/`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.pyc`, `.env`, `.venv/`, `venv/`, `*.db`, `.DS_Store`, `docs/internal/`.

5. **Internal docs in public repo** — Move to `docs/internal/` and gitignore:
   - `docs/OPC-EXPERIENCE-REPORT.md`
   - `docs/product/PRD.md`, `ACCEPTANCE-REPORT.md`
   - `docs/TECH-DESIGN.md`, `docs/TEST-RESULTS.md`
   - Keep public: `docs/API.md`, `docs/INTEGRATION.md`

## 🟡 Should Fix (Usability)

6. **Generic adapter missing features** — `adapters/generic.py` lacks:
   - `notifications` parameter support
   - `send_fn` callback
   - `advance()` method
   - `notify()` method
   - Constructor should accept `send_fn` parameter

7. **Public API incomplete** — `__init__.py` doesn't export:
   - `Notifier` (from roundtable.notify)
   - `InvalidReplyToError` (from roundtable.exceptions)

8. **README needs expansion** — Missing:
   - Badges (PyPI, Tests, License)
   - Notification push feature docs
   - `advance()` / `notify()` usage examples
   - LangChain / AutoGen / CrewAI integration examples
   - Contributing guide
   - Changelog (v0.1.0)

9. **Tests import Hermes code** — `tests/test_core.py` line 45: `from roundtable.adapters.hermes import (...)`. Should be try/except or moved to separate `tests/test_hermes_adapter.py`.

## Task Status

Task `t_xxxxxxxx` assigned to 码飞, blocked until cron unblocks at 00:30.
