---
name: amiao-post-to-wechat
description: Editor-first WeChat Official Account publishing skill. Posts content to WeChat Official Account (微信公众号) via API or browser, while prioritizing humanized writing, WeChat-native formatting, compatibility, and efficient publishing. Supports article posting (文章) with HTML, markdown, or plain text input, and image-text posting (贴图/图文) with multiple images. Use when user mentions 发布公众号, 微信公众号, post to wechat, 公众号文章, 图文, 贴图, markdown 发公众号, 写完发一下, 帮我发到公众号, or similar.
version: 3.0.0
skill_schema: 1.0
metadata:
  openclaw:
    homepage: https://clawhub.ai/skills/amiao-post-to-wechat
    requires:
      anyBins:
        - bun
        - npx
changelog:
  - version: 3.0.0
    changes:
      - FSM-based workflow replacing linear checklist
      - 7-dimension quality scoring system (0-100) with per-publish logging
      - Auto-tune suggestions after every 10 publish cycles
      - Error levels 1-4 with automatic retry
      - Turbo mode for pre-polished content
      - Parallel side-computation in editorial pass
      - Industry terminology protection via config
      - Domain-specific AI-tone signal suppression
      - Access token cache with auto-refresh
      - Image source resolution with graceful fallback
  - version: 2.1.0
    changes:
      - Domain AI-tone signals and protected terms
      - Pre-publish confirmation step
      - Image source resolution order
      - CTA type guidance
      - Slug rules for Chinese titles
---

# WeChat Official Account Publishing Skill v3.0.0

## Language
Always match the user's language. Chinese input → respond in Chinese. English input → respond in English.

## Core Principle
This skill is an **editor-first, self-improving publishing pipeline** — not a raw uploader.

**Priority order**:
1. Humanized writing quality
2. WeChat compatibility
3. Visual readability
4. Publishing speed

Never sacrifice compatibility for fancy formatting. Never sacrifice readability for automation.

---

## Quick Reference

| Mode | When | Key flag |
|------|------|----------|
| Standard | Default | — |
| Turbo | Content already polished | `--turbo` or `turbo: true` in frontmatter |
| Raw | Skip all editorial pass | `--raw` |
| Image-text | Short post with images | auto-detected |

**Supported tones**: `专业评论` · `行业快评` · `知识科普` · `观点专栏` · `深度分析` · `快讯播报`

**Reference files** (load when needed):
- `references/fsm.md` — Full FSM state table
- `references/quality-scoring.md` — Scoring rubric details
- `references/editorial-rules.md` — Humanization + formatting rules
- `references/config-reference.md` — All EXTEND.md keys + full example
- `references/scripts.md` — Script CLI reference
- `references/troubleshooting.md` — Error levels + fix guide

---

## FSM Workflow (Summary)

Load `references/fsm.md` for the complete state transition table.

**State sequence**:
```
idle
  → loading_config
    → resolving_account
      → classifying_input
        → [turbo?] editorial_pass_light / editorial_pass_full
          → metadata_validation
            → packaging_check
              → pre_publish_confirm (if enabled)
                → publishing
                  → reporting → idle
```

**Key transition rules**:
- `editorial_pass_full` loops max **2 iterations** if quality_score < threshold; then warn + continue
- `packaging_check` auto-repairs what it can; halts only for missing cover (API mode)
- `publishing` auto-retries on LEVEL 1 errors (max 2 retries); escalates on LEVEL 3+
- Any state can transition to `error_report` on unrecoverable failure

---

## Error Levels

| Level | Type | Behavior |
|-------|------|----------|
| 1 | Transient (token expiry, network blip) | Auto-retry silently (max 2, wait 3–10s) |
| 2 | Auto-repairable (missing summary, cover fallback, over-length) | Repair + flag in confirmation |
| 3 | Requires user action (credentials missing, empty content) | Halt + exact setup guide |
| 4 | Unrecoverable API error | Log + show error code + link to mp.weixin.qq.com |

