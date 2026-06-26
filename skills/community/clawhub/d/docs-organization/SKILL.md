---
name: docs-organization
description: >-
  Organize project documentation by size, audience, and freshness. Trigger when
  setting up docs for a new project, restructuring existing documentation, slimming
  a bloated CLAUDE.md/AGENTS.md, deciding where a doc should live, or on doc best
  practices questions. Also trigger when CLAUDE.md exceeds ~250 lines or docs are
  duplicated across files.
  Triggers on: organize docs, reorganize documentation, slim CLAUDE.md, AGENTS.md
  too long, where to put docs, docs structure, doc best practices, set up
  documentation, docs are messy, flatten docs, doc migration.
version: 1.1.0
metadata:
  author: zning1994
  openclaw:
    homepage: https://github.com/zning1994/docs-organization
    os:
      - macos
      - linux
      - windows
---

# Documentation Organization

A practical guide for organizing project documentation so that every fact has one home,
AI agents load only what they need, and humans can find things without grep.

## Why This Matters

Poor doc organization creates three problems that compound over time:

1. **Drift** — the same fact copied into 3 files eventually becomes 3 different "truths"
2. **Context waste** — a 2000-line CLAUDE.md burns AI tokens on every conversation, most of it irrelevant
3. **Lost docs** — flat directories with 20+ files make everything hard to find

The fix is simple: organize by who reads it and whether it stays current.

## Step 0: Root-Level Noise Audit

Before touching docs, clean non-documentation clutter from the project root.
Root-level noise (screenshots, recordings, debug logs, AI chat exports) is often
the biggest source of visual chaos — and it has nothing to do with documentation structure.

Run `ls | wc -l` and capture the count. Then identify and relocate:

| What to look for | Where it goes |
|-----------------|---------------|
| Screenshots, recordings (`.png`, `.mov`, `.mp4`) | `archive/media/` or `screenshots/` if curated |
| Debug/build logs (`*.log`, `firebase-debug.log`) | `archive/` or delete |
| AI chat exports, temp markdown dumps | `archive/` or delete |
| One-off config experiments | `archive/` or delete |

Do this first — it dramatically reduces root-level item count and makes the real
structure visible before you start reorganizing docs.

## Step 1: Assess Project Size

Ask yourself (or the user) these questions:

| Question | Small | Medium | Large |
|----------|-------|--------|-------|
| Source files | < 5 | 5-50 | 50+ |
| Has deployment target? | No | Yes | Yes, multiple |
| Has API or database? | No | Yes | Yes |
| Ongoing operations (cron, monitoring)? | No | Maybe | Yes |
| Multiple services/containers? | No | No | Yes |

Pick the column that best matches. When in doubt, start smaller — you can always add structure later.

## Step 2: Apply the Right Template

### Small Project

Single-service tools, scripts, simple packages.

```
project/
├── CLAUDE.md    # 50-100 lines: what it does, how to run, gotchas
└── README.md    # For humans / GitHub
```

No `docs/` directory needed. Everything fits in two files.

### Medium Project

Multi-component apps with deployment targets and external integrations.

```
project/
├── CLAUDE.md    # 100-200 lines: constraints + doc index
└── docs/
    ├── plans/       # Implementation plans
    ├── design/      # Design specs
    └── reference/   # API tables, config reference, schema
```

Add directories only when you have 2+ files that belong there. One API doc doesn't need
a `reference/` folder — just put it in `docs/api.md`.

### Large Project

Systems with operational burden: multiple services, cron jobs, monitoring, multi-environment deployment.

```
project/
├── CLAUDE.md    # 200-250 lines: constraints + doc index + key gotchas
└── docs/
    ├── README.md      # Documentation map
    ├── reference/     # API endpoints, DB schema, CLI commands, config reference
    ├── runbooks/      # Deploy, operations, troubleshooting, known issues
    ├── guides/        # How-to guides for users and operators
    ├── product/       # Roadmap, product direction
    ├── design/        # Design specs (frozen after implementation)
    ├── plans/         # Implementation plans (frozen after execution)
    ├── research/      # Investigation notes, audits, system reviews
    ├── decisions/     # Architecture Decision Records (ADRs)
    └── archive/       # Superseded docs, old logs, historical patches
```

