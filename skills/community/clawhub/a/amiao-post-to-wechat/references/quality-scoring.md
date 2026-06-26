# Quality Scoring Rubric

## Scoring Model

Score = sum of all dimension scores. Max = 100.

---

## Dimension 1: opening_hook (0–20)

Score the first paragraph of the article body (after any H1 title).

| Score | Condition |
|-------|-----------|
| 18–20 | Strong pull: direct conclusion, sharp conflict, concrete scene, or provocative question. Reader has a reason to continue. |
| 13–17 | Decent setup: context is given, some forward motion, but not sharply compelling. |
| 7–12 | Flat context: background info only, no tension or pull. |
| 0–6 | Generic AI opener: "在当今…背景下", "随着…的发展", restated title as first sentence. |

---

## Dimension 2: heading_quality (0–15)

Evaluate all H2 and H3 headings.

| Score | Condition |
|-------|-----------|
| 13–15 | Headings read like real reader questions or judgment statements. Specific. Varied. e.g. "镍价为什么这次跌得这么快" |
| 9–12 | Headings are functional labels. Adequate but generic. e.g. "原因分析" "市场走势" |
| 5–8 | Headings are weak or missing in long sections. |
| 0–4 | No headings in body over 600 chars, or headings that are just numbered: "一、", "二、" |

---

## Dimension 3: paragraph_rhythm (0–15)

Evaluate distribution of paragraph lengths across the body.

| Score | Condition |
|-------|-----------|
| 13–15 | Clear variation: mix of 1–2 sentence punchy paragraphs and 3–5 sentence explanation paragraphs. No 5+ consecutive same-length paragraphs. |
| 9–12 | Some variation but majority uniform. |
| 5–8 | Most paragraphs same length (e.g. all 3-sentence blocks). |
| 0–4 | All paragraphs identical length, or one massive wall of text. |

---

## Dimension 4: ai_tone_density (0–20)

Count occurrences of AI-tone signals. Lower count = higher score.

**Blocked signals (universal)**:
- 值得注意的是
- 总的来说
- 从某种意义上说
- In conclusion
- It is worth noting that
- 综上所述
- 不难看出
- 毋庸置疑

**Domain-specific blocked signals** (apply when configured in EXTEND.md `domain_ai_tone_signals`):
- 在全球不锈钢市场持续波动的背景下
- 综合多方因素分析
- 值得业内人士关注的是
- 从当前行业发展趋势来看
- 在多重因素共同作用下
- *(plus any account-level additions)*

**Scoring**:
| Blocked phrase count | Score |
|---------------------|-------|
| 0 | 20 |
| 1 | 16 |
| 2 | 12 |
| 3 | 7 |
| 4+ | 3 |

---

## Dimension 5: term_preservation (0–10)

Check all terms listed in `protected_terms` (global + account-level).

| Score | Condition |
|-------|-----------|
| 10 | All protected terms intact as configured |
| 7 | 1 term simplified or paraphrased |
| 4 | 2 terms altered |
| 0 | 3+ terms altered or this dimension is irrelevant (no protected_terms configured) → award 10 |

If no `protected_terms` configured, award full 10 points by default.

---

## Dimension 6: ending_quality (0–10)

Evaluate the closing section (after the last body section, before keyword block).

| Score | Condition |
|-------|-----------|
| 9–10 | Human close that summarizes with a viewpoint, asks a grounded question, or invites action. CTA matches article type (see CTA types below). |
| 6–8 | Functional close. Wraps up adequately. CTA present but generic. |
| 3–5 | Template ending: "综上所述，…" / "希望对读者有所帮助" style. |
| 0–2 | Abrupt cut, no close, or pure keyword dump as ending. |

**CTA types**:
- `technical`: "欢迎留言讨论实际工况 / 您的项目用的是哪种规格？"
- `market`: "关注后查看历史价格走势 / 行情追踪就在这里"
- `science`: "转发给需要的同行 / 收藏备用"
- `generic`: "欢迎关注 / 持续更新"

---

## Dimension 7: length_fit (0–10)

Compare article body length to `default_article_length` (default: 2000 chars).

| Condition | Score |
|-----------|-------|
| Within 0–110% of target | 10 |
| 111–130% of target | 7 |
| 131–150% of target | 4 |
| > 150% of target (unless user requested long-form) | 1 |
| < 60% of target (content likely thin) | 5 |

If user explicitly requested longer content, award 10 regardless.

---

## Score Interpretation

| Total | Meaning | Action |
|-------|---------|--------|
| 85–100 | Excellent | Proceed with confidence |
| 70–84 | Good | Proceed; note any low dimensions |
| 60–69 | Acceptable | Proceed with warning; show weak dimensions |
| 50–59 | Weak | One more editorial pass recommended |
| < 50 | Poor | Mandatory additional pass; block turbo mode |

---

## Score Display Format (in pre-publish confirmation)

```
质量评分 Score: 76/100
  ✓ opening_hook    18/20
  ✓ heading_quality 13/15
  ⚠ paragraph_rhythm  9/15  (rhythm could vary more)
  ✓ ai_tone_density  16/20  (1 phrase removed)
  ✓ term_preservation 10/10
  ✓ ending_quality    8/10
  ✓ length_fit        2/10  ← wait this should show actual
```

Only show dimensions with score < 80% of max if space is tight. Always show total.
