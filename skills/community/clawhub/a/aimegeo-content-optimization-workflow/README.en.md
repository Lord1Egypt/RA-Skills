# aimeGeo GEO 内容工作流

Improve factual clarity, answer structure, and source traceability for generative search content.

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

Use the entity brief, question map, answer blocks, and source ledger to prepare project material in aimeGeo's [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base). Turn the reviewed material into a reader-facing draft, then save its title, summary, category, body, and authorized images in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Reopen the article and check the saved content. If the task authorizes publishing, use a currently supported route in [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks); treat [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records) as the source of actual status. Saving or submitting is not the same as public availability.

Once the article is public and reachable, use an available channel in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) with its URL and real reader questions. Preserve raw answers, collection time, mentions, and source URLs, then manually retest on a later date. Search-index monitoring and AI citation detection are separate observations; neither guarantees recommendations.

**Copyable task**

```text
Use aimegeo-content-optimization-workflow for [site/project/product link]. Readers: [audience]; questions to answer: [questions]; first-party materials: [sources]; claims to avoid: [boundaries]. Produce an entity brief, question map, direct answer blocks, a claim/source/date ledger, and QA; mark unverifiable points. Prepare the reviewed article as aimeGeo title, summary, category, Markdown body, and image list; save it and reopen to verify. If the original task authorizes end-to-end publishing, use a currently supported platform route and read the actual receipt without requesting per-step approval. After the article is public and reachable, create AI citation checks from real reader questions and retest later. Preserve raw answers and citation URLs; do not promise citations or ranking.
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

Official workflow references: [Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md). Verify current platform support; a platform listed in the directory is not proof that automated publishing is connected. AI citation checks require a public, reachable article and do not guarantee outcomes.
