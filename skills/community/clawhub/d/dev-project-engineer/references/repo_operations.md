# Repo Operations Reference

Standard git workflows for the Project Engineer.

**External Dependency:** All git commands in this file are executed through the separately loaded `git_essentials` skill (or equivalent git tooling skill). That skill manages repository credentials and access tokens. This file defines *procedures and standards* only — it does not execute commands directly.

**Access Model:** Read-only. The engineer clones, pulls, checks out branches, and diffs. It never pushes, merges, deletes, or modifies repository content.

All operations assume the git skill has been configured with read-only access to project repositories.

## Cloning a Repo

> **In most setups the repo is already cloned at setup time** to `~/.openclaw/projects/[project_name]/workspace/repo/`. Pull from there rather than re-cloning. Only clone fresh if the repo is not present.

```bash
# Only if repo not yet present:
git clone <repo-url> ~/.openclaw/projects/<project-name>/workspace/repo
cd ~/.openclaw/projects/<project-name>/workspace/repo
git checkout main
```

Confirm the default branch is `main`. If the repo uses `master`, note this in the audit and recommend migration to `main`.

## Pulling Latest Code

Always pull before any analysis to ensure you're working with current code:

```bash
cd ~/.openclaw/projects/<project-name>/workspace/repo
git checkout main
git pull origin main
```

## Checking Out a Dev Branch (for Escalation/Review)

```bash
git fetch origin
git checkout <branch-name>
git pull origin <branch-name>
```

Dev branch naming convention for this team:
```
[project-id]/[sprint-id]/[task-id]-[short-description]
```
Example: `ezbi/sprint-3/1234-navbar-redesign`

## Diffing a Branch Against Main

To understand what a dev has changed (for PR review or escalation support):

```bash
# Summary of changed files
git diff main...<branch-name> --stat

# Full diff
git diff main...<branch-name>

# Diff for specific file
git diff main...<branch-name> -- path/to/file.ext
```

## Identifying Affected Files for a Requirement

When tracing a requirement through the codebase:

1. Use `grep -rn` to search for relevant function names, route paths, component names, or DB table references.
2. Use `find` to locate files by naming convention.
3. Review import chains to understand dependency relationships.
4. Document every file that would need modification in the Technical Assessment.

```bash
# Search for a term across the codebase
grep -rn "searchTerm" --include="*.ts" --include="*.tsx" --include="*.py" --include="*.js"

# Find files by name pattern
find . -name "*.model.*" -o -name "*.controller.*" -o -name "*.service.*"

# Show directory tree
find . -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*" | head -100
```

## Multi-Repo Projects

If FE and BE live in separate repos:

1. Clone both repos into separate directories under `/home/claude/`.
2. Analyze each independently but document cross-repo dependencies (e.g., FE expects endpoint X from BE).
3. In the Implementation Plan, explicitly note when a BE task must complete before a FE task can begin due to API contract dependencies.
4. When reviewing branches, always confirm which repo the branch belongs to.

## What the Engineer NEVER Does

- Push to `main` or any branch
- Merge PRs (QA reviews, PM approves if needed)
- Delete branches
- Force-push or rewrite history
- Modify code on `main` directly

The engineer reads, analyzes, and advises. Code changes are executed by FE/BE devs.
