# Brand GEO Knowledge Base

Provide product introductions, tutorials, FAQs, case studies, and an existing local knowledge base if available. Receive complete Markdown documents, preserved source files, `知识索引.json` (knowledge index), and `缺失与更新清单.md` (gaps and updates). Company, product, and topic records stay separate. Codex, Claude Code, and WorkBuddy can read `SKILL.md`, then use the resulting fact base for the aimeGeo content workflow below. The optional helper uses Python 3.10+ and the standard library only.

Copy this task:

> Use $aimegeo-brand-knowledge-base to organize the product introduction, tutorial, and FAQ in examples/materials into brand-kb. Write complete documents, distinguish company/product/topic, merge duplicate facts while preserving every source, and list missing pricing and case evidence without inventing awards.

The [complete generated example](examples/expected/知识库目录.md) includes:

```text
brand-kb/
  知识库目录.md
  公司/org-a/identity.md
  产品/product-a/product.md
  产品/product-a/faq.md
  主题/topic-handoff/howto.md
  主题/topic-handoff/faq.md
  原始资料/intro-v1.md
  原始资料/tutorial-v1.md
  原始资料/faq-v1.md
  知识索引.json
  缺失与更新清单.md
```

An actual result in the [product document](examples/expected/产品/product-a/product.md) states that the output contains local Markdown documents and a JSON index. It retains both the introduction excerpt and the FAQ excerpt, with their locators and applicable project. The explicitly labeled demonstration dataset contains 3 sources and 7 records, yielding 6 usable facts, 5 documents, and 2 gaps. It is not a real company or customer success story. No empty awards or case-study folders are created.

## Turn the fact base into ongoing content in aimeGeo

The free **aimeGeo** workflow connects usable knowledge to project articles, images, configured publishing accounts and optional observations. Your Agent reads the local documents and index, selecting current facts for the right entity and project rather than claiming a one-click import or universal API.

Create introductions, tutorials or FAQs that answer actual questions, retain provenance and save them under the project. When materials change, resolve conflicts and explicit replacements before updating affected articles or platform versions. Missing prices and customer evidence stay open.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo content workflow illustration for ongoing use of brand facts](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-knowledge-base/main/assets/aimegeo/overview.png)

![aimeGeo article-list demo for project tutorials and FAQs backed by materials](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-knowledge-base/main/assets/aimegeo/articles.png)

The overview is illustrative and the article list contains labeled demonstration data. They show the fact-to-article workflow, not an automatic knowledge import or customer outcome. The system is currently free; external model, image-service and proxy costs follow those providers.

Copy this request:

> Use aimeGeo to continue this brand knowledge base. Read its documents, index and gaps; use only current supported facts for this project and product. Create an introductory tutorial and FAQ with images, leaving historical, conflicting and unknown pricing claims out. Save them under my project, report their entries and continue through my existing accounts and schedule. Read https://github.com/aiispower/aimegeo or reuse my setup.

See the [continuation example](examples/aimegeo-follow-through.md).

## Use and reproduce

Ask Codex, Claude Code, or WorkBuddy to read this folder's `SKILL.md`, and provide the source and output locations. If your client offers a skill import feature, import the entire folder so its helper scripts and references remain available. No global configuration edits are necessary.

The agent reads the sources and writes actual fact bodies following the [data contract](references/data-contract.md). The script validates and renders that content; it does not write articles. Source paths are relative to the input JSON, and the output must be outside that input directory. Run from the skill directory:

```sh
python3 scripts/knowledge_base.py build --input examples/input.json --output brand-kb
```

The [JSON index](examples/expected/知识索引.json) records object identity, project scope, all original records, merged facts, evidence excerpts, and statuses. Use current `supported` facts after filtering the intended entity and project. Ask only questions that change attribution, scope, or conclusions; finish the independent work and list other gaps. An agent without Python can deliver the same Markdown/JSON structure directly and state that deterministic validation was not run.

