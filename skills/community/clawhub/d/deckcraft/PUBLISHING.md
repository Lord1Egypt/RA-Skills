# Publishing DeckCraft to ClawHub

How to publish a new version of DeckCraft.

## Prerequisites

1. **ClawHub CLI installed**:
   ```bash
   npm install -g clawhub
   ```

2. **Logged in**:
   ```bash
   clawhub login
   clawhub whoami  # confirm
   ```

## Pre-publish checklist

Run all checks before publishing:

```bash
# 1. All tests pass
python3 tests/test_smoke.py        # 95 layout × canvas tests
python3 tests/test_validation.py   # 20 input validation tests
python3 tests/test_importers.py    # 34 importer tests (v5.3+)

# 2. All examples work
python3 examples/01_basic_cover_to_closing.py
python3 examples/02_multi_canvas.py
python3 examples/03_from_outline_json.py
python3 examples/04_from_source.py     # v5.3+

# 3. CLI works
python3 scripts/generate_ppt.py --list-themes
python3 scripts/generate_ppt.py --list-canvases
python3 scripts/generate_ppt.py -i examples/03_outline.json -o /tmp/cli_test.pptx
python3 scripts/import_source.py --help    # v5.3+

# 4. No personal info or local paths
grep -rn "天天\|毛毛\|simon\|@user\|localhost" .  # should be empty
grep -rn "/home/\|/Users/" .                        # should be empty (only test files)
```

## Version bump

Update version in:

- `SKILL.md` (line: `**Version**: X.Y.Z`)
- `CHANGELOG.md` (new section header)
- `engine/__init__.py` (if applicable)
- This file (`PUBLISHING.md`)

Use [SemVer](https://semver.org/):
- **MAJOR** (5.x → 6.x): breaking API changes
- **MINOR** (5.1 → 5.2): backward-compatible new features
- **PATCH** (5.1.0 → 5.1.1): bug fixes, no new features

## Build & validate

Before publishing, do a clean test:

```bash
# Fresh install
pip install -r requirements.txt

# Run all tests
python3 -m pytest tests/  # if pytest installed
# or
python3 tests/test_smoke.py && python3 tests/test_validation.py
```

## Publish

```bash
clawhub publish ./deckcraft \
  --slug deckcraft \
  --name "DeckCraft" \
  --version 5.2.0 \
  --changelog "v5.2.0: Multi-canvas support (16:9/9:16/1:1/4:3/A4), input validation, 95+20 tests, MIT license, README/MIGRATION docs"
```

The CLI will:
1. Hash local files
2. Resolve any matching published version
3. Upload new version to the registry
4. Confirm success with the new version URL

## Post-publish

1. **Verify the listing**:
   ```bash
   clawhub search "deckcraft"
   clawhub list  # confirm in installed skills
   ```

2. **Test install** in a fresh environment:
   ```bash
   clawhub install deckcraft --version 5.2.0
   python3 -c "from engine import DeckEngine; eng = DeckEngine(canvas='9:16'); eng.cover(title='Hello'); eng.save('/tmp/test.pptx')"
   ```

3. **Update local** (if you have it installed via ClawHub):
   ```bash
   clawhub update deckcraft
   ```

## Versioning policy

- **Patch releases** (5.2.0 → 5.2.1): bug fixes only, automatic
- **Minor releases** (5.2 → 5.3): new features, must pass all tests, must update CHANGELOG
- **Major releases** (5 → 6): breaking changes, must update MIGRATION.md, may require user action

## Rollback

If a release is broken:

1. Fix the issue in source
2. Bump version (5.2.0 → 5.2.1) — never overwrite
3. Re-publish
4. Notify users via CHANGELOG

You cannot delete a published version from ClawHub, only supersede it.
