---
name: docs-sync
description: >
  Keep project documentation in sync with code changes. Identifies which docs need
  updating after a PR merges or code changes, drafts the updates, and manages doc site
  structure (mkdocs, docusaurus, vitepress). Use when: (1) a PR just merged and docs
  may need updating, (2) the user says "update the docs" or "sync docs", (3) a new
  doc was created and needs to be added to site navigation, (4) the user wants to audit
  which docs are stale. NOT for: writing docs from scratch for a new project (just write
  them), generating API reference docs from code comments (use typedoc/jazzy/etc.), or
  content that isn't developer documentation.
---

# Docs Sync

## Prerequisites

- git
- gh (GitHub CLI, authenticated via `gh auth login`)

Keep project documentation current with code changes. Three modes:

1. **Content sync** — update doc content after code changes
2. **Site management** — maintain doc site structure and navigation
3. **Docs audit** — identify stale docs that need attention

## Repo Discovery

Before doing anything, discover the project's documentation setup:

1. Run `git rev-parse --show-toplevel` to find the repo root
2. Check for `.docs-sync.yml` at the repo root — if it exists, read it and use its
   values for all paths, roles, and site config
3. If no config file, auto-discover:
   - Doc site engine: look for `mkdocs.yml`, `docusaurus.config.js`, `.vitepress/config.*`
   - Doc directory: look for `docs/`, `documentation/`, `wiki/`
   - Known doc files: scan for common patterns (see Doc Roles below)
   - Convention files: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`
4. Run `gh repo view --json name,owner` to confirm the repo

### Config File: `.docs-sync.yml`

Optional config file at repo root. All fields are optional — auto-discovery fills gaps.
See `docs-sync.yml` in the skill directory for a starter.

```yaml
# Map your doc files to roles so the skill knows what content belongs where
docs:
  - path: docs/features.md
    role: features

  - path: docs/architecture.md
    role: architecture

  - path: CHANGELOG.md
    role: changelog
    format: keep-a-changelog

  - path: CLAUDE.md
    role: conventions

  - path: README.md
    role: readme

# Doc site configuration (optional)
site:
  engine: mkdocs               # mkdocs | docusaurus | vitepress
  config: mkdocs.yml           # path to site config
  auto_nav: true               # update navigation when docs change
```

## Doc Roles

Roles tell the skill what kind of content a file contains, so it knows *how* to update it.

| Role | Content | Updated when... |
|------|---------|-----------------|
| `features` | User-facing feature descriptions, shortcuts, status | New feature added, feature behavior changes |
| `architecture` | App structure, data flow, patterns, diagrams | New components, changed patterns, refactors |
| `conventions` | Dev setup, coding rules, build commands | Build process changes, new conventions adopted |
| `changelog` | Version-based change history | Any significant change (follows format: keep-a-changelog, conventional, custom) |
| `readme` | Project overview, install instructions, quick start | Major features, install process changes |
| `api` | API reference, endpoints, function signatures | Public API changes |
| `guide` | Tutorials, how-tos, walkthroughs | Workflow changes, new capabilities |
| `custom` | Anything else — describe in the `description` field | Based on your description |

### Auto-Detection (No Config)

Without a config file, the skill detects roles by filename:

| Pattern | Inferred role |
|---------|--------------|
| `*feature*`, `*capability*` | `features` |
| `*architect*`, `*design*`, `*structure*` | `architecture` |
| `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `*convention*` | `conventions` |
| `CHANGELOG*`, `CHANGES*`, `HISTORY*` | `changelog` |
| `README*` | `readme` |
| `*api*`, `*reference*`, `*endpoint*` | `api` |
| `*guide*`, `*tutorial*`, `*howto*` | `guide` |

Files not matching any pattern are skipped unless listed in the config.

## Workflow: Content Sync

When the user says docs need updating (or after a PR merge):

