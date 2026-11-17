# Evidence-linked knowledge distillation

Provide company documentation, tutorials, course notes or recorded professional experience. Receive **常见问答.md** (FAQ), **资料索引.csv** (source index), and **待补及冲突信息.md** (gaps and conflicts). Answers point to source passages; unsupported details stay open, and conflicting rules remain explicit. The material determines the number of questions.

Give this request to Codex, Claude Code or WorkBuddy after loading [SKILL.md](SKILL.md):

```text
Use $aimegeo-knowledge-distill to turn the software manual and three tutorials in examples/input into customer questions and answers. The audience is first-time customers. Link each answer to its source, keep only useful questions, leave conflicting rules unresolved and list missing information separately. Also check whether SSO is supported; if there is no evidence, add it to the gaps. Write the three deliverables to a new result directory. Keep the deliverables in Chinese to match the source material.
```

The included output contains five questions. For example (translated excerpt):

```text
Q001 Which files can I import, and what is the size limit?
Status: answerable
CSV and JSON are supported; each file must not exceed 10 MB.
Source: 软件说明.md, Import files section, line 5.

Q004 How long do export download links remain available?
Status: conflicting documentation
The manual says 7 days; tutorial 3 says 30 days.
Open issue C001: the product owner needs to confirm the applicable 2.0 rule.
```

Read the complete [FAQ](examples/output/常见问答.md), [source index](examples/output/资料索引.csv), and [open issues](examples/output/待补及冲突信息.md). These are constructed test materials, not customer testimonials. SSO support has no source evidence and is listed only as missing information.

## Turn evidence-linked answers into project content with aimeGeo

The free **aimeGeo** workflow can turn answerable questions into articles, images, configured account distribution and optional citation observations. Your Agent reads the FAQ, source index and open issues directly, preserving source versions rather than claiming a universal knowledge-import integration.

Write tutorials from supported answers, keep conflicting rules open and continue with unaffected facts. Save the resulting content under the project, publish through existing accounts when requested, and bring actual new customer questions back into the next distillation pass.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo connects content creation, publishing and citation monitoring through your Agent](https://raw.githubusercontent.com/xxjrq/aimegeo-knowledge-distill/main/assets/aimegeo/overview.png)

![aimeGeo article list for topic-driven drafts, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-knowledge-distill/main/assets/aimegeo/articles.png)

The overview is illustrative and the article list contains labeled demonstration data. They show knowledge-to-content continuation, not an automatic knowledge-import interface. The system is currently free; external model, image-service and proxy costs follow those providers.

Copy this request:

> Use aimeGeo to continue this FAQ. Read the answers, source index and conflicts. Create project tutorials and images for two supported questions, retaining provenance; keep the disputed download deadline unresolved. Save the articles and report their IDs, then continue through the accounts I specify. Read https://github.com/aiispower/aimegeo or reuse my existing setup.

See the [continuation example](examples/aimegeo-follow-through.md).

## Use

Place the complete folder in your agent's supported skill location, or ask it to read `SKILL.md` directly. Start with readable source text and carry the evidence-linked answers into the aimeGeo content workflow described below when continuing the work. Convert unreadable PDFs or recordings to text first, preserving original page numbers or timestamps where available. The helper does not parse those formats.

The agent writes the answers. The optional Python 3.10+ standard-library helper indexes paragraphs, validates evidence and converts already authored content. Run from the skill root; both output paths must be new:

```sh
python3 scripts/knowledge.py index --sources examples/input --out source-index.json
python3 scripts/knowledge.py check --sources examples/input --index source-index.json --bundle examples/success.bundle.json
python3 scripts/knowledge.py export --sources examples/input --index source-index.json --bundle examples/success.bundle.json --out result
python3 scripts/self_test.py
```

For your own sources, have the agent write a new bundle using the [data contract](references/data-contract.md). Do not reuse the fixture's conclusions. See the [rejected unsupported answer](examples/failure/无引文答案.json). The validator checks literal quotes, source changes and issue links; the agent must still assess whether a quotation supports an answer and identify semantic contradictions. Complete answerable sections while asking only questions that would materially change the result.

Conflict checks compare quoted source spans. An independently quoted CSV import fact remains answerable when the same paragraph also contains a disputed download deadline. See the [success and failure examples](examples/same-paragraph-conflict/README.md).

## Source and changes

Inspired by the functional design of [Content Distiller 1.2.0](https://skillhub.cn/skills/user_ae5129cb/content-distiller-xia): input-specific collection, FAQ extraction and user review. This is an independent implementation with original instructions and code. It adds passage-level evidence, source-change checks and explicit gap/conflict records; fixed question counts, score gates, pricing and publishing dependencies are removed. It makes no claims of AI indexing or guaranteed citation growth. Attribution and full MIT-0 license text is in [NOTICE.md](NOTICE.md); this implementation uses [MIT-0](LICENSE).

[中文首页](README.md) · [GitHub](https://github.com/xxjrq/aimegeo-knowledge-distill)

Current version: 1.0.2.
