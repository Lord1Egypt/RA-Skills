# Release Pipeline Reference

## Table of Contents
1. [Tool: Changesets](#tool-changesets)
2. [Versioning Strategy](#versioning-strategy)
3. [Workflow: Day-to-Day](#workflow-day-to-day)
4. [Automated CI/CD Pipeline](#automated-cicd-pipeline)
5. [npm Publishing](#npm-publishing)
6. [Package Configuration Checklist](#package-configuration-checklist)
7. [Changelog Format](#changelog-format)
8. [Pre-releases & Beta Versions](#pre-releases--beta-versions)

---

## Tool: Changesets

[Changesets](https://github.com/changesets/changesets) manages version bumps, changelog generation, and publishing in a monorepo. It's the standard tool for component library release workflows.

### Why Changesets?

- Works natively with pnpm/yarn workspaces
- Changelog is auto-generated from changeset descriptions
- Supports pre-releases and snapshot versions
- GitHub bot for PR-based reviews
- Atomic publish across multiple packages

### Installation

```bash
pnpm add -D @changesets/cli -w
pnpm changeset init
```

This creates `.changeset/config.json`.

**`.changeset/config.json`:**

```json
{
  "$schema": "https://unpkg.com/@changesets/config/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

---

## Versioning Strategy

Follow **Semantic Versioning** (semver):

| Change Type | Version Bump | When |
|---|---|---|
| `patch` | `1.0.0 → 1.0.1` | Bug fixes, internal refactors |
| `minor` | `1.0.0 → 1.1.0` | New features, new components, new props (backward-compatible) |
| `major` | `1.0.0 → 2.0.0` | Breaking changes (removed props, renamed APIs, behavior changes) |

**Breaking change examples:**
- Removing or renaming a prop
- Changing a prop's type in a non-backward-compatible way
- Removing a component
- Changing the CSS class naming scheme
- Dropping support for a React version

---

## Workflow: Day-to-Day

### Step 1: Create a Changeset (when making changes)

```bash
pnpm changeset
```

Interactive prompts:
1. Select which packages changed
2. Select bump type (major / minor / patch)
3. Write a description (this becomes the changelog entry)

A markdown file is created in `.changeset/`:

```markdown
---
"@myds/components": minor
"@myds/tokens": patch
---

Add new `Badge` component with `status` and `size` variants.

Update color tokens with additional gray-950 step.
```

**Commit this file** with your PR.

### Step 2: Version Bump (before releasing)

```bash
# Consumes all pending .changeset files,
# bumps package versions, updates CHANGELOG.md files
pnpm changeset version
```

Review and commit the version bump:
```bash
git add .
git commit -m "chore: version packages"
```

### Step 3: Publish to npm

```bash
pnpm changeset publish
```

This publishes all packages that have version bumps. After publishing:

```bash
git push --follow-tags
```

---

## Automated CI/CD Pipeline

Use the official [changesets/action](https://github.com/changesets/action) for GitHub Actions.

### How It Works

1. PRs: Changeset bot comments to remind contributors to add changesets
2. On merge to `main`: A "Version Packages" PR is auto-created/updated
3. On merge of the version PR: packages are auto-published to npm

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches:
      - main

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - run: pnpm install --frozen-lockfile

      - run: pnpm build

      - run: pnpm test

      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
          version: pnpm changeset version
          commit: "chore: version packages"
          title: "chore: version packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## npm Publishing

### Before First Publish

1. **Create npm organization** (for scoped packages `@myds/*`):
   ```bash
   npm org create myds
   ```

2. **Set up npm token**:
   ```bash
   npm token create --type=automation
   # Add as NPM_TOKEN secret in GitHub repo settings
   ```

3. **Ensure package.json is correct**:
   ```json
   {
     "name": "@myds/components",
     "version": "0.1.0",
     "private": false,
     "publishConfig": {
       "access": "public",
       "registry": "https://registry.npmjs.org"
     }
   }
   ```

4. **Add `.npmignore`** (or use `files` field in package.json):
   ```
   # .npmignore
   src/
   *.test.*
   *.stories.*
   tsconfig.json
   vitest.config.ts
   ```

   Or use `files` in `package.json` (preferred):
   ```json
   {
     "files": ["dist", "README.md"]
   }
   ```

### Dry Run (check what will be published)

```bash
pnpm publish --dry-run
# or
npm pack --dry-run
```

---

## Package Configuration Checklist

Before first publish, verify each package:

- [ ] `name` is scoped and unique (`@myds/components`)
- [ ] `version` starts at `0.1.0` or `1.0.0`
- [ ] `main` points to CJS output
- [ ] `module` points to ESM output
- [ ] `types` points to `.d.ts`
- [ ] `exports` map defined for named sub-paths
- [ ] `files` field restricts to `dist/`
- [ ] `sideEffects: false` (for tree-shaking) — unless you have global CSS imports
- [ ] `peerDependencies` lists React (not in `dependencies`)
- [ ] `publishConfig.access: "public"` for scoped packages

**Full `package.json` example:**

```json
{
  "name": "@myds/components",
  "version": "1.0.0",
  "description": "Enterprise UI component library",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "sideEffects": false,
  "files": ["dist", "README.md"],
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    },
    "./styles": "./dist/styles.css"
  },
  "peerDependencies": {
    "react": ">=17",
    "react-dom": ">=17"
  },
  "publishConfig": {
    "access": "public"
  },
  "keywords": ["design-system", "react", "ui", "components"]
}
```

---

## Changelog Format

Changesets generates changelogs in this format:

```markdown
# @myds/components

## 2.1.0

### Minor Changes

- a1b2c3d: Add new `Badge` component with `status` and `size` variants

### Patch Changes

- Updated dependencies
  - @myds/tokens@1.2.1

## 2.0.0

### Major Changes

- f4e5d6c: **Breaking:** `Button` prop `kind` renamed to `variant` for consistency

  **Migration:** Replace all `kind="..."` with `variant="..."`

## 1.0.1

### Patch Changes

- b7c8d9e: Fix `Input` placeholder color in dark mode
```

**Writing good changeset descriptions:**
- Use present tense: "Add", "Fix", "Update", not "Added"
- Include migration guides for breaking changes
- Reference issue/PR numbers when helpful
- Keep summaries concise; add detail in PR body

---

## Pre-releases & Beta Versions

For releasing unstable/experimental versions:

```bash
# Enter pre-release mode
pnpm changeset pre enter beta

# Create changesets and version as normal
pnpm changeset
pnpm changeset version
# → versions become 2.0.0-beta.0, 2.0.0-beta.1, etc.

# Publish with beta tag
pnpm changeset publish --tag beta

# Exit pre-release mode when stable
pnpm changeset pre exit
```

Install beta version:
```bash
pnpm add @myds/components@beta
```

### Snapshot Releases (for PR testing)

```bash
# Publish a snapshot version for testing
pnpm changeset version --snapshot pr-123
pnpm changeset publish --tag snapshot
# → @myds/components@1.0.0-pr-123-20240101000000
```
