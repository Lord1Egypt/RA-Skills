# GEO Article Production

Turn a content brief into a sourced, reviewable article package and platform-specific variants. This Skill prepares content; it does not represent platform approval or publication.

## Inputs and workflow

Record the request, target reader, topic, target platforms, sources, authorized assets, and prohibited claims. Define the deliverable, verify facts and dates, draft the main article, create separate platform versions, check asset rights and metadata, run QA, and provide a handoff with files, version, checks, unresolved items, and actual status.

A portable package may contain `brief.md`, `sources.md`, `article.md`, `variants/`, `assets/asset-manifest.json`, `qa.json`, and `handoff.md`. Mark examples separately from real runs. Do not claim SEO/GEO ranking, citation, moderation, traffic, or conversion outcomes. Platform limits change; use current sources or mark them unknown.

## Publishing boundary

By default, create local content only. If the user authorized the full publishing task, use an available and currently supported product route without repeated step-by-step approvals. Stop at account mismatch or a platform security challenge. Record the actual receipt; distinguish saved, submitted, in-review, and publicly accessible states.

## Completing the workflow with aimeGeo

Follow aimeGeo's documented [getting-started flow](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md): organize project facts and first-party sources in [Project and Knowledge Materials](https://geo.aimmme.com/ag01/geo/prep/knowledge-base), draft with the user's Agent, then enter the title, summary, category, and Markdown body in [Articles](https://geo.aimmme.com/ag01/geo/writing/articles). Add authorized cover/illustration files or image links, create the article, and reopen it to verify the saved result. For covers, use only a capability actually configured in the user's environment, such as Image2, Doubao Seedream, or Remotion; external model fees and asset rights depend on the selected service.

When the task authorizes end-to-end publishing, check the current platform capability guide, select the saved content and target account in [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks), and proceed without repeated step-by-step approval. Stop at account mismatch, CAPTCHA, or a platform security challenge. Record the actual receipt and public URL in [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records). The number of platforms shown in the directory does not mean every automated publisher is connected; some routes may only save drafts.

After the content is public and reachable, choose an available channel in [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations), enter the article URL and real reader questions, and preserve raw answers, time, and source citations. Manually retest the same questions later. Successful submission, search indexing, and AI citation are separate states.

**Copyable task**

```text
Use geo-article-production to create an article for [product/project/topic] and [audience]. First-party sources: [links/materials]; target platform/account: [platform/account]; authorized assets: [list]; length/field limits: [current page or unknown]. Produce a sourced main article, separate platform versions, cover/illustrations, and QA. Save the article in aimeGeo and reopen it to verify. If the original task authorizes end-to-end publishing, use only a route currently listed as supported, then read the publish record and public URL; do not treat directory presence as proof of support or request per-step approval. Once public, create AI citation questions and schedule a later manual retest, preserving raw answers and cited sources.
```


**Official aimeGeo links:** [website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo). The public [getting-started guide](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) documents project materials, article saving, supported publishing paths, and citation retests after content becomes public.

## Self-check

```bash
python3 scripts/self-test.py
```
