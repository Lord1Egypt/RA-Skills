# full-page-translate

Translate a full article from a foreign URL into natural, publication-quality Simplified Chinese markdown.

## Trigger

When user sends a link in format:
`https://r.jina.ai/https://example.com/article`
Or:
`translate: https://example.com/article`

## Workflow

### Step 1: Fetch Content

GET markdown content from `r.jina.ai/{url}`. If the URL doesn't already have the `r.jina.ai/` prefix, add it automatically.

### Step 2: Content Analysis

Before translating, read through the full article and identify:

- **Subject & context**: what the article is about, its background knowledge
- **Key terminology**: technical terms, proper nouns, and domain-specific jargon; decide consistent Chinese translations upfront
- **Tone & style**: is it casual/formal/technical/storytelling? Match the tone in Chinese
- **Figurative language**: metaphors, idioms, cultural references that need adaptation rather than literal translation

### Step 3: Translate

Translate the full article into Simplified Chinese, following these principles:

- **Natural Chinese expression**: write as a native Chinese writer would, not as a translator. Avoid translationese (翻译腔) and Europeanized sentence structures (欧化中文)
- **Terminology consistency**: use the terminology decisions from Step 2 throughout
- **Sentence restructuring**: break long compound sentences into shorter, natural Chinese sentences when needed. Chinese favors shorter clauses connected by logic rather than nested subordinate clauses
- **Cultural adaptation**: adapt idioms and cultural references to Chinese equivalents where appropriate; keep original when the reference itself is the point
- **Preserve structure**: keep the original markdown structure (headings, lists, code blocks, links, images)
- **No additions or omissions**: translate everything; do not summarize, skip, or add commentary

For long articles (over 4000 words), split into logical chunks at heading boundaries and translate each chunk, then merge the results to ensure consistency.

### Step 4: Review & Polish

After translating, do a final pass to check:

- **Accuracy**: no meaning distortion or omission
- **Fluency**: read it aloud mentally — does it sound like natural Chinese writing?
- **Translationese check**: eliminate remaining patterns like 被动句滥用 (overuse of 被), 的的的 chains, or unnatural word order
- **Terminology consistency**: same term translated the same way throughout
- **Formatting**: markdown renders correctly, no broken links or structure

## Built-in Glossary

Common terms that should be translated consistently:

| English | Chinese |
|---|---|
| AI Agent | AI 智能体 |
| Prompt | 提示词 |
| Token | Token（不翻译） |
| Fine-tuning | 微调 |
| Hallucination | 幻觉 |
| RAG (Retrieval-Augmented Generation) | 检索增强生成 |
| Embedding | 向量嵌入 |
| LLM (Large Language Model) | 大语言模型 |
| Open Source | 开源 |
| Vibe Coding | 氛围编程 |
| Context Window | 上下文窗口 |
| Inference | 推理 |
| Benchmark | 基准测试 |
| Multimodal | 多模态 |
| Agentic | 智能体化的 |

Use this glossary as default. If the article's domain requires additional terms, decide translations in Step 2 and apply them consistently.
