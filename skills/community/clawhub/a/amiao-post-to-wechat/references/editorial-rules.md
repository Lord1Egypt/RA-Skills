# Editorial Rules

## 1. Humanization Rules (去AI化)

Prefer **editorial humanization**, not fake disguise. The goal is writing that reads like a knowledgeable human editor, not a robot pretending to be one.

### Universal AI-tone signals to reduce
- Mechanical "first, second, third" sequencing without narrative reason
- Repeated fillers: "值得注意的是" / "总的来说" / "从某种意义上说" / "In conclusion" / "It is worth noting that"
- Every paragraph having the same length and sentence rhythm
- Empty correctness without concrete scenes or judgment
- Over-complete summary tone, like answering an exam question

### Domain-specific AI-tone signals (for vertical industry accounts)
Default list (apply unless overridden by `domain_ai_tone_signals` in EXTEND.md):
- "在全球不锈钢市场持续波动的背景下……"
- "综合多方因素分析……"
- "值得业内人士关注的是……"
- "从当前行业发展趋势来看……"
- "在多重因素共同作用下……"

Account-specific `domain_ai_tone_signals` from EXTEND.md **replace** (not append to) this list.

### Humanization actions
- Vary paragraph length deliberately
- Mix short (1–2 sentence) and medium (3–4 sentence) blocks
- Use more direct phrasing
- Prefer concrete wording over abstract wording
- Keep one or two sharp judgment sentences when appropriate
- Use subheadings that reflect real reader questions
- Let the ending feel like a human editor wrapping up, not a template

### What to never do without explicit user instruction
- Invent facts
- Add statistics not in the source
- Change the author's core position
- Over-dramatize into clickbait
- Add emojis unless the user's style clearly includes them

---

## 2. Industry Terminology Protection

Never simplify, paraphrase, or replace terms listed in `protected_terms` (global or account-level). These are load-bearing words for the target audience.

If a term looks niche but is central to the article, preserve the original form unless the user explicitly requests simplification.

**Default protected terms example** (overridden by config):
- 双相钢
- 316L
- BA面
- 盐雾测试时长
- δ铁素体含量
- WRC-1992

---

## 3. Opening Hook Patterns

When the opening is weak, rewrite using one of these patterns:

| Pattern | Example |
|---------|---------|
| Direct conclusion | "镍价这轮跌，根子在印尼。" |
| Problem framing | "为什么同样的304，这家报价比那家低800一吨？" |
| Conflict opening | "供应端没问题，需求端没崩，价格却在跌——这不正常。" |
| Concrete scene | "上周有个客户来问：能不能用201代替304？我说：要看用在哪。" |

Avoid: "在当今全球不锈钢市场背景下……" / "随着行业不断发展……"

---

## 4. Ending + CTA Patterns

After the final content section, write a human close that:
- Summarizes with a viewpoint, OR
- Asks a grounded question readers can relate to, OR
- Invites a specific action

Then select CTA by `default_cta_type` (or infer from article type):

| CTA type | Trigger | Example |
|----------|---------|---------|
| `technical` | technical / process article | "你们项目现在用的是哪种规格？欢迎留言讨论。" |
| `market` | price / 行情 article | "关注公众号，每周持续追踪行情走势。" |
| `science` | 科普 / knowledge article | "觉得有用的话，转发给需要的同行。" |
| `generic` | default fallback | "关注[账号名]，持续更新行业干货。" |

---

## 5. Long-tail Keyword Block

Append after the closing section, before the profile block.

Rules:
- 3 to 8 phrases
- Topic-relevant, not generic stuffing
- Natural Chinese phrasing over SEO fragments
- Phrases should match likely WeChat search intent

Format:
```
相关长尾词：[词1]、[词2]、[词3]、[词4]
```

Examples by article type:
- 行情文: 不锈钢行情分析、304价格走势、镍价波动影响、双相钢选材
- 科普文: 公众号排版优化、微信图文发布、去AI化写作、微信公众号发文工具
- 技术文: 316L焊接要求、双相钢δ铁素体、不锈钢耐蚀性选材

---

## 6. Public-account Profile Block

Append at the very end of the article.

Required elements:
- Account / brand name
- What the account mainly publishes
- What value readers can expect
- Short follow/readership invitation
- 1–2 concrete identity details that make the account feel real

Style: concise, specific, not salesy, consistent with account tone.

If no explicit profile text is given, infer from:
1. `default_profile_block` in account config
2. `default_profile_block` in global config
3. Account name + inferred content type from article history

---

## 7. WeChat Formatting Rules

WeChat is not a browser. Favor robust, readable structures.

### Prefer
- Clear H1/H2/H3 hierarchy
- Short paragraphs (3–4 sentences max for dense topics)
- Quote blocks for key citations or pulled quotes
- Bullet lists with modest depth (max 2 levels)
- Simple highlighted takeaway blocks
- Single-column visual flow
- Bottom reference section for external resources

### Avoid or simplify
- Complex nested lists
- Multi-column layouts
- Wide tables
- Deeply nested blockquotes
- Heavy custom HTML/CSS
- Dense inline URL clutter

### Automatic downgrade rules
| Original | Downgrade to |
|----------|-------------|
| Wide table (4+ columns) | Compact list or summary block |
| Multi-column comparison | Stacked sections with clear H2 labels |
| Long inline URLs | Bottom reference section |
| Complex HTML block | Simple paragraph / quote / list |

### Link handling
- Ordinary external links → convert to bottom references by default
- Internal WeChat links (`mp.weixin.qq.com`) → keep inline by default
- Use `--no-cite` only when user explicitly wants all links inline

---

## 8. Visual Style by Article Type

| Type | Style |
|------|-------|
| 资讯/快评 | Compact, crisp, industrial brief. Dark tone. |
| 深度分析 | Restrained, serious, black/gray dominant. Generous whitespace. |
| 知识科普/专栏 | Warmer instructional style. Clear section guidance. |

If no style specified, choose best fit for article type while staying conservative.

One dominant accent color at most. Consistent section rhythm. Avoid flashy decoration.
