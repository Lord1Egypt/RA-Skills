---
name: changelog-weaver
description: "Generate polished changelogs and release notes from git history, PRs, and issues — auto-categorize features, fixes, and breaking changes"
tags:
  - changelog
  - release-notes
  - git
  - conventional-commits
  - versioning
  - devtools
---

# Changelog Weaver

Transform git history into polished, human-readable changelogs and release notes. Parse Conventional Commits, auto-categorize changes by type, deduplicate similar commits, and generate output in multiple formats — from `CHANGELOG.md` to messaging-platform announcements.

## First-Success Path (30 seconds)

```bash
# 1. Collect commits since your last git tag
python3 scripts/weaver.py collect --from-latest-tag -o commits.json

# 2. Generate a CHANGELOG.md
python3 scripts/weaver.py generate -i commits.json -f changelog

# 3. That's it — a structured changelog ready for review
```

To add AI-powered semantic rewriting (human-readable descriptions instead of raw commit messages), load `commits.json` into chat and say: **"Rewrite all commit descriptions to be user-facing"** — copy the `ai_rewrites` back into the JSON, then regenerate.

## Workflow

### Step 1: Collect Change Sources

Decide what to include in the changelog:

```bash
# Between two tags
weaver.py collect --from v2.3.0 --to v2.4.0 -o changes.json

# Since the latest tag (auto-detected)
weaver.py collect --from-latest-tag -o changes.json

# By date range
weaver.py collect --since "2026-06-01" --until "2026-06-15" -o changes.json

# All commits on a branch
weaver.py collect --from main --to feature/big-refactor -o changes.json
```

The script reads `git log`, filters merge commits by default, and outputs structured JSON.

If PR/issue data is available (GitHub/GitLab), the AI can enrich the changelog with PR titles and linked issue numbers. Mention this in your prompt.

### Step 2: Smart Classification

