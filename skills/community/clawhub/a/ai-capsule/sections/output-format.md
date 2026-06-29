# Output Format Specification

## Card Format

```markdown
### #N ★★★★☆ 7.2/10 · [Article Title]

🔗 [URL](URL)
📌 **[Source Name]** · engineer · learn mode · 🎯 **READ**
`Relevance:8` `Utility:7` `Novelty:6` `Depth:8` | `Wow:5` `Perspective:6` `Cross-domain:4`

- **Relevance:** [tech stack / scenario match reason]
- **Utility:** [specific deliverable description]
- **Novelty:** [specific technical differentiator]
- **Depth:** [information density description]
- **Wow:** [counter-intuitive or elegant aspect]
- **Perspective:** [new concept / new perspective description]
- **Cross-domain:** [cross-domain inspiration point]

**Summary:** [article entity + core value, one sentence, no filler phrases]

**Value:** [based on F score — F≥8: write specific intersection with your tech stack (what you can do / save / avoid); F=4-7: write indirect value; F≤3: write "A quick scan for industry context is enough"]

---
```

**Action tag display rules:**
- `🎯 **TRY**` — article contains a GitHub repo / runnable code / dataset
- `🎯 **READ**` — deep content worth reading in full
- `🎯 **SCAN**` — news brief or low-score item, a quick skim is enough

## Language Adaptation

`output_language` controls the language of all card text. Reference table:

| Element | zh (Chinese) | en (English) |
|---------|-------------|--------------|
| Score tags | `匹配:8` `实用:7` `新颖:6` `深度:8` \| `震撼:5` `认知:6` `跨界:4` | `Relevance:8` `Utility:7` `Novelty:6` `Depth:8` \| `Wow:5` `Perspective:6` `Cross-domain:4` |
| Reason labels | `- **匹配**` `- **实用**` `- **新颖**` `- **深度**` `- **震撼**` `- **认知**` `- **跨界**` | `- **Relevance**` `- **Utility**` `- **Novelty**` `- **Depth**` `- **Wow**` `- **Perspective**` `- **Cross-domain**` |
| Summary / Value labels | `**内容：**` `**价值：**` | `**Summary:**` `**Value:**` |
| Mode annotation | `学习模式` `解决模式` `探索模式` | `learn` `solve` `scout` |
| Daily report header | `AI 胶囊日报` | `AI Capsule Daily` |
| Low-F value line | 快速扫一眼了解行业背景即可 | A quick scan for industry context is enough |

**Proper nouns always stay in original form** (unaffected by `output_language`): article titles, model names, framework names, GitHub repo names, URLs, Action tags (TRY/READ/SCAN), score numbers.

## Daily Report Header

```markdown
# AI Capsule Daily — YYYY-MM-DD

Sources: all · Identity: engineer · learn mode · N articles total

---
```

## Source Name Reference (📌 must use one of the following)

| Source name | Data source |
|------------|-------------|
| `HuggingFace Papers` | huggingface.co/api/papers |
| `OpenAI Blog` | openai.com/news/rss.xml |
| `Microsoft Research` | microsoft.com/en-us/research/feed |
| `Anthropic Product Blog` | claude.com/blog |
| `Anthropic Engineering` | anthropic.com/engineering |
| `Anthropic News` | anthropic.com/news |
| `Google DeepMind` | deepmind.google/blog |
| `Meta AI` | ai.meta.com/blog |
| `Simon Willison` | simonwillison.net |
| `Eugene Yan` | eugeneyan.com |
| `Chip Huyen` | huyenchip.com |
| `Ben's Bites` | bensbites.com/feed |
| `Product Hunt Daily` | producthunt.com/leaderboard/daily |
| `GitHub Trending` | github.com/trending |
| `Hacker News` | hnrss.org (100+ points) |
| `Reddit LocalLLaMA` | reddit.com/r/LocalLLaMA (Tavily search) |

## Scoring Reason Rules

**Reasons must describe the specific content entity of the article** — filler and vague language are prohibited:
- ❌ Wrong: "The article is very in-depth and worth reading carefully"
- ❌ Wrong: "Limited" / "None" / "Not relevant" (these are not reasons — they avoid writing a reason)
- ✅ Correct: "The article includes a runnable Colab Notebook and a link to download a cleaned JSON dataset"
- ✅ Low scores still need specific reasons, for example:
  - Low W: `Experimental results improve within expected range on standard benchmarks — no counter-intuitive findings`
  - Low S: `Method discussed entirely within NLP — no perspective borrowed from other fields`
  - Low R: `Subject is Vietnamese speech recognition — no intersection with the engineer's LLM app development context`

Reason format per dimension:
- **R**: state the specific reason the tech stack / scenario matches or doesn't match
- **U**: enumerate the specific deliverable entities in the article, or explain why usable output is absent
- **N**: point to a specific technical differentiator or metric, or explain why this is already known
- **D**: describe the information density and how the argument is made
- **W/P/S**: objectively describe the specific effect achieved, old-vs-new concept contrast, or cross-domain entity; if score is low, explain why the dimension's threshold wasn't met

**Two-line summary rules:**
- **Summary line**: describe the article's specific content entity and core value — no filler phrases
- **Value line**: written from the personal fit angle of the F dimension — not a generic recommendation:
  - F≥8 (high match): write the **specific intersection** with your tech stack — what you can directly use, what you save, what pitfall you avoid
    - ✅ "Directly applicable to your own Agent harness design — saves architecture exploration time"
    - ✅ "Test whether it can replace the custom crawler in your RAG pipeline — see if declarative extraction is enough"
  - F=4-7 (medium match): write **indirect value** — know the direction, use as background for tech decisions, judge if it's worth digging deeper
    - ✅ "Understand the multi-agent safety research direction — consider isolation mechanisms early when designing Agent collaboration"
  - F≤3 (low match): **write directly** "A quick scan for industry context is enough" — do not fabricate value
  - ❌ "Very useful reference for AI engineers" (doesn't say which tech stack it relates to)
  - ❌ "Worth reading carefully" (doesn't say why it's worth your time)
