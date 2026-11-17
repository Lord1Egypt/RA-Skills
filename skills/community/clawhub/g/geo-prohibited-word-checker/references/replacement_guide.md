# GEO Prohibited Word Replacement Guide

Use this guide to generate contextually appropriate replacements for prohibited words detected in GEO/SEO content. The goal is to **preserve the original meaning** while removing compliance risks.

## Core Principles

1. **Semantic preservation**: The sentence must convey the same idea after replacement — just in a compliant way.
2. **Tone downgrade**: Absolute, exaggerated, or superlative claims should be softened to objective, moderate language.
3. **Delete when necessary**: If the prohibited word is core to illegal content (drugs, gambling, weapons), delete or substantially rewrite the surrounding passage.
4. **Read naturally**: The replaced text must read smoothly — no awkward phrasing, no obvious "compliance censoring" style.

## Replacement by Category

### Category 1: Advertising Law Prohibited Terms (广告法违禁词)

These are absolute superlatives and exclusivity claims banned under Chinese advertising law.

| Strategy | Example |
|---|---|
| Replace superlatives with descriptors | "最好" → "优秀的", "全球第一" → "行业前列" |
| Soften absolute claims | "独一无二" → "独具特色", "绝无仅有" → "难得一见" |
| Remove ranking claims | "排名第一" → "备受欢迎", "销量冠军" → "市场反响热烈" |
| Replace "最" words | "最佳" → "理想", "最高级" → "高水准", "最便宜" → "实惠" |
| Downgrade prestige terms | "顶级" → "优秀", "王牌" → "明星", "金牌" → "精品" |
| Neutralize exclusivity | "唯一" → "其中之一", "独家" → "专有", "首选" → "推荐选择" |

### Category 2: Exaggerated Promotion (夸大宣传词)

These are sensational or exaggerated marketing terms.

| Strategy | Example |
|---|---|
| Replace emotional/sensational terms | "疯狂抢购" → "受到广泛关注", "震惊" → "引人注目" |
| Use objective language | "颠覆行业" → "推动行业创新", "炸裂登场" → "全新亮相" |
| Remove urgency baiting | "不容错过" → "值得关注", "最后机会" → "限时活动" |
| Downgrade clickbait | "惊人发现" → "研究发现", "颠覆认知" → "带来新认识" |
| Use measured enthusiasm | "绝佳" → "出色的", "完美" → "令人满意的" |

### Category 3: Illegal Content (违法内容词)

Drugs, gambling, weapons, and other clearly illegal content references.

| Strategy | Example |
|---|---|
| Delete entirely | Delete the word and rewrite the sentence if it's central to the meaning |
| Replace with legitimate concept | "赌博机" related content → remove entirely |
| Rewrite passage | If a paragraph revolves around illegal content, rewrite it with compliant content |
| Use generic placeholders only if unavoidable | Only as last resort, and only when the word is not central |

**Important**: For this category, preservation of meaning is secondary to compliance. Delete first.

### Category 4: Misleading Claims (误导性词汇)

Health, financial, or product claims that could mislead consumers.

| Strategy | Example |
|---|---|
| Add qualifiers and caveats | "包治百病" → "有助于改善健康状况" |
| Use conditional language | "根治" → "辅助缓解", "永不复发" → "降低复发风险" |
| Reference factual basis | "神药" → "效果显著的药物方案", "祖传秘方" → "传统配方" |
| Remove guarantee language | "保证有效" → "对多数用户有帮助", "100%有效" → "效果明显" |

## Handling Overlapping Matches

When one prohibited word is a substring of another (e.g., "第一" inside "排名第一"):

1. The detection script outputs matches sorted by word length (longest first)
2. **Always process longest words first** — replace "排名第一" before "第一"
3. After replacing a longer word, re-check whether the shorter word still exists in the remaining text
4. If the shorter word was only present inside the longer word, it is automatically resolved — skip it

### Example

```
Original: "我们的产品排名第一，是行业的首选品牌。"

Matches detected: ["排名第一"(len=4), "首选"(len=2), "第一"(len=2)]

Processing order:
1. "排名第一" → replace with "广受好评" → "我们的产品广受好评，是行业的首选品牌。"
2. "首选" → replace with "推荐" → "我们的产品广受好评，是行业的推荐品牌。"
3. "第一" → check: no longer in text → skip
```

## Batch Replacement Workflow

When performing replacements:

1. Group matches by category for consistent strategy application
2. Process in order: illegal → misleading → advertising → exaggeration
3. For each match, read the context (before and after the word)
4. Generate the replacement text based on context and category
5. Apply replacements from end of text to beginning to preserve position indexes
6. After all replacements, read the full text once to verify natural flow

## Output Format

When presenting results to the user, show a comparison table:

| # | Position | Original | Replacement | Category |
|---|---|---|---|---|
| 1 | 42 | 排名第一 | 广受好评 | advertising |
| 2 | 58 | 首选 | 推荐 | advertising |
| 3 | 120 | 顶级 | 优秀 | advertising |

Then save the cleaned file with `_clean` suffix (e.g., `article_clean.md`).
