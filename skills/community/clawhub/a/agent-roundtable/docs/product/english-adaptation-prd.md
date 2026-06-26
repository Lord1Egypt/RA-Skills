# Roundtable English Adaptation — PRD

> **Version**: 1.0
> **Date**: 2026-05-21
> **Status**: Draft
> **Owner**: 饼哥 (Product Director)
> **Project**: [roundtable-ai](https://github.com/MoyuFamily/agent-roundtable)

---

## 1. Background & Goals

### 1.1 Problem

Roundtable-ai is a Python library for orchestrating multi-agent roundtable discussions. All user-facing content — README, code comments, docstrings, CLI output, social preview, and demo assets — is currently in Chinese. This blocks adoption by international developers and limits PyPI/GitHub discoverability.

### 1.2 Goal

Make roundtable-ai fully accessible to English-speaking developers while preserving the existing Chinese experience for current users.

### 1.3 Core Value

**Unlock global adoption** — English-first documentation and UI, zero friction for international contributors.

---

## 2. Bilingual Strategy

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. English-only** | Replace all Chinese with English | Simplest, best for global reach | Loses Chinese users' comfort |
| B. Dual-language (side by side) | README with both languages | Inclusive | Verbose, hard to maintain |
| C. Separate branches | `main` (EN), `zh` branch | Clean separation | Maintenance overhead |

**Recommendation: Option A — English-first, with Chinese README in a `docs/zh/` folder as reference.**

Rationale:
- PyPI and GitHub are English-dominant ecosystems
- Most Chinese developers read English docs comfortably
- Maintaining two parallel READMEs is unsustainable for a small team
- The demo code examples are already in English variable names

---

## 3. Translation Inventory

### 3.1 P0 — Must Ship (Blocks International Release)

| # | File | Content Type | Chinese Lines | Effort |
|---|------|-------------|---------------|--------|
| 1 | `README.md` | Title, tagline, descriptions, code comments, section headers | ~80 lines | M |
| 2 | `docs/design/social-preview.html` | Tagline text (line 181) | 1 line | S |
| 3 | `src/roundtable/core.py` | `_DEMO_TOPIC`, `_DEMO_PARTICIPANTS`, `_DEMO_SPEECHES`, `_DEMO_TRACKS`, `_DEMO_SUMMARY` (lines 608-783) | ~60 lines | M |

### 3.2 P1 — Should Ship (Improves Developer Experience)

| # | File | Content Type | Chinese Lines | Effort |
|---|------|-------------|---------------|--------|
| 4 | `src/roundtable/core.py` | Inline code comments | ~10 lines | S |
| 5 | `docs/API.md` | API documentation | TBD | M |
| 6 | `docs/INTEGRATION.md` | Integration guide | TBD | M |
| 7 | `docs/architecture.md` | Architecture doc | 8 lines | S |
| 8 | `src/skills/SKILL.md` | Hermes skill definition (mixed CN/EN) | 3 lines | S |

### 3.3 P2 — Nice to Have (Polish)

| # | File | Content Type | Effort |
|---|------|-------------|--------|
| 9 | `docs/design/assets/demo.gif` | Animated demo with Chinese text | L (re-record) |
| 10 | `docs/product/PRD-web-viewer.md` | Internal PRD (Chinese) | Skip — internal doc |
| 11 | `docs/design/DESIGN-SPEC.md` | Design spec (Chinese) | Skip — internal doc |
| 12 | `docs/design/web-viewer/*.md` | Web viewer specs (Chinese) | Skip — internal doc |
| 13 | `docs/tech-designs/*.md` | Tech design docs (Chinese) | Skip — internal doc |
| 14 | `docs/discussions/*.md` | Discussion transcripts (Chinese) | Skip — internal doc |

**Note**: Internal docs (PRDs, design specs, tech designs, discussions) are team-facing and can remain Chinese. Only user-facing content needs translation.

---

## 4. Detailed Translation Specs

### 4.1 README.md

**Current**: All Chinese headers, descriptions, code comments, contribution guide.

**Target structure**:

```markdown
# Roundtable

**Let multiple AI agents sit down and discuss — auto-track consensus &分歧, reach conclusions.**

---

## ⚡ 3 Lines of Code, Start a Meeting

## 🎯 Why Roundtable?

## ✨ Key Features

## 📦 Installation

## 🚀 Quick Start

### Basic Usage
### Error-Safe Mode (Recommended for Production)
### Real-time Notifications

## 🔌 Hermes Agent Integration

## 📐 Architecture

## 🤝 Contributing

## 📄 License
```

**Key translations**:
| Chinese | English |
|---------|---------|
| 让多个 AI 坐下来开会讨论 | Let multiple AI agents sit down and discuss |
| 自动追踪共识与分歧，得出结论 | Auto-track consensus &分歧, reach conclusions |
| 谁先说？谁后说？ | Who speaks first? Who goes next? |
| 说了什么？达成共识了吗？ | What was said? Did they reach consensus? |
| 讨论怎么结束？结论在哪？ | How does it end? Where's the conclusion? |
| 实时知道进展？ | Real-time progress updates? |
| 你只管选人、定话题，Roundtable 帮你管剩下的一切。 | You pick the people and set the topic — Roundtable handles the rest. |
| 从源码安装 | Install from source |
| 错误安全模式 | Error-Safe Mode |
| 代码规范 | Code Standards |

### 4.2 core.py Demo Content

The demo data (lines 608-783) is used for `demo()` and `run_demo()`. Translate:

| Field | Current (CN) | Target (EN) |
|-------|-------------|-------------|
| `_DEMO_TOPIC` | 选择后端框架：FastAPI vs Go Gin vs Node Express | Choose backend framework: FastAPI vs Go Gin vs Node Express |
| Role: 全栈工程师 | Full-Stack Engineer |
| Role: 架构师 | Architect |
| Role: 产品经理 | Product Manager |
| perspective: 重视开发效率和生态 | Values dev efficiency and ecosystem |
| perspective: 重视性能和可维护性 | Values performance and maintainability |
| perspective: 重视交付速度和团队学习成本 | Values delivery speed and team learning curve |

All demo speeches (~30 lines) should be translated naturally, preserving technical terms (FastAPI, Go Gin, Celery, Pydantic, etc.).

### 4.3 social-preview.html

Line 181:
```html
<!-- Current -->
<div class="tagline">让多个 AI Agent 坐下来开会讨论<br>自动追踪共识与分歧，得出结论</div>

<!-- Target -->
<div class="tagline">Let multiple AI agents sit down and discuss<br>Auto-track consensus &分歧, reach conclusions</div>
```

Or fully English:
```html
<div class="tagline">Let multiple AI agents hold a meeting<br>Auto-track consensus &分歧, reach conclusions</div>
```

### 4.4 demo.gif

The demo GIF contains Chinese text in the terminal output. Two options:
1. **Re-record** with English demo output (recommended)
2. **Keep as-is** with a note that it shows Chinese UI (acceptable for v1)

---

## 5. Translation Quality Standards

| Criterion | Requirement |
|-----------|-------------|
| **Tone** | Technical, concise, developer-friendly |
| **Terminology** | Use standard English CS terms (convergence, round, participant, speak) |
| **Code examples** | Keep variable names in English; translate string literals and comments |
| **Consistency** | Same term throughout (e.g., always "round" not "turn/iteration") |
| **Naturalness** | Not word-for-word; should read like native English docs |
| **Technical accuracy** | Preserve all technical meaning; no lossy translation |

### Glossary (Must Be Consistent)

| Chinese | English | Notes |
|---------|---------|-------|
| 圆桌 | Roundtable | Keep brand name |
| 讨论 | Discussion | Not "conversation" |
| 轮 | Round | Not "turn" or "iteration" |
| 发言 | Speak / Statement | Context-dependent |
| 参与者 | Participant | Not "member" |
| 共识 | Consensus | Standard term |
| 分歧 | Disagreement | Standard term |
| 收敛度 | Convergence score | Keep "score" |
| 总结 | Summary | Not "conclusion" |
| 通知 | Notification | Standard term |

---

## 6. Implementation Plan

### Phase 1 — P0 (1-2 days)

1. Translate `README.md` to English
2. Create `docs/zh/README.md` with original Chinese version
3. Translate `social-preview.html` tagline
4. Translate demo data in `core.py`

### Phase 2 — P1 (1 day)

5. Translate code comments in `core.py`
6. Translate `docs/API.md` and `docs/INTEGRATION.md`
7. Translate `docs/architecture.md`
8. Fix mixed Chinese in `src/skills/SKILL.md`

### Phase 3 — P2 (Optional)

9. Re-record `demo.gif` with English output
10. Update PyPI long_description to English

---

## 7. Acceptance Criteria

### Must Pass

- [ ] README.md is fully English (no Chinese characters in user-facing text)
- [ ] `pip show roundtable-ai` shows English description
- [ ] GitHub repo description and topics are English
- [ ] `demo()` runs and prints English output
- [ ] `social-preview.html` renders English tagline
- [ ] All code examples in README run correctly with English strings

### Should Pass

- [ ] `docs/API.md` and `docs/INTEGRATION.md` are English
- [ ] No Chinese in any user-facing file under `docs/`
- [ ] `docs/zh/README.md` preserves original Chinese README

### Nice to Have

- [ ] `demo.gif` shows English terminal output
- [ ] PyPI page reads naturally in English

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Translation loses technical nuance | Medium | Use glossary; have technical reviewer check |
| demo.gif re-recording effort | Low | Defer to P2; keep Chinese version for now |
| Breaking code examples | High | Run all examples after translation |
| Chinese users lose comfort | Low | Keep `docs/zh/README.md` as reference |

---

## 9. Out of Scope

- Internationalization (i18n) framework or locale switching
- Multi-language CLI output (English only for now)
- Translation of internal docs (PRDs, design specs, discussions)
- Right-to-left (RTL) language support
