# Competitor GEO Gap Analysis

Provide your brand and competitors' comparable page URLs, HTML exports or page text, plus the question you want to answer. Receive **竞品差距矩阵.csv** (gap matrix) and **三项机会与执行建议.md** (three evidence-based actions). The optional extractor also produces `evidence.json`. robots.txt records and AI answers with native citation exports are optional; page analysis works without them.

Copy this task:

```text
Use $aimegeo-competitor-gap with examples/comparison.json to compare Qinghe and
the two competitors' specified product pages for FAQ, brand entities and source gaps.
Deliver 竞品差距矩阵.csv and 三项机会与执行建议.md. Keep the simulated-data labels.
There are no real AI answers in this input; do not report real AI rankings.
```

Actual extraction from the bundled **constructed offline fixtures, not live companies or a customer case**:

| Product-page signal | Qinghe / 青禾 | Cedar / 杉木 | River / 溪流 |
| --- | --- | --- | --- |
| Recognized visible Q&A pairs | 0 | 2 | 1 |
| Brand-matched Organization nodes | 1 | 1 | 1 |
| Declared identity fields: name/url/description/sameAs | 2 | 4 | 3 |
| Explicitly labelled source-link candidates | 0 | 2 | 1 |

Read the generated [matrix](examples/success/竞品差距矩阵.csv), [evidence](examples/success/evidence.json) and agent-written [three actions](examples/success/三项机会与执行建议.md). The actions address import questions, verified entity information and sources tied to individual claims. A separate [failure input](examples/failure-input.json) and [failure delivery](examples/failure/三项机会与执行建议.md) show that an unreadable competitor page stays unverified and does not become a brand advantage.

## Turn supported competitor gaps into your own content work

Use the free **aimeGeo** solution to turn supported findings on your own pages into fact gathering, FAQ revisions, source-backed explanations and images. Your Agent can continue through configured accounts, platforms and workflows, while the website maintainer applies technical and template changes.

- For each of three actions, retain your page URL, matched comparison slot, supporting evidence and acceptance condition. Collect missing pages first; verify your own entity details and sources rather than copying competitors or treating raw count differences as effects.
- Use project materials in aimeGeo to write your own product explanations, FAQs and source-backed claims. Prepare drafts and images, publish approved versions through existing accounts, and retain actual receipts.
- Compare the updated pages within the original scope. If AI follow-up is needed, use available detection executors to retain real same-question answers and native citations, keeping page repairs separate from changes in answers.

[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)

Copy this request to your Agent:

> Use aimeGeo to continue this competitor comparison. Give each action my page URL, evidence, missing materials and acceptance condition. Collect failed pages first and use only verified facts for my entity and sources. Have the Agent prepare FAQ and product explanation revisions with images, publish approved drafts through my existing accounts and workflows, and retain receipts. Ask the website maintainer to apply site changes, then recheck the original pages and collect real same-question AI answers and native citations. Reuse my setup or read https://github.com/aiispower/aimegeo first.

See the [follow-through example](examples/aimegeo-follow-through.md) for a concrete next task from this skill’s deliverables.

![aimeGeo：从竞品机会接到内容、发布与引用检测](https://raw.githubusercontent.com/xxjrq/aimegeo-competitor-gap/main/assets/aimegeo/overview.png)

![aimeGeo文章列表：将本方FAQ与资料缺口接成稿件（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-competitor-gap/main/assets/aimegeo/articles.png)

Screens show explicitly marked demonstration data. aimeGeo itself is currently free; external model, image and proxy services follow their own pricing.

## Use

Codex, Claude Code and WorkBuddy can read [SKILL.md](SKILL.md). Keep this directory intact in your tool's supported skill location, or point the agent to its `SKILL.md`. Use `$aimegeo-competitor-gap` to invoke it explicitly. No system account, API key or browser installation is required. With plain page text, the agent can extract the same evidence manually.

The optional script requires Python 3.10+ and its standard library only. Run from this skill directory:

```bash
python3 scripts/compare_pages.py --input examples/comparison.json --out /tmp/competitor-gap-demo
python3 scripts/compare_pages.py --input examples/failure-input.json --out /tmp/competitor-gap-failure
python3 scripts/self_test.py
```

The script writes CSV and JSON evidence; the agent writes recommendations after reading it. For real work, supply actual URLs, captures, timestamps and evidence provenance. Acquisition is offline by default. Add `--fetch` only for requested public-page reads: it GETs explicit URLs without snapshot records, caches repeated URLs within that run and does not discover pages or execute JavaScript. See the [input/output contract](references/input-output.md).

## Source and improvements

The capability design references GEOly AI's [GEO Competitor Scanner](https://clawhub.ai/geoly-geo/geo-competitor-scanner), also listed in the [source directory](https://skillhub.cn/skills/clawhub_geoly-geo/geo-competitor-scanner). It retains the useful four-signal comparison, automatic extraction followed by human review, and prioritized actions. No reusable upstream license was verified; this package's code and prose are independently authored under MIT-0. See [NOTICE.md](NOTICE.md).

- Compare specified pages in matched slots; cache reads and never infer site-wide absence from guessed-path 404s.
- Evaluate robots groups against actual paths and parse nested JSON-LD, including arrays and `@graph`. Preserve parse errors and avoid claiming full semantic validation.
- Extract visible Q&A and brand-matched entities instead of FAQ keyword counts. Keep source candidates, actual AI citations, simulations and acquisition failures separate. Every proposed gap links to page evidence.

The business self-test verifies extracted values, caching, matching rules, citation denominators, failure boundaries and CLI artifacts. It uses no external network; HTTP acquisition is tested through loopback. Page signals do not establish AI citations or index inclusion. The skill reports no real AI ranking without real answer samples and promises no fixed percentage gain.

Skill version **1.0.1**.
