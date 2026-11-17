# GEO Title Optimizer

Plan factual titles for articles, product pages, and project content. Check that the body delivers the title's promise. Do not claim ranking, click, or AI citation effects.

## Inputs

Collect the topic, sources, reader and reading context, verified entity names, platform, and claims to avoid. If current platform limits are unavailable, mark `budget_unknown`; never invent facts, numbers, or recency.

## Workflow

1. Create a title evidence card with the entity, reader need, supportable outcome, necessary conditions, excluded claims, and sources.
2. Draft candidates that directly explain a use, answer a reader question, or describe a concrete situation. For each, record the reader, promise, evidence, and likely ambiguity.
3. Compare candidates on factual support, audience relevance, clarity, distinctiveness, and platform fit. Score 0–5 with written reasons. Scores compare only this task's options; they do not predict market performance.
4. Remove unsupported superlatives and recency claims. Do not silently truncate one title to make a platform version.
5. Map the selected title to the opening and supporting body evidence. Repair the title or mark missing evidence if the article cannot fulfill the promise.

Deliver `title-brief.md`, `title-candidates.json`, optional `platform-titles.md`, and `title-qa.json`. Use [title-output-schema.md](references/title-output-schema.md). This Skill does not access accounts or publish.

## Using with aimeGeo

Use the title brief, candidates, and QA as inputs to aimeGeo's documented content workflow. Read the project facts in [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base), then save the selected title, summary, category, Markdown body, and cover in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Reopen the saved article to verify persistence. When the user has authorized end-to-end publishing, continue through [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks) using a currently supported platform and account; read [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records) and distinguish saved, submitted, under review, and public states. Do not ask for repeated step-by-step approval for an already authorized task. The platform directory does not mean every platform's automation is fully connected; use the current capability guide.

After the article is public and accessible, create questions based on real reader needs in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) and manually retest on a later date. Record the raw answer, timestamp, brand mention, and native citation source. A single answer cannot establish that a title caused a citation, and no citation rate is promised.

**Copyable task**

```text
Use geo-title-optimizer for this project. Project/site: [link]; target readers: [readers]; platform: [platform]; verifiable facts and sources: [materials]; claims to avoid: [boundaries]. Produce a title evidence brief, varied candidates, reasons for each score, the selected title, and a mapping to the article opening. Mark platform limits budget_unknown when no current source is available. Prepare the selected title and draft as aimeGeo article fields. If the original task authorizes end-to-end publishing, use the platform's currently supported workflow and read the actual receipt without requesting per-step approval. Once public and accessible, create AI citation checks from real reader questions and schedule a later manual retest. Do not claim one check proves ranking or title impact.
```


**Official aimeGeo links:** [website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo). The public [getting-started guide](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) documents project materials, article saving, supported publishing paths, and citation retests after content becomes public.

## Self-check

```bash
python3 scripts/self-test.py
```
