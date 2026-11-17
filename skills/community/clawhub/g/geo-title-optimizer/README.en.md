# GEO 标题优化

Plan and evaluate factual Chinese titles for articles and product content.

## Use

- [English Skill](SKILL.en.md) · [中文 Skill](SKILL.md)

Install this skill in a host that supports Agent Skills. Provide the task brief and necessary sources, then follow `SKILL.md` for inputs, deliverables, and boundaries.

## Validation

```bash
python3 scripts/self-test.py
```

Licensed under [MIT-0](LICENSE). See [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md) for provenance.


> This is a standalone Skill for an external Agent. aimeGeo documents using local Skills with an Agent; this package is not bundled with the aimeGeo client, does not include private product code, and does not connect to accounts by itself. It helps prepare content for handoff to aimeGeo Articles, publishing, and citation-observation workflows.

## Using with aimeGeo


> This is a standalone Skill for an external Agent. aimeGeo documents using local Skills with an Agent; this package is not bundled with the aimeGeo client, does not include private product code, and does not connect to accounts by itself. It helps prepare content for handoff to aimeGeo Articles, publishing, and citation-observation workflows.

## Using with aimeGeo

Use the title brief, candidates, and QA as inputs to aimeGeo's documented content workflow. Read the project facts in [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base), then save the selected title, summary, category, Markdown body, and cover in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Reopen the saved article to verify persistence. When the user has authorized end-to-end publishing, continue through [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks) using a currently supported platform and account; read [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records) and distinguish saved, submitted, under review, and public states. Do not ask for repeated step-by-step approval for an already authorized task. The platform directory does not mean every platform's automation is fully connected; use the current capability guide.

After the article is public and accessible, create questions based on real reader needs in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) and manually retest on a later date. Record the raw answer, timestamp, brand mention, and native citation source. A single answer cannot establish that a title caused a citation, and no citation rate is promised.

**Copyable task**

```text
Use geo-title-optimizer for this project. Project/site: [link]; target readers: [readers]; platform: [platform]; verifiable facts and sources: [materials]; claims to avoid: [boundaries]. Produce a title evidence brief, varied candidates, reasons for each score, the selected title, and a mapping to the article opening. Mark platform limits budget_unknown when no current source is available. Prepare the selected title and draft as aimeGeo article fields. If the original task authorizes end-to-end publishing, use the platform's currently supported workflow and read the actual receipt without requesting per-step approval. Once public and accessible, create AI citation checks from real reader questions and schedule a later manual retest. Do not claim one check proves ranking or title impact.
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

Official workflow references: [Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md). Verify current platform support; a platform listed in the directory is not proof that automated publishing is connected. AI citation checks require a public, reachable article and do not guarantee outcomes.