1. **Identify what changed** — determine the scope of code changes:
   - If a PR number is provided: `gh pr view <N> --json files,title,body`
   - If a commit range: `git diff --name-only <range>`
   - If unspecified: `git diff --name-only HEAD~1` (last commit)
   - Read the actual diffs for changed files to understand *what* changed, not just *which* files

2. **Map changes to affected docs** — for each changed file, determine which doc
   roles are affected:
   - New UI component → `features`, `architecture`
   - Changed data model → `architecture`
   - New keyboard shortcut → `features`
   - Changed build command → `conventions`
   - Bug fix → `changelog` (if tracking fixes)
   - New API endpoint → `api`, `readme` (if it's a headline feature)

3. **Read current docs** — read each affected doc file to understand current content,
   structure, and style

4. **Draft updates** — write the specific changes needed for each doc:
   - Match the existing writing style and structure
   - Add to existing sections rather than creating new ones (unless clearly needed)
   - For `changelog`: add entry under the appropriate version/section
   - For `features`: add or update the feature entry, not rewrite the whole file
   - For `architecture`: update the affected section, preserve diagrams

5. **Apply or propose** — based on user preference:
   - **Direct apply**: edit the files, commit to a branch, report what changed
   - **Review first**: show the proposed changes and ask for approval
   - **Issue**: create a GitHub issue listing which docs need updating and why

### Quality Checklist

Before committing doc updates:

- [ ] Each update matches the existing style of that doc file
- [ ] No content was removed that's still accurate
- [ ] New entries are placed in the correct section (not appended randomly)
- [ ] Cross-references between docs are consistent
- [ ] Changelog entries follow the file's existing format
- [ ] Feature descriptions are user-facing (not implementation details)

## Workflow: Site Management

When docs are added, moved, or deleted — keep the site structure current.

### mkdocs

1. Read `mkdocs.yml` and parse the `nav:` section
2. For new docs: determine the correct nav section based on the doc's role and path
3. Add the entry to `nav:` in the right position
4. For moved docs: update the nav path
5. For deleted docs: remove the nav entry

### docusaurus

1. Check `sidebars.js` or `sidebars.ts`
2. For auto-generated sidebars: ensure the doc has correct frontmatter (`sidebar_position`, `sidebar_label`)
3. For manual sidebars: add/update/remove entries

### vitepress

1. Check `.vitepress/config.*` for sidebar configuration
2. Add/update/remove sidebar entries as needed

### General Rules

- **Preserve existing organization** — don't reorganize the nav, just maintain it
- **Follow naming patterns** — if existing entries use Title Case, match that
- **Respect ordering** — add new entries at logical positions, not always at the end
- **Update indexes** — if a section has an `index.md` with a list, update it too

## Workflow: Docs Audit

When the user asks "which docs are stale?" or "audit my docs":

1. Discover all doc files (see Repo Discovery)
2. For each doc file, check `git log -1 --format="%ar" -- <path>` for last modified
3. Compare with recent code changes in related areas
4. Report docs that may be stale:
   - Doc hasn't been updated in a long time but related code changed recently
   - Doc references files/functions/patterns that no longer exist
   - Doc describes behavior that the code no longer implements
5. Suggest specific updates needed for each stale doc

## Important Rules

- **Match existing style** — read the doc before updating it. Don't impose a new format.
- **Be surgical** — update the specific section that changed, don't rewrite entire docs
- **Features are user-facing** — don't write "Added SyncSettingsView.swift", write
  "Added sync settings with enable/disable toggle, status indicator, and Sync Now button"
- **Don't remove accurate content** — only remove content that's now wrong
- **Commit to a branch** — never push directly to main
- **One concern per update** — if a PR changed both features and architecture, update
  both docs but keep the changes focused on what actually changed
- **Respect repo conventions** — if the repo has CLAUDE.md or CONTRIBUTING.md, read
  and follow its branch naming, commit message, and PR conventions
