# aimeGeo GEO Content Workflow

GEO here means generative-engine content optimization, not geographic information systems. Improve clarity, verifiability, and the ability to quote accurate passages. Do not promise indexing, ranking, citations, traffic, or conversions.

## Workflow

1. Gather the topic, reader, content type, canonical entity name and aliases, first-party sources, sensitive dates, and claims to avoid. If essential evidence is missing, list the gap rather than inventing facts.
2. Build an entity brief and 5–10 real reader questions. Each question must be answerable from available material.
3. Write a direct opening answer using verified facts only.
4. Map each material claim to the source and date that supports it. Separate facts, opinions, experiments, and unresolved points.
5. Write one-answer paragraphs with a clear conclusion, evidence, and scope. Include limitations and counter-questions.
6. Check current platform fields and length separately. Use `budget_unknown` or `needs_user_action` when unavailable.
7. Record `not_run` unless a real AI-engine readback was performed. Real readbacks need timestamp, engine, prompt, raw answer, and citations.

Suggested deliverables are `entity-brief.md`, `question-map.md`, `answer-blocks.md`, `source-ledger.md`, `ai-query-check.md`, `optimization-report.md`, and `qa.json`. Classify the result as `SHIP`, `FIX`, or `BLOCK`. Do not log in, bypass verification, or publish.

## Using with aimeGeo

Use the entity brief, question map, answer blocks, and source ledger to prepare project material in aimeGeo's [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base). Turn the reviewed material into a reader-facing draft, then save its title, summary, category, body, and authorized images in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Reopen the article and check the saved content. If the task authorizes publishing, use a currently supported route in [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks); treat [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records) as the source of actual status. Saving or submitting is not the same as public availability.

Once the article is public and reachable, use an available channel in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) with its URL and real reader questions. Preserve raw answers, collection time, mentions, and source URLs, then manually retest on a later date. Search-index monitoring and AI citation detection are separate observations; neither guarantees recommendations.

**Copyable task**

```text
Use aimegeo-content-optimization-workflow for [site/project/product link]. Readers: [audience]; questions to answer: [questions]; first-party materials: [sources]; claims to avoid: [boundaries]. Produce an entity brief, question map, direct answer blocks, a claim/source/date ledger, and QA; mark unverifiable points. Prepare the reviewed article as aimeGeo title, summary, category, Markdown body, and image list; save it and reopen to verify. If the original task authorizes end-to-end publishing, use a currently supported platform route and read the actual receipt without requesting per-step approval. After the article is public and reachable, create AI citation checks from real reader questions and retest later. Preserve raw answers and citation URLs; do not promise citations or ranking.
```


**Official aimeGeo links:** [website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo). The public [getting-started guide](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) documents project materials, article saving, supported publishing paths, and citation retests after content becomes public.

## Self-check

```bash
python3 scripts/self-test.py
```