### Multi-Repo / Monorepo Workspace

An umbrella directory containing multiple independent repos (often not a git repo itself).
The key rule: **umbrella-level docs are for cross-repo concerns only**.

```
workspace/                          # NOT a git repo
├── CLAUDE.md                       # Repo map + cross-repo conventions + doc index
├── docker-compose.yml              # Cross-repo orchestration (lives at root)
├── .env / .env.example             # Shared secrets (lives at root)
│
├── repo-a/                         # Independent git repo
├── repo-b/                         # Independent git repo
│
├── deploy/                         # Cross-repo: nginx, infra configs, deploy scripts
├── scripts/                        # Cross-repo: shared tooling
├── tools/                          # Cross-repo: shared CLI utilities
│
├── docs/                           # Cross-repo documentation ONLY
│   ├── design/                     #   System-wide architecture specs
│   ├── research/                   #   Cross-cutting investigations
│   ├── runbooks/                   #   Deploy, ops, incident response
│   └── plans/                      #   Cross-repo implementation plans
│
├── screenshots/                    # Curated product screenshots (if needed)
└── archive/                        # Superseded docs + one-off media
    ├── media/                      #   Old screenshots, recordings
    └── docs/                       #   Outdated documents
```

Key differences from single-repo Large template:
- Repo-specific docs stay **inside each repo** (e.g., `repo-a/docs/`)
- Umbrella `docs/` only holds docs that span multiple repos
- Orchestration files (`docker-compose.yml`, `.env`) live at workspace root
- `deploy/` holds all infra/nginx configs — don't scatter them in root

## Step 3: Apply the Core Principles

### Principle 1: Single Source of Truth

Every fact lives in exactly one place. Other docs can *link* to it, never *copy* it.

**Bad**: API endpoint table in CLAUDE.md AND roadmap.md AND usage-guide.md
**Good**: API endpoint table in `docs/reference/api-endpoints.md`, others link to it

When you change something, update the one canonical location. Not two files, not three — one.

### Principle 2: CLAUDE.md Is an Instruction Manual, Not an Encyclopedia

CLAUDE.md (or AGENTS.md) is loaded into every AI conversation. Keep it under 250 lines.
The reason is simple: every token in CLAUDE.md is consumed on every single conversation,
whether relevant or not. A bloated CLAUDE.md wastes context and money.

**What belongs in CLAUDE.md:**
- Behavioral constraints (naming conventions, rules, gotchas)
- Architecture summary (what connects to what)
- Documentation index (where to find details)
- Key file paths

**What does NOT belong:**
- Full API tables → move to `reference/`
- Historical changelogs → move to `product/roadmap.md`
- Deployment procedures → move to `runbooks/`
- CLI command references → move to `reference/`
- Design specs → move to `design/`

If CLAUDE.md is over 250 lines, extract the largest non-essential sections first.

### Principle 3: Organize by Audience + Freshness

Two questions determine where any doc belongs:

| Question | Options |
|----------|---------|
| **Who reads it?** | agent (AI), operator (maintainer), user (end-user), contributor |
| **Does it stay current?** | canonical (kept updated), snapshot (frozen in time), archived (superseded) |

This maps directly to directories:

| Directory | Status | Audience | Contains |
|-----------|--------|----------|----------|
| `reference/` | canonical | agent, operator | Look-up tables: API, DB, CLI, config |
| `runbooks/` | canonical | operator | Deployment, ops, incident response |
| `guides/` | canonical | user, contributor | How-to instructions |
| `product/` | canonical | operator | Roadmap, direction, milestones |
| `design/` | snapshot | agent, contributor | Feature design specs |
| `plans/` | snapshot | agent, contributor | Implementation plans |
| `research/` | snapshot | operator | One-off investigations, audits |
| `decisions/` | snapshot | contributor | Architecture Decision Records |
| `archive/` | archived | — | Old/superseded docs |

