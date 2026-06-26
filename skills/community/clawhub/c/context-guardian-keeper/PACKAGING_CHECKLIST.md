# Packaging Checklist

Version target: 1.1.7

Include in published package:
- `SKILL.md`
- `README.md`
- `PACKAGING_CHECKLIST.md`
- `references/`
- `scripts/context_guardian.py`
- `scripts/test_context_guardian.py`
- `.clawhubignore`

Exclude from published package:
- `.clawhub/`
- `_meta.json`
- `__pycache__/`
- `*.pyc`, `*.pyo`
- `.pytest_cache/`, `.mypy_cache/`
- `.context_guardian/`
- temporary test output directories such as `__main___*/` and `.tmp_ctx_test*/`
- logs and one-off scratch files

Pre-publish checks:
- Runtime contract wording matches the schema/reference implementation.
- Tests pass for the current artifact.
- Verify: `python3 scripts/test_context_guardian.py` exits 0 and leaves no `__main___*` or `.tmp_ctx_test*` residuals in the skill tree.
- `.clawhubignore` excludes local runtime state and generated noise.
- Version target matches the actual package metadata or release tag; do not require a changelog file when the package does not ship one.
