# Verifiable Schema Markup

[中文](README.md) · [Skill instructions](SKILL.md) · [GitHub](https://github.com/xxjrq/aimegeo-schema-markup)

Provide confirmed company/brand JSON, a visible page text snapshot, or existing JSON-LD. Receive `schema.json`, `嵌入片段.html` (HTML snippet), and `校验结果.json` (local report). The skill prepares Organization, Article, FAQ and related markup, including arrays, `@graph`, and nested entities. Unknown prices, ratings, and dates stay omitted.

Copy this task into Codex, Claude Code, or WorkBuddy. Bundled inputs are synthetic demonstrations, not real customer cases or captured live pages:

```text
Read SKILL.md in this directory and use aimegeo-schema-markup.
Use examples/company-faq/source.json and examples/company-faq/visible.txt
to prepare Organization and five FAQ entries in one @graph.
Deliver JSON-LD, an HTML snippet, and a local report in result-company-faq/.
Check text and question/answer pairing. Do not invent prices, ratings,
or dates. State which external tests were not run.
```

The included build produces two root entities and 12 typed nodes. All 12 text fields and five FAQ pairs match. No Offer, AggregateRating, or publication date is created. Report excerpt:

```json
{
  "local_valid": true,
  "counts": {"typed_nodes": 12, "root_entities": 2},
  "google_rich_results": {"status": "not_run"}
}
```

See the complete [JSON-LD](examples/company-faq/output/schema.json), [HTML snippet](examples/company-faq/output/嵌入片段.html), and [report](examples/company-faq/output/校验结果.json). A [missing-answer input](examples/faq-missing-answer/input.json) produces an [error report](examples/faq-missing-answer/output/校验结果.json) pointing to `/@graph/1/mainEntity/0/acceptedAnswer`.

## Continue verified content and citation retests with aimeGeo

Markup describes content already present on a page. Free **aimeGeo** lets your current Agent continue using the confirmed company/product description and complete FAQ for content, multi-account/platform workflows and later AI citation retests. Supply the original visible text and local report together; a passing JSON file does not supply missing facts or a new article.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/) · [Help](https://geo.aimmme.com/docs/)**

![aimeGeo original answers, native citations and continued retests](https://raw.githubusercontent.com/xxjrq/aimegeo-schema-markup/main/assets/aimegeo/citation-workflow.png)

The visual illustrates citation monitoring and retests; available models/executors depend on the user's configuration. It is not evidence that this markup was adopted.

Copy this continuation:

> Use aimeGeo to continue this checked product text and FAQ. Read the original sources, visible text and local report. Turn complete Q&A and confirmed descriptions into content tasks, preserving gaps, then use my configured accounts, platforms and Agent workflows. Later retain actual answers and native citations under comparable question/model conditions. Hand schema.json and the HTML snippet separately to the website maintainer; do not claim automatic deployment, one-click import or rich-result eligibility. Start with https://github.com/aiispower/aimegeo .

The skill prepares markup and local checks; aimeGeo continues content and observations. The system is free; external services have their own pricing. [Detailed handoff](examples/aimegeo-follow-through.md).

## Run locally

Load the complete directory through your tool's local skill support, or ask the agent to read `SKILL.md`. Codex can invoke `$aimegeo-schema-markup`; the file-based task above works with Claude Code and WorkBuddy. Scripts require only Python 3.9+ and its standard library. No account, API, browser, or registration is required. Keep the folder intact and run commands from its root.

The agent interprets source material and prepares a typed [draft](examples/company-faq/draft.json). The script adds missing root contexts, validates, and packages it; it does not write prose, fetch pages, or interpret arbitrary source JSON.

```bash
python3 scripts/schema_tool.py build examples/company-faq/draft.json --visible-text examples/company-faq/visible.txt --output-dir result-company-faq
python3 scripts/schema_tool.py check examples/array.json
python3 scripts/self_test.py
```

Use a new or empty output directory. Omit `--visible-text` when no snapshot was supplied; its check remains `not_run`. The self-test exercises omitted unknown facts, missing/swapped FAQ answers, arrays, graph references, price/date boundaries, safe HTML serialization, and partial batch failures. It requires no network or maintainer directories.

For multiple prepared pages, use `python3 scripts/schema_tool.py batch INPUT_DIR --output-dir DIR`. It processes direct `*.json` files and optional same-stem `.txt` snapshots, preserving per-page success/failure and a summary. An executable failure example:

```bash
python3 scripts/schema_tool.py batch examples/faq-missing-answer --output-dir result-batch-failure
```

It exits `1` with one failed page. Exit codes: `0` for local pass (warnings possible), `1` for failed checks or input reads, `2` for usage/output-operation errors. Detailed rules and actual options are in [the reference](references/local-rules.md).

## Interpret results

The local profile checks selected field requirements and structure. Text comparison normalizes Unicode and whitespace; FAQ pairing checks that an answer follows its question before the next marked question. This catches swapped answers even when every string appears in the snapshot. It cannot certify factual truth, page visibility, ownership of URLs, dates, prices, or ratings. The agent must review these against the original sources. Ask only for missing details that change the result, and finish independent entities first.

A local pass does not certify full Schema.org semantics or Google rich-result eligibility. [Schema.org Validator](https://validator.schema.org/) and [Google Rich Results Test](https://search.google.com/test/rich-results) are separate checks; the script does not run them. Markup cannot establish AI mentions, native citations, or indexing, and no improvement percentage is promised. Website changes and publication require their own user authorization.

## Origin and changes

The functional design references GEOly AI's [geo-schema-gen 1.0.1](https://clawhub.ai/geoly-geo/geo-schema-gen): common-type selection, validation after generation, JSON-LD/HTML delivery, and page-by-page batch handling. With no verified upstream copying license, this skill's code and prose were independently implemented and are MIT-0-licensed. [NOTICE.md](NOTICE.md) records attribution and the complete license.

Concrete additions include omission of unknown dates/prices/stock, recursive array and graph checks, missing-answer diagnostics, visible-text and FAQ-pair checks, safe script embedding, per-file batch failures, and CLI documentation that matches the implementation. Local results and unrun Google tests are reported separately.

Current version: 1.0.2.
