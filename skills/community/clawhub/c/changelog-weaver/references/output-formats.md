# Output Format Specifications

Changelog Weaver generates four output formats from the same structured JSON data.

## 1. Changelog Format (`--format changelog`)

Follows the [Keep a Changelog](https://keepachangelog.com/) convention.

```markdown
# Changelog

## [2.4.0] - 2026-06-15

### ✨ Features
- Added dark mode theme with system preference detection (#356) — @bob
- Export dashboard as PDF with custom branding options (#342) — @alice

### 🐛 Bug Fixes
- Fixed date picker offset in Safari when timezone is UTC+8 (#349) — @charlie

### ⚠️ Breaking Changes
- Removed legacy `/api/v1/users` — use `/api/v2/users` instead (#370)
```

**Structure:**
- `# Changelog` — top-level heading
- `## [version] - YYYY-MM-DD` — version heading with date
- `### {emoji} {Category}` — grouped by type, ordered by priority (breaking → feat → fix → ...)
- `- {description} (#PR) — @contributor` — each entry
- `### 🙏 Contributors` — closing section

**Best for:** Project root `CHANGELOG.md`, versioned alongside code.

## 2. Release Notes Format (`--format release`)

Optimized for GitHub/GitLab Release pages with contributor attribution and commit hashes.

```markdown
## 🚀 Release 2.4.0

**47 commits** by **5 contributors**

### ✨ Features
- Added dark mode theme with system preference detection (#356) by @bob in `a3f2c1d`
- Export dashboard as PDF with custom branding options (#342) by @alice in `b8e4f9a`

### 🐛 Bug Fixes
- Fixed date picker offset in Safari (#349) by @charlie in `c7d1e2f`

### 🙏 New Contributors
Thanks to all contributors for this release!

**Full Changelog**: https://github.com/user/repo/compare/v2.3.0...v2.4.0
```

**Structure:**
- Release title with rocket emoji
- Summary line (commit count, contributor count, breaking change warning)
- Grouped entries with `by @author in \`hash\`` format
- Expandable breaking change details with `>` blockquote
- Contributors section with compare link

**Best for:** GitHub Releases, GitLab Releases, release announcement pages.

## 3. Plain Text Format (`--format plain`)

Optimized for messaging platforms. Supports `--platform` flag:

### `--platform generic` (default)
```
📦 2.4.0 发布通知 (2026-06-15)

✨ Features
  • Added dark mode theme
  • Export dashboard as PDF

🐛 Bug Fixes
  • Fixed date picker in Safari

👥 贡献者: alice, bob, charlie
```

### `--platform feishu` / `--platform dingtalk`
```
📦 2.4.0 发布通知 (2026-06-15)

【Features】
  • Added dark mode theme
  • Export dashboard as PDF

【Bug Fixes】
  • Fixed date picker in Safari

👥 贡献者: alice, bob, charlie
```

**Behavior:** Limits to 5 entries per category with "... and N more changes" for the rest. Contributors limited to 8 with a count of remaining.

**Best for:** 飞书群公告, 钉钉群消息, 企业微信通知, Slack announcements.

## 4. JSON Format (`--format json`)

Full structured data for CI/CD pipelines and programmatic consumption.

```json
{
  "meta": {
    "version": "2.4.0",
    "date": "2026-06-15",
    "generated_at": "2026-06-15T09:30:00+08:00",
    "generator": "changelog-weaver",
    "repo_url": "https://github.com/user/repo.git"
  },
  "stats": {
    "total_commits": 47,
    "total_contributors": 5,
    "contributors": ["alice", "bob", "charlie", "dave", "eve"],
    "type_counts": {"feat": 12, "fix": 18, "docs": 5, "chore": 4, "refactor": 3, "perf": 2, "breaking": 1, "other": 2},
    "breaking_changes": 1,
    "date_range": {"first": "2026-06-01T10:00:00Z", "last": "2026-06-15T18:00:00Z"}
  },
  "categories": {
    "breaking": {
      "label": "Breaking Changes",
      "emoji": "⚠️",
      "count": 1,
      "entries": [...]
    },
    "feat": {
      "label": "Features",
      "emoji": "✨",
      "count": 12,
      "entries": [
        {
          "hash": "a3f2c1d",
          "description": "add dark mode theme support",
          "scope": "ui",
          "breaking": false,
          "breaking_detail": "",
          "author": "bob",
          "references": ["356"],
          "original_subject": "feat(ui): add dark mode theme support",
          "count": 1
        }
      ]
    }
  },
  "ai_rewrites": {
    "a3f2c1d": "Added dark mode theme with system preference detection",
    "b8e4f9a": "Export dashboard as PDF with custom branding options"
  }
}
```

**Best for:** CI/CD pipelines (GitHub Actions, GitLab CI), automated release workflows, Slack/Discord bots.
