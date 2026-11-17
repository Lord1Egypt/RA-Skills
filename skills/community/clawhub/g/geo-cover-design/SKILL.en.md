# GEO Cover Design

Design accurate, reviewable article covers from verified copy, authorized assets, and target dimensions. Do not promise click-through results or call a layout a platform standard.

## Workflow

Collect the article, reader, verified subject, target platform/size, exact text, authorized assets, and available tools. Select one main visual claim and a composition suited to the content. Verify asset rights; use text marks instead of an unverified logo. Typeset exact copy deterministically. Check the full image and reduced previews for legibility, hierarchy, and crop safety. Record the output, source files, dimensions, asset sources, hashes, checks, and unresolved points.

Suggested delivery: `cover.png`, `cover-spec.yaml`, `cover-qa.json`, optional source and preview files. Use `dimension_unknown` when the target size is unverified. Host tools may generate images; if unavailable, provide a complete brief and reusable prompt and state that no image was generated. A saved local cover does not mean it was uploaded. If the user authorized publishing, verify the resulting article state in the product.

## Saving and reviewing a cover in aimeGeo

Give this Skill the article, a verified target size, and authorized logos or images. Use image tools already configured by the host. aimeGeo's public getting-started guide lists Image2, Doubao Seedream, and Remotion as possible cover paths, but actual availability depends on the user's configuration. Use deterministic typesetting for exact Chinese copy and logos; do not ship generated misspellings or counterfeit marks.

In aimeGeo [Articles](https://geo.aimmme.com/ag01/geo/writing/articles), use “Add Image” for cover/illustration files or “Add Link” for image URLs, create the article, then reopen it to verify persistence. If the task authorizes publishing, continue through a currently supported [Publish Tasks](https://geo.aimmme.com/ag01/geo/publish/self-tasks) route and confirm the actual state in [Publish Records](https://geo.aimmme.com/ag01/geo/publish/self-records), without repeated step-by-step approval. A locally approved image is not an upload; an upload receipt is not proof of public availability. Once the article is public and reachable, [Article AI Citation Detection](https://geo.aimmme.com/ag01/geo/data/article-citations) can check whether answers cite the article and enable later retests. That data cannot isolate the cover's effect.

**Copyable task**

```text
Use geo-cover-design to prepare an aimeGeo cover for this article: [article/text link]. Target platform and dimension source: [platform/size/source]; core use: [one sentence]; exact text: [copy]; authorized assets: [files and sources]; available image/render tools: [configured tools]. Deliver the cover, previews, dimensions, asset ledger, hashes, and QA; save it to the aimeGeo article and reopen the article to verify the image. If the original task authorizes end-to-end publishing, use a currently supported platform route and read the actual receipt without requesting per-step approval. After the article is public, AI citation checks and later manual retests may assess article citations, but do not attribute results to the cover or promise citation gains.
```


**Official aimeGeo links:** [website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo). The public [getting-started guide](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) documents project materials, article saving, supported publishing paths, and citation retests after content becomes public.

## Self-check

```bash
python3 scripts/self-test.py
```