The script automatically classifies every commit by [Conventional Commits](https://www.conventionalcommits.org/) type:

| Prefix | Category | Example |
|--------|----------|---------|
| `feat:` | Features | `feat(auth): add OAuth2 login` |
| `fix:` | Bug Fixes | `fix: resolve race condition in cache` |
| `docs:` | Documentation | `docs: update API reference` |
| `chore:` | Chores | `chore: bump dependencies` |
| `refactor:` | Refactoring | `refactor: extract payment module` |
| `perf:` | Performance | `perf: optimize query planner` |
| `test:` | Tests | `test: add integration tests` |
| `build:` | Build System | `build: migrate to vite` |
| `ci:` | CI/CD | `ci: add deploy workflow` |
| `revert:` | Reverts | `revert: rollback auth changes` |
| `security:` | Security | `security: patch XSS vector` |
| `deps:` | Dependencies | `deps: update react to 19.0` |

Commits that don't follow the convention are grouped under `other` — the AI can still reclassify them by analyzing the commit message content.

### Step 3: AI Semantic Rewrite

Load the generated JSON into chat for the AI to perform semantic rewriting:

> **Prompt:** "I have a changelog JSON at `commits.json`. Rewrite all commit descriptions to be user-facing, replace technical jargon with plain language, and suggest category corrections for any misclassified commits. Output as `ai_rewrites` mapping."

The AI will:
- Convert `fix: resolve race condition in user auth token refresh` → "Fixed login sessions expiring prematurely during token refresh"
- Shorten verbose descriptions to one line
- Merge related entries that span multiple commits
- Flag entries that need human review

Copy the `ai_rewrites` object back into the JSON under the top-level key `"ai_rewrites"`, then regenerate.

### Step 4: Deduplicate & Merge

The script merges adjacent commits of the same type with ≥70% description token overlap. For manual merging, tell the AI:

> **Prompt:** "Merge any commits in `commits.json` that clearly belong to the same feature or fix. Update the `count` field."

The AI will identify related commits (e.g., 3 commits all fixing the same date-picker bug) and consolidate them.

### Step 5: Identify Breaking Changes

Breaking changes are detected automatically via:
- `!` suffix: `feat(api)!: remove deprecated endpoint`
- Footer: `BREAKING CHANGE: drops support for Node 16`

The AI also scans `other` commits for breaking-change language:

> **Prompt:** "Scan all commit descriptions in `commits.json` for breaking changes not marked with ! or BREAKING CHANGE footer. Add `breaking: true` and a `breaking_detail` for each."

### Step 6: Generate Output Formats

Once the JSON is ready (with optional AI rewrites), generate output in any format:

```bash
# Keep a Changelog format (CHANGELOG.md)
weaver.py generate -i commits.json -f changelog -o CHANGELOG.md

# GitHub Release body
weaver.py generate -i commits.json -f release -o RELEASE_NOTES.md

# Plain text for 飞书/钉钉
weaver.py generate -i commits.json -f plain -p feishu -o announcement.txt

# JSON for CI/CD pipelines
weaver.py generate -i commits.json -f json -o changelog.json
```

### Step 7: Quality Check

Before publishing, run a quality pass:

> **Prompt:** "Review `CHANGELOG.md` for issues: missing entries (compare to git diff --stat), broken links, misclassified items, entries that need human confirmation. Output a QA checklist."

Key checks:
- Every significant change has an entry
- No duplicate or contradictory entries
- Breaking changes are clearly highlighted
- Links to PRs/issues are valid
- Release date and version are correct

### Step 8: Deliver & Integrate

Write the final output:

```bash
# Write to project root
cp CHANGELOG.md /path/to/project/CHANGELOG.md

# Or prepend to existing changelog (keep history)
cat CHANGELOG.md <(tail -n +2 /path/to/project/CHANGELOG.md) > /tmp/merged.md
```

For CI/CD integration, consume the JSON output:

```yaml
# GitHub Actions example
- name: Generate Changelog
  run: |
    python3 scripts/weaver.py collect --from-latest-tag -o changelog.json
    python3 scripts/weaver.py generate -i changelog.json -f release >> $GITHUB_STEP_SUMMARY
```

## Sample Prompts

### 1. Basic Release Changelog
> "Generate a changelog for the v2.4.0 release from git history since v2.3.0. Use Keep a Changelog format. Our project is at ~/projects/myapp."

**What the skill does:** Runs `collect`, loads JSON, suggests rewrites, generates `CHANGELOG.md`.

### 2. Weekly Team Report
> "Generate a weekly summary of changes to the `backend` repo since last Monday. Format as a plain text message for DingTalk — Chinese, concise, grouped by feature/fix/chore."

**What the skill does:** Runs `collect --since "last Monday"`, generates `plain -p dingtalk`, AI rewrites descriptions in Chinese.

### 3. GitHub Release with AI Rewrites
> "Collect all commits since v1.5.0 in ~/projects/api-server. Rewrite every description to be user-facing. Generate a GitHub Release body with contributor shoutouts. Add a 'What's New' highlight section at the top."

**What the skill does:** Collects commits, AI rewrites descriptions, generates `release` format with highlights.

### 4. Breaking Change Audit
> "Scan commits between v3.0.0 and v3.1.0 for breaking changes — both marked and unmarked. Generate a migration guide section in the changelog."

**What the skill does:** Collects commits, AI scans for breaking changes, adds migration notes.

### 5. PR-Enriched Changelog
> "Generate a changelog from git history, but also pull PR titles from GitHub for the `myorg/myrepo` project. Match commits to PRs by branch name and reference numbers. Use PR titles for the changelog entries instead of commit messages."

**What the skill does:** Collects commits, AI cross-references with GitHub PR API, uses PR titles.

## Real-World Examples

### Example 1: Open Source Library Release

**Scenario:** You maintain `react-data-grid` and are releasing v4.2.0. The repo uses Conventional Commits. You need a professional `CHANGELOG.md` following Keep a Changelog format.

**Input:**
```bash
python3 scripts/weaver.py collect \
  --repo ~/projects/react-data-grid \
  --from v4.1.0 --to v4.2.0 \
  -o v4.2.0-commits.json
```

The JSON contains 47 commits: 12 feat, 18 fix, 5 docs, 4 chore, 3 refactor, 2 perf, 1 breaking, 2 other.

**AI Prompt:** "Load `v4.2.0-commits.json`. Rewrite all descriptions to be concise and user-facing. The audience is React developers. Merge the 3 commits about 'column resize' into one entry. Flag the breaking change for prominent display."

**Output (CHANGELOG.md excerpt):**
```markdown
# Changelog

## [4.2.0] - 2026-06-15

### ⚠️ Breaking Changes
- Removed `legacyRowRenderer` prop — migrate to `rowRenderer` with the new `RowConfig` interface (#892)

### ✨ Features
- Column resize handles: drag to resize any column, double-click to auto-fit (#845, #867, #881) — @sarahchen
- Virtual scrolling for 100K+ row datasets with <50ms render time (#878) — @mikez
- Multi-select cells with Shift+Click and Ctrl+Click (#903) — @alexk

### 🐛 Bug Fixes
- Fixed date filter not respecting custom timezone (#890) — @jamesw
- Fixed column reorder breaking when a column is hidden (#895) — @linday

### 🙏 Contributors
@alexk, @jamesw, @linday, @mikez, @sarahchen
```

---

### Example 2: Team Weekly Report for 飞书

**Scenario:** Every Friday, the platform team sends a summary of the week's changes to the company-wide 飞书 group. The repo (`~/projects/platform`) has 30-50 commits per week with mixed commit quality.

**Input:**
```bash
python3 scripts/weaver.py collect \
  --repo ~/projects/platform \
  --since "2026-06-08" --until "2026-06-15" \
  -o weekly-2026-06-15.json
```

**AI Prompt:** "Load `weekly-2026-06-15.json`. Rewrite all descriptions in Chinese, grouping by feature/fix/infra. Focus on business impact. Generate plain text for 飞书, limit to top 10 entries."

**Output (announcement.txt):**
```
📦 平台周报 (2026-06-08 ~ 2026-06-15)

【新功能】
  • 用户画像页新增「活跃度趋势」图表，支持按周/月切换
  • 数据导出支持自定义字段选择，减少导出体积 60%

【问题修复】
  • 修复 Safari 浏览器下 Dashboard 加载白屏问题（影响约 5% 用户）
  • 修复大文件上传偶发超时，现在支持 500MB 以下文件稳定上传
  • 修复深夜时段定时任务漏执行的问题

【基础设施】
  • CI 构建时间从 12 分钟优化到 6 分钟
  • 升级 Redis 集群至 7.2，内存使用降低 30%

👥 本周贡献者: 张三, 李四, 王五, 赵六
```

---

### Example 3: Breaking Change Migration Guide

**Scenario:** Your API server v3.0 introduces several breaking changes. The changelog must include a detailed migration guide for downstream consumers.

**Input:**
```bash
python3 scripts/weaver.py collect \
  --repo ~/projects/api-server \
  --from v2.9.0 --to v3.0.0 \
  -o v3.0.0-commits.json
```

**AI Prompt:** "This is a major version bump. Scan all commits for breaking changes — both marked and unmarked. For each breaking change, write a migration note with 'Before' and 'After' code snippets. Generate the changelog with a prominent 'Migration Guide' section at the top."

**Output (CHANGELOG.md excerpt):**
```markdown
## [3.0.0] - 2026-06-15

### 📋 Migration Guide

#### 1. `/api/v1/users` → `/api/v2/users`
**Before:**
```http
GET /api/v1/users?role=admin
```
**After:**
```http
GET /api/v2/users?filter[role]=admin
```

#### 2. Authentication header format
**Before:** `Authorization: Token abc123`
**After:** `Authorization: Bearer abc123`

#### 3. Webhook payload structure
The `event.data` field is now always an object (was sometimes a string). Update your webhook handlers to expect `typeof event.data === 'object'`.

---

### ⚠️ Breaking Changes
- Migrated user endpoints to v2 with filter-based query params (#1204)
- Changed authentication scheme from Token to Bearer (#1189)
- Normalized webhook payload structure — `event.data` is always an object (#1215)

### ✨ Features
- Added bulk user import API with CSV validation (#1198)
- New webhook retry mechanism with exponential backoff (#1207)
```

## Requirements

- **Python 3.9+** — standard library only (no pip dependencies)
- **git** — available on `$PATH`

## Safety

- All processing is local — no git history is sent to external services
- The script runs read-only git commands (`git log`, `git describe`)
- AI rewriting happens in-chat with explicit user review before final output
- No destructive operations — output files are written to specified paths only

## Compare with Related Skills

| Skill | Focus | How Changelog Weaver Differs |
|-------|-------|------------------------------|
| **Release Guard** | Pre-release quality checks (files, secrets, scripts) | Changelog Weaver **generates the changelog content**, not checks |
| **Git Blame Auditor** | Code attribution, contributor stats, tech debt | Changelog Weaver summarizes **what changed**, not who wrote what |
| **Doc Weaver** | Markdown → Word/PDF with templates | Changelog Weaver is **git-aware**, specialized for changelogs |

These skills are **complementary**: use Release Guard to validate a release, Changelog Weaver to document it, and Doc Weaver to format it into a polished PDF.
