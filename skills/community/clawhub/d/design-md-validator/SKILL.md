# DESIGN.md Skill — Design System Validation & Management

> Validate, diff, and export DESIGN.md files for consistent design systems across projects.

## Overview

DESIGN.md is a format specification (by Google Labs) for describing a visual identity to coding agents. It combines:
- **YAML front matter** — Machine-readable design tokens
- **Markdown body** — Human-readable design rationale

## Installation

The skill uses `@google/design.md` npm package:
```bash
npm install -g @google/design.md
```

## Commands

### 1. Lint — Validate DESIGN.md
```bash
npx @google/design.md lint DESIGN.md
```

**Checks:**
- Token references resolve (`broken-ref` → error)
- WCAG contrast ratios (`contrast-ratio` → warning)
- Missing primary colors (`missing-primary` → warning)
- Section order (`section-order` → warning)

**Output:** JSON with findings

### 2. Diff — Compare Versions
```bash
npx @google/design.md diff DESIGN.md DESIGN-v2.md
```

**Detects:**
- Added/removed/modified tokens
- Regressions between versions

### 3. Export — Convert to Other Formats
```bash
npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

### 4. Spec — View Format Specification
```bash
npx @google/design.md spec
npx @google/design.md spec --rules
```

## Quick Start

1. **Read existing DESIGN.md** in project
2. **Run lint** to validate structure
3. **Run export** to generate Tailwind config
4. **Update components** based on findings

## Usage in Coding

When working on UI components:

```bash
# Before editing a component, lint current state
npx @google/design.md lint design-md/markiosi/DESIGN.md

# After changes, diff to check for regressions
npx @google/design.md diff design-md/markiosi/DESIGN.md design-md/markiosi/DESIGN.md.new

# Export updated tokens
npx @google/design.md export --format tailwind design-md/markiosi/DESIGN.md > tailwind.tokens.json
```

## Workflow Integration

1. **Before making UI changes:**
   - Read project's DESIGN.md
   - Run `lint` to understand current design state

2. **After UI changes:**
   - Update DESIGN.md tokens accordingly
   - Run `diff` to detect regressions
   - Run `lint` to validate WCAG compliance

3. **For new components:**
   - Check DESIGN.md for existing component patterns
   - Define new components in DESIGN.md first
   - Use token references (`{colors.primary}`) over hardcoded values

## Resources

- **Spec:** https://github.com/google-labs-code/design.md
- **Stitch Tool:** https://stitch.withgoogle.com/
- **Design Tokens Format:** https://www.designtokens.org/
