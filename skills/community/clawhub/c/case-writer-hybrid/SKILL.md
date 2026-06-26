---
name: case-writer-hybrid
description: Expand a structured brief in `content-production/inbox/` into a reusable long-form markdown article draft, then run a local writer / critic / judge quality loop with a constrained humanization pass. Use when Codex needs a stage-1 article draft plus reusable writing sidecars for downstream `generate-image` and `wechat-formatter`.
---

# Case Writer Hybrid

Turn the structured brief into a stage-1 article draft, a writing pack sidecar, and a review trace that can flow into image generation and WeChat formatting.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill case-writer-hybrid --input content-production/inbox/20260403-ai-content-system-brief.md
```

## Prepare Input

Expect a markdown file with these sections:

- `基础信息`
- `核心观点`
- `背景与语境`
- `论证方向`
- `可用案例 / 素材`

Important fields inside `基础信息`:

- `date`
- `slug`
- `topic`
- `target_reader`
- `publish_goal`

## Follow Drafting Workflow

1. Read the brief and preserve explicit user-supplied claims, framing, and evidence.
2. Use `论证方向` as the backbone for the major argument sections.
3. Pull material from `可用案例 / 素材` into the matching sections instead of inventing new examples first.
4. Build a stable first draft structure: title, 导语, 问题提出, 核心判断, 论证段, 结论, 可传播总结.
5. Run up to 3 local rounds of `writer -> critic -> humanizer-zh -> judge`.
6. If the score still fails after 3 rounds, stop and emit a quality-gate notice instead of continuing downstream.

## Write Output

Write the markdown draft to:

```text
content-production/drafts/<slug>-article.md
```

Also write:

```text
content-production/drafts/<slug>-writing-pack.md
content-production/drafts/<slug>-writing-pack.json
content-production/drafts/<slug>-review-trace.json
```

If the draft fails the quality gate after 3 rounds, also write:

```text
content-production/published/YYYYMMDD-<slug>-quality-gate.md
```

## Respect Constraints

- Treat the result as a controlled local draft loop, not a free-form creative writer
- If the brief is sparse, preserve structure and fill gaps conservatively
- Prefer explicit user-supplied arguments over invented framing
- Do not continue to image generation or formatting if the quality gate fails

## Read Related Files

- Runtime entry: `skill_runtime/engine.py`
- Usage guide: `docs/case-writer-hybrid-execution-spec.md`
- Downstream skills: `generate-image`, `wechat-formatter`