See `references/troubleshooting.md` for full repair paths.

---

## Quality Scoring (Pre-publish)

Score is computed before `pre_publish_confirm`. Load `references/quality-scoring.md` for rubric.

| Dimension | Max | Signal |
|-----------|-----|--------|
| opening_hook | 20 | First paragraph creates pull or tension |
| heading_quality | 15 | Reader-question style, not generic labels |
| paragraph_rhythm | 15 | Varied length, no mechanical same-beat paragraphs |
| ai_tone_density | 20 | Inverse: fewer blocked phrases = higher score |
| term_preservation | 10 | All `protected_terms` intact |
| ending_quality | 10 | Human close + CTA present |
| length_fit | 10 | Within `default_article_length`, not padded |
| **Total** | **100** | |

**Thresholds**:
- ≥ 70 → proceed normally
- 60–69 → proceed with warning in confirmation
- < 60 → another editorial pass (max 2 total)
- < 50 → halt even in Turbo mode

Show score + brief per-dimension note in `pre_publish_confirm`.

---

## Turbo Mode

Activated by `--turbo` flag or `turbo: true` in frontmatter.

**Skips**: deep humanization pass, pre-publish confirmation (auto-proceed), quality score display (only blocks if < 50)

**Still runs**: metadata resolution, packaging check (auto-repair), cover resolution, token cache check, publish, log

Use when content is already manually polished, or when batch-publishing multiple articles.

---

## Editorial Pass (Standard)

Load `references/editorial-rules.md` for full humanization rules, AI-tone signal list, and formatting downgrade table.

**Parallelizable side-computations** (run while main humanization pass runs):
- Slug generation (from title)
- Tail keyword generation (from article topic)
- Profile block inference (from account config)
- Image count assessment (from article length)

**Humanization strength**:
- `light`: minimal cleanup, preserve style
- `medium`: default; improve rhythm, headings, opening, ending
- `strong`: substantial rewrite while preserving meaning

**Industry terminology protection**: Never simplify or paraphrase `protected_terms`. These are load-bearing words for the target audience.

---

## Image Handling

**Count guidance by length**:
| Article length | Preferred images |
|---------------|-----------------|
| < 800 chars | 2 |
| 800–1500 chars | 2–3 |
| 1500–2000 chars | 3 (optionally 4) |
| > 2000 chars | compress content first, then reassess |

**Source resolution order**:
1. Inline images already in markdown / HTML
2. `imgs/` directory beside article file
3. User-supplied via `--images`
4. If insufficient: warn in confirmation, do not block publish

---

## Metadata & Packaging

**Metadata resolution** (each field):
- Title: CLI → frontmatter/H1 → strongest H2 → first meaningful sentence → auto-generate
- Summary: CLI → frontmatter → first paragraph trimmed → auto-generate
- Author: CLI → frontmatter → account default → global default

**Packaging checklist** (auto-repair if missing, unless `--raw`):
- [ ] Length within `default_article_length`
- [ ] 2–4 images (warn if under; do not block)
- [ ] Long-tail keyword block (3–8 phrases, topic-specific)
- [ ] Public-account profile block

**Cover image resolution** (API mode only):
1. `--cover` → frontmatter cover fields → `imgs/cover.png` → first inline image → halt if still missing

---

## Access Token Cache

Cache location (in priority order): `amiao/.wechat-token-cache` → `~/amiao/.wechat-token-cache`

Behavior: read cache → verify expiry → refresh if expired/invalid → update cache. Failure to refresh = LEVEL 1 retry, then LEVEL 3 if persistent.

---

## Publish Log + Auto-tune

Every successful publish appends one record to `amiao/.publish-log.yaml`:

