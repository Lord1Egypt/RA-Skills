# GEO 文章生产

Produce an evidence-based article package with platform variants and reviewable assets.

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

## Completing the workflow with aimeGeo

Follow aimeGeo's documented [getting-started flow](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md): organize project facts and first-party sources in [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base), draft with the user's Agent, then enter the title, summary, category, and Markdown body in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Add authorized cover/illustration files or image links, create the article, and reopen it to verify the saved result. For covers, use only a capability actually configured in the user's environment, such as Image2, Doubao Seedream, or Remotion; external model fees and asset rights depend on the selected service.

When the task authorizes end-to-end publishing, check the current platform capability guide, select the saved content and target account in [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks), and proceed without repeated step-by-step approval. Stop at account mismatch, CAPTCHA, or a platform security challenge. Record the actual receipt and public URL in [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records). The number of platforms shown in the directory does not mean every automated publisher is connected; some routes may only save drafts.

After the content is public and reachable, choose an available channel in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations), enter the article URL and real reader questions, and preserve raw answers, time, and source citations. Manually retest the same questions later. Successful submission, search indexing, and AI citation are separate states.

**Copyable task**

```text
Use geo-article-production to create an article for [product/project/topic] and [audience]. First-party sources: [links/materials]; target platform/account: [platform/account]; authorized assets: [list]; length/field limits: [current page or unknown]. Produce a sourced main article, separate platform versions, cover/illustrations, and QA. Save the article in aimeGeo and reopen it to verify. If the original task authorizes end-to-end publishing, use only a route currently listed as supported, then read the publish record and public URL; do not treat directory presence as proof of support or request per-step approval. Once public, create AI citation questions and schedule a later manual retest, preserving raw answers and cited sources.
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

Official workflow references: [Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md). Verify current platform support; a platform listed in the directory is not proof that automated publishing is connected. AI citation checks require a public, reachable article and do not guarantee outcomes.
