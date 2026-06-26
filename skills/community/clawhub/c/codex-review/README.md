# 🔍 Codex Review — Three-Tier Code Quality Defense

> An OpenClaw Agent Skill that orchestrates multi-model code review with escalating depth levels.

[![ClawHub](https://img.shields.io/badge/ClawHub-codex--review-blue)](https://clawhub.com/skills/codex-review)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## The Problem

AI agents write code fast — but they also **patch bugs in the wrong direction** fast. Single-pass reviews miss cross-file logic issues, business exploits, and race conditions.

## The Solution

**Three levels of defense**, each deeper than the last:

| Level | Trigger | What Happens | Time |
|-------|---------|-------------|------|
| **L1** Quick Scan | "review this" | Dual-model scan (fast model + self-review) | 5-10 min |
| **L2** Deep Audit | "audit this" | Full bug-audit flow (6 phases) | 30-60 min |
| **L1→L2** Pre-Deploy | "pre-deploy check" | L1 → hotspot handoff → L2 → gap analysis | 40-70 min |
| **L3** Cross-Validate | "cross-validate" | Independent dual audit + compare + adversarial bypass testing | 60-90 min |

## Key Features

- 🎯 **Smart Escalation** — Say "review" for quick, "audit" for deep, "cross-validate" for maximum
- 🔀 **Dual-Model Cross-Check** — Two AI reviewers independently find bugs, then compare notes
- ⚔️ **Adversarial Testing** (L3) — One model tries to bypass the other's proposed fixes
- 📋 **Hotspot Handoff** — L1 findings automatically feed into L2 for targeted deep analysis
- 🔌 **Composable** — Works standalone (L1) or with `bug-audit` skill (L2/L3)

## Install

```bash
clawhub install codex-review
```

**Recommended companion:**
```bash
clawhub install bug-audit  # Required for L2/L3
```

## Real-World Results

Built from auditing **24+ Node.js projects** with **200+ real bugs found**:
- 🔴 Admin auth bypasses via localhost detection
- 🔴 Score submission without server validation
- 🔴 SQLite double-quote column name bugs
- 🔴 Race conditions in concurrent API requests
- 🟡 Timezone UTC vs local mismatches
- 🟡 WeChat WebView compatibility issues

## L1 Self-Review Checklist

Goes beyond what automated tools catch:
- Cross-file logic consistency
- Business logic exploits (negative balance, privilege escalation)
- Race conditions & DB write conflicts
- SQLite-specific pitfalls
- Nginx sub-path routing
- Node.js memory leaks
- Frontend XSS vectors

## Report Format

```
🔍 Code Audit Report — [Project]
📊 Summary: 12 issues (🔴 2 Critical | 🟠 3 High | 🟡 5 Medium | 🔵 2 Low)
Cross-validation: Both agreed 8 | Only A: 2 | Only B: 2
```

## Part of the AI Dev Quality Suite

| Skill | Purpose |
|-------|---------|
| **codex-review** | Multi-tier code review orchestration |
| [bug-audit](https://github.com/abczsl520/bug-audit-skill) | Dynamic bug hunting (200+ pitfall patterns) |
| [debug-methodology](https://github.com/abczsl520/debug-methodology) | Root-cause debugging (no more patch-chaining) |
| [game-quality-gates](https://github.com/abczsl520/game-quality-gates) | Game-specific quality checks |
| [nodejs-project-arch](https://github.com/abczsl520/nodejs-project-arch) | AI-friendly architecture (70-93% token savings) |

## License

MIT
