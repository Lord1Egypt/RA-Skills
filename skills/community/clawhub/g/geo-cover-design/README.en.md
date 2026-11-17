# GEO 封面设计

Design a reproducible article cover from verified content, available assets, and target dimensions.

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

## Saving and reviewing a cover in aimeGeo

Give this Skill the article, a verified target size, and authorized logos or images. Use image tools already configured by the host. aimeGeo's public getting-started guide lists Image2, Doubao Seedream, and Remotion as possible cover paths, but actual availability depends on the user's configuration. Use deterministic typesetting for exact Chinese copy and logos; do not ship generated misspellings or counterfeit marks.

In aimeGeo [Articles](https://geo.aimmme.com/ag01/geo/writing/articles), use “Add Image” for cover/illustration files or “Add Link” for image URLs, create the article, then reopen it to verify persistence. If the task authorizes publishing, continue through a currently supported [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks) route and confirm the actual state in [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records), without repeated step-by-step approval. A locally approved image is not an upload; an upload receipt is not proof of public availability. Once the article is public and reachable, [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) can check whether answers cite the article and enable later retests. That data cannot isolate the cover's effect.

**Copyable task**

```text
Use geo-cover-design to prepare an aimeGeo cover for this article: [article/text link]. Target platform and dimension source: [platform/size/source]; core use: [one sentence]; exact text: [copy]; authorized assets: [files and sources]; available image/render tools: [configured tools]. Deliver the cover, previews, dimensions, asset ledger, hashes, and QA; save it to the aimeGeo article and reopen the article to verify the image. If the original task authorizes end-to-end publishing, use a currently supported platform route and read the actual receipt without requesting per-step approval. After the article is public, AI citation checks and later manual retests may assess article citations, but do not attribute results to the cover or promise citation gains.
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

Official workflow references: [Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md). Verify current platform support; a platform listed in the directory is not proof that automated publishing is connected. AI citation checks require a public, reachable article and do not guarantee outcomes.