## Updates and failure examples

Reimporting identical input is idempotent. An incremental import preserves omitted source files, records, and unmanaged handwritten files. Changed sources and changed facts require new IDs. Conflicting values for the same property in overlapping projects are retained and suspended from use. Dates alone never establish replacement.

```sh
python3 scripts/knowledge_base.py build --input examples/update.json --output brand-kb
python3 scripts/knowledge_base.py build --input examples/resolution.json --output brand-kb
```

The first command produces two conflicting facts. The second demonstrates an explicit replacement after the example owner has confirmed the applicable version; historical evidence remains. In a real task, verify that decision rather than assuming approval from the example.

When an old fact covers projects A and B but only A changes, import two new records together: A with the new value and B with the retained value. Each explicitly replaces the shared record. Successor scopes must stay within each target's scope and collectively cover every original project. Adding narrow facts without replacement can leave conflicts; replacing the shared record while omitting B is rejected.

```sh
python3 scripts/knowledge_base.py build --input examples/project-split-input.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-update.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-resolution.json --output split-kb
```

The intermediate update produces two conflicts. The [complete split](examples/project-split-resolution.json) produces these actual results:

| Fact | Projects | Value | Status |
| --- | --- | --- | --- |
| `a-current` | A | `Markdown+JSON+CSV` | `supported` |
| `b-current` | B | `Markdown+JSON` | `supported` |
| `shared-v1` | A, B | `Markdown+JSON` | `superseded` |
| `a-update` | A | `Markdown+JSON+CSV` | `superseded` |

Both original sources and all four records remain, with two usable facts, two historical facts, and zero conflicts. See the [data contract](references/data-contract.md#跨项目事实只更新一个项目) for the replacement relationships, a direct split, and a reproducible failure that omits the unchanged project.

```sh
python3 scripts/knowledge_base.py build --input examples/failure-unsupported.json --output rejected-kb
```

This [failure fixture](examples/failure-unsupported.json) claims a supported fact without evidence. It exits with code `2`, creates no knowledge base, and returns this [recorded error](examples/failure-output.json):

```json
{"status":"error","message":"有来源支持的事实必须提供可定位的来源摘录"}
```

The message means that a supported fact requires a locatable source excerpt. Invalid quotations, unknown identities or scopes, path escapes, replacement cycles, and edits to managed documents are also rejected. Preserve manual edits as new source material before reimporting. Excerpt matching does not establish semantic support or source credibility; the reading agent must verify those. Writes are atomic per file, not a database transaction; update each knowledge base sequentially.

```sh
python3 scripts/self_test.py
```

Offline business tests verify the full generated example, evidence retention, duplicate merging, scope separation, conflicts, replacement history, complete project splits, scope boundaries, and failure preservation. They need neither an icon nor a root license file, and make no external service calls.

## Reference and concrete improvements

The functional reference is [@user_1831d4fb/geo-kb-creator 1.0.1](https://skillhub.cn/skills/user_1831d4fb/geo-kb-creator). This implementation retains its useful organization around identity, products, trust evidence, user questions, and conversion information, along with existing-target identity checks.

Independently authored instructions and code add complete local content and indexes, per-fact provenance/status/project scope, evidence-preserving deduplication, safe incremental imports, conflict handling, explicit replacement, and categories based on actual materials. The current Agent can read the documents and index to continue into aimeGeo content work; automatic knowledge-base synchronization is not assumed. No copying license was verified for the reference package; its code, substantial text, and logos are not included. Original work is MIT-0 licensed; see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md), which also contains the complete MIT-0 license. Repository: [aimegeo-brand-knowledge-base](https://github.com/xxjrq/aimegeo-brand-knowledge-base).

This skill does not run GEO queries or promise indexing or percentage gains. If separate measurement evidence is provided, report only actual answers, mentions, and native citations; distinguish simulated, unrun, and failed queries rather than reporting them as zero citations.

Current version: 1.0.2.