```yaml
- date: <ISO8601+08:00>
  account: <alias>
  article_title: <title>
  quality_score: <0-100>
  humanize_level: <light|medium|strong>
  tone: <tone>
  article_length: <chars>
  image_count: <n>
  publish_method: <api|browser>
  media_id: <id>
  issues_found: [<list of flags>]
  cta_type: <type>
  tail_keywords: [<list>]
```

**Auto-tune** (triggered after every 10th publish cycle):
- Avg quality_score < 72 → suggest reviewing humanization defaults
- Tail keywords repeat too uniformly → suggest refreshing `default_tail_keywords`
- Article length consistently under/over → suggest adjusting `default_article_length`
- One tone consistently scores higher → suggest making it `default_tone`

Report suggestions at end of 10th cycle. Never auto-apply; always surface to user.

---

## Pre-publish Confirmation Summary

Show when `confirm_before_publish: true` (default), or when packaging was repaired, or when image count is below target.

```
───────────────────────────────────────
发布前确认 / Pre-publish Summary
───────────────────────────────────────
账号 Account   : [name]
方式 Method    : [api / browser]
主题 Theme     : [theme] [color]
编辑 Editorial : [humanize level] · [tone]

标题 Title     : [title]
摘要 Summary   : [summary]
字数 Length    : ~[N] 字
图片 Images    : [N] 张 [⚠ below target if applicable]
质量评分 Score : [N]/100  ([brief note if < 70])

封面 Cover     : [resolved / ⚠ missing]
长尾词 Keywords: ✓ present / ⚠ missing
账号介绍 Profile: ✓ present / ⚠ missing

[⚠ Any auto-repairs applied]
───────────────────────────────────────
确认发布？(y/n / 输入 e 返回编辑)
```

If `confirm_before_publish: false` and no warnings: skip confirmation, show summary inline in completion report instead.

---

## Completion Report

```
✓ WeChat Publishing Complete!

Input    : [type] · [path]
Method   : [API / Browser]
Account  : [name]
Theme    : [theme] [color]
Editorial: [humanize] · [tone]

Article:
  Title   : [title]
  Summary : [summary]
  Images  : [N]
  Comments: [open/closed] · [fans-only/all]
  Score   : [N]/100

Result:
  ✓ Draft saved to WeChat Official Account
  media_id: [id]   (API mode)

Files:
  [• slug.md if created from plain text]

Next: https://mp.weixin.qq.com → 内容管理 → 草稿箱
```

---

## Scripts

Load `references/scripts.md` for full CLI reference.

| Script | Purpose |
|--------|---------|
| `scripts/wechat-api.ts` | Article via API |
| `scripts/wechat-article.ts` | Article via browser |
| `scripts/wechat-browser.ts` | Image-text post |
| `scripts/md-to-wechat.ts` | Markdown → WeChat HTML |
| `scripts/check-permissions.ts` | Environment preflight |

Runtime: `bun` → `npx -y bun` → explain + suggest install

**Critical**: Publishing scripts handle markdown conversion internally. **Never pre-convert markdown to HTML before calling the publish script.**

---

## Configuration

Load `references/config-reference.md` for all supported EXTEND.md keys and a full annotated example.

**EXTEND.md location** (checked in order):
```bash
amiao/amiao-post-to-wechat/EXTEND.md          # project-level
${XDG_CONFIG_HOME:-$HOME/.config}/amiao/amiao-post-to-wechat/EXTEND.md
$HOME/amiao/amiao-post-to-wechat/EXTEND.md    # user-level
```

If not found → run first-time setup (`references/config/first-time-setup.md`) before proceeding.

**Value priority**: CLI → frontmatter → EXTEND (account → global) → skill defaults

---

## OpenClaw / ClawHub Rules

- `SKILL.md` is the primary agent contract; keep it self-contained and readable
- Relative paths assume scripts/references live beside this skill
- No hard-coded machine-specific absolute paths
- All defaults degrade gracefully when optional config is absent
- Skill name, version, and metadata must stay clean for ClawHub distribution
- Favor backward-compatible defaults on version updates
