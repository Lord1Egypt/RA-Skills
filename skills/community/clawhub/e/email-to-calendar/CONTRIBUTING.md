# Contributing to email-to-calendar

## Development Setup

The skill is located at `~/.openclaw/workspace/skills/email-to-calendar/` and source-controlled separately from the main server config repo.

## Definition of Done (DOD)

After completing any work on this skill, you must complete ALL of the following:

### 1. Run Tests
```bash
cd ~/.openclaw/workspace/skills/email-to-calendar/scripts
./run_tests.sh
```
All 158 tests must pass before proceeding.

### 2. Update CHANGELOG.md
Document what changed with today's date, following existing format.

### 3. Bump Version
Update the `version` field in the `SKILL.md` frontmatter (the single source of
truth for the skill version).

Version format: `MAJOR.MINOR.PATCH`
- PATCH: Bug fixes, minor tweaks
- MINOR: New features, non-breaking changes
- MAJOR: Breaking changes to API or workflow

### 4. Commit Changes
```bash
cd ~/.openclaw/workspace/skills/email-to-calendar
git add -A
git status  # Review changes
git commit -m "Description of changes"
```

### 5. Push to Remote
```bash
git push origin master
```

### 6. Publish to ClawHub
Install the CLI (`npm i -g clawhub`, needs Node >= 22) and authenticate once:
```bash
clawhub login        # device flow; approve in the browser
clawhub whoami       # confirm
```

Preview, then publish from the repo root (pass `--version` to match SKILL.md):
```bash
clawhub skill publish . --version X.Y.Z --slug email-to-calendar --dry-run
clawhub skill publish . --version X.Y.Z --slug email-to-calendar
```

Note: `package.json` must NOT contain an `openclaw` key — the CLI treats that as
a plugin and refuses to publish it as a skill. (This repo no longer ships a
`package.json`; skill metadata lives in the SKILL.md frontmatter.)

## File Structure

| Path | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions (read by agents) |
| `SETUP.md` | User configuration guide |
| `BOOT.md` | Self-bootstrapping instructions |
| `CHANGELOG.md` | Version history |
| `LICENSE` | MIT license |
| `scripts/` | Shell script wrappers |
| `scripts/utils/` | Python utility modules |
| `scripts/tests/` | Unit tests |
| `references/` | Reference documentation |

## Testing

Tests use Python's built-in `unittest` module (no pip install required).

```bash
# Run all tests
./scripts/run_tests.sh

# Run a specific test file (via the runner)
./scripts/run_tests.sh test_date_parser

# Run with verbose output
python3 -m unittest discover -s scripts/tests -v
```

## Code Style

- Shell scripts are thin wrappers that delegate to Python utilities
- Python utilities are in `scripts/utils/`
- Keep SKILL.md concise - move detailed docs to `references/`