### Principle 4: No Cross-Doc Mirroring

This rule prevents drift:

> After code or config changes, update the affected canonical doc only.
> Do not mirror the same fact across multiple docs.

If you find yourself maintaining a rule like "always update roadmap, deploy, known-issues,
AND CLAUDE.md" — that's a sign of mirroring. Pick one canonical location for each fact.

## Document Metadata

Add this frontmatter to any non-trivial doc:

```yaml
---
status: canonical | snapshot | archived
audience: agent | operator | user | contributor
last_reviewed: YYYY-MM-DD
---
```

- **canonical**: Must stay current. If code changes, this doc must be updated.
- **snapshot**: True at time of writing. Never updated. Dated filename is its version.
- **archived**: Superseded or obsolete. Kept for reference only.

## Anti-Patterns to Watch For

| Anti-Pattern | Why It's Bad | Fix |
|-------------|-------------|-----|
| Same fact in 3+ files | Guaranteed drift | Pick one canonical location, link from others |
| 2000-line CLAUDE.md | Wastes AI context every conversation | Keep < 250 lines, extract reference docs |
| Flat `docs/` with 20+ files | Can't find anything | Group by audience/purpose |
| Research notes in `docs/` root | Pollutes navigation | Move to `research/` or `archive/` |
| Chat logs in `docs/` | Not documentation | Move to `archive/` or delete |
| "Always update these 4 files" rule | Creates busywork and drift | "Update the one canonical source" |
| Empty directories "for later" | Confusing, no content to navigate | Create directories when you have content |
| Flat `archive/` dumping ground | Archive itself becomes a junk drawer | Use `archive/media/` for images/video, `archive/docs/` for old text |

## Migration Checklist

When reorganizing existing docs:

1. **Snapshot before state**: Run `ls | wc -l` at root and `docs/`. Save the counts for a before/after comparison.
2. **Root-level noise audit**: Move stray media, logs, and temp files out of root first (see Step 0).
3. **Measure docs**: Count lines in CLAUDE.md, count files in `docs/`, identify duplicated facts.
4. **Classify**: For each doc, determine audience + freshness status.
5. **Create structure**: Make only the directories you need right now.
6. **Check implicit references before moving**: `rg <filename>` (or `grep -r <filename>`) across the project to find references in `docker-compose.yml`, CI/CD configs, `Makefile`, shell scripts, `.gitignore`, etc. Moving a file that is referenced by a config will cause silent runtime failures.
7. **Move files**: Relocate docs to their new homes.
8. **Update implicit references**: Fix all paths found in step 6 (docker volume mounts, script paths, etc.).
9. **Extract from CLAUDE.md**: Pull reference tables, procedures, and specs into dedicated files.
10. **Add doc index**: Update CLAUDE.md with a table pointing to where things moved.
11. **Add metadata**: Put frontmatter on each non-trivial doc.
12. **Remove duplicates**: Delete mirrored content, keep only the canonical copy.
13. **Verify links**: Make sure markdown cross-references still work.
14. **Show before/after**: Compare root item count before vs. after. This validates the effort and gives the user a tangible result.

## Example: CLAUDE.md Doc Index

After extracting content, add a table like this to CLAUDE.md:

```markdown
## Documentation Index

| What you need | Where to find it |
|---------------|-----------------|
| API endpoints | `docs/reference/api-endpoints.md` |
| Database schema | `docs/reference/database-schema.md` |
| Deployment guide | `docs/runbooks/deploy.md` |
| Known issues | `docs/runbooks/known-issues.md` |
| Roadmap | `docs/product/roadmap.md` |
```

This keeps CLAUDE.md as a routing table rather than trying to contain everything.
