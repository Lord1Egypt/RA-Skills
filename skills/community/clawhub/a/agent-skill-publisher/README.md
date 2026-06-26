# skill-publisher

[English](README.md) | [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: macOS | Linux | Windows (WSL)](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows%20(WSL)-lightgrey.svg)](https://github.com/bryant24hao/skill-publisher)

> One command to publish your agent skill to GitHub, ClawdHub, and skills.sh.

A Claude Code skill that automates the entire skill publishing pipeline — from pre-flight validation to installation verification across all three platforms.

## Why

Publishing a skill should be simple, but the reality is:

- **GitHub** needs a repo, topics for discoverability, and correct badge links
- **ClawdHub** has a CLI with a known bug (`acceptLicenseTerms`), slug conflicts, and no auto-retry
- **skills.sh** doesn't auto-index — you must submit a GitHub issue to `vercel-labs/skills`
- Install commands in README must match the final repo name on all platforms
- Bilingual READMEs need consistent content and working language switchers

Miss one step and your skill is either unfindable or uninstallable.

**skill-publisher handles the full pipeline in one session.**

## What It Does

```
1. Pre-flight Check    → Validate SKILL.md, README, LICENSE, secrets scan
2. GitHub Publish      → Create repo, push, add discovery topics
3. ClawdHub Publish    → Login, check slug, publish (with bug workaround)
4. skills.sh Submit    → Auto-create index request issue
5. Install Verify      → Test all 3 install methods end-to-end
6. Post-publish        → Summary with all links and commands
```

## Quick Install

```bash
npx skills add bryant24hao/skill-publisher -g -y
```

**Manual**:

```bash
git clone https://github.com/bryant24hao/skill-publisher.git ~/.claude/skills/skill-publisher
```

## Usage

```
/skill-publisher
publish my skill
上架技能
发布 skill 到 clawhub 和 skills.sh
```

## Prerequisites

- **[gh](https://cli.github.com/)** — GitHub CLI (for repo creation and issue submission)
- **git** — version control

Optional:
- **clawhub CLI** — for ClawdHub publishing (`npx clawhub` works without global install)

## Known Issues

| Issue | Workaround |
|-------|------------|
| ClawdHub CLI v0.7.0 missing `acceptLicenseTerms` | Auto-patched during publish |
| skills.sh no auto-indexing | Auto-submits issue to vercel-labs/skills |
| ClawdHub slug conflicts | Pre-checks availability before GitHub repo creation |

## License

[MIT](LICENSE)
