---
name: changelog-linter
description: Validate CHANGELOG.md files against the Keep a Changelog format (keepachangelog.com). Checks version ordering, date formats, section types, link references, and formatting. Use when asked to lint, validate, check, or audit a CHANGELOG.md file, verify changelog format, or ensure changelog follows Keep a Changelog conventions. Triggers on "lint changelog", "validate changelog", "check CHANGELOG.md", "changelog format".
---

# Changelog Linter

Validate CHANGELOG.md files against the [Keep a Changelog](https://keepachangelog.com) specification.

## Commands

All commands use the bundled Python script at `scripts/changelog_linter.py`.

### 1. Lint a changelog

```bash
python3 scripts/changelog_linter.py lint <file> [--strict] [--format text|json|markdown]
```

Run all validation rules against a CHANGELOG.md file.

**Flags:**
- `--strict` — exit code 1 on any warning (not just errors)
- `--format` — output format: `text` (default), `json`, `markdown`

### 2. List versions

```bash
python3 scripts/changelog_linter.py versions <file> [--format text|json]
```

Extract and display all versions with dates and change counts.

### 3. Validate version ordering

```bash
python3 scripts/changelog_linter.py order <file> [--format text|json]
```

Check that versions are in descending semver order.

### 4. Check links

```bash
python3 scripts/changelog_linter.py links <file> [--format text|json]
```

Verify that all version headers have corresponding link references at the bottom.

## Lint Rules (16 total)

### Structure (5 rules)
1. **missing-title** — File doesn't start with `# Changelog`
2. **missing-description** — No description paragraph after title
3. **no-versions** — No version entries found
4. **empty-version** — Version section has no change entries
5. **unreleased-missing** — No `[Unreleased]` section

### Versions (4 rules)
6. **invalid-version** — Version doesn't follow semver (MAJOR.MINOR.PATCH)
7. **invalid-date** — Date doesn't follow ISO 8601 (YYYY-MM-DD)
8. **version-order** — Versions not in descending order
9. **duplicate-version** — Same version appears twice

### Sections (3 rules)
10. **invalid-section** — Section type not in spec (Added/Changed/Deprecated/Removed/Fixed/Security)
11. **empty-section** — Section header with no list items
12. **section-order** — Sections not in recommended order

### Formatting (4 rules)
13. **missing-link-ref** — Version header has no corresponding link reference
14. **broken-link-ref** — Link reference exists but URL is empty or malformed
15. **inconsistent-bullets** — Mixed bullet styles (`-` and `*`)
16. **trailing-whitespace** — Lines with trailing whitespace

## Output Formats

### Text (default)
```
CHANGELOG.md:15 error [invalid-date] Version 1.2.0 has invalid date: "March 2024" (expected YYYY-MM-DD)
CHANGELOG.md:28 warning [empty-section] Section "Deprecated" under 1.1.0 has no entries
CHANGELOG.md:45 warning [missing-link-ref] Version 1.0.0 has no link reference

3 issues (1 error, 2 warnings)
```

### JSON / Markdown
Standard structured output with issues, summary, and version list.

## CI Integration

```yaml
- name: Lint Changelog
  run: python3 scripts/changelog_linter.py lint CHANGELOG.md --strict
```

Exit codes: 0 = valid, 1 = issues found.
