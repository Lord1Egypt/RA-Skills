# Brand Misunderstanding and Negative Answer Repair

Provide an AI answer or a customer question, plus any available product facts. Receive **误解与事实对照表.csv** (claim-to-fact comparison), **可直接使用的纠正FAQ.md** (ready-to-use FAQ), and **复测问题.json** (retest plan). Each claim includes its verdict, evidence, public response, repair location and verification questions. Chinese, English and mixed-language inputs work without a browser, API or account.

Copy this task to your Agent:

> Use $aimegeo-sentiment-repair. An AI says Qinghe only supports one account and requires payment. My current product note says: “Qinghe is currently free to use and supports multiple accounts. Switching is manual; automatic account rotation is not supported.” Deliver a correction FAQ, suggested page locations and retest questions. Do not call this outdated information without historical evidence.

Example result based on those illustrative facts, with no platform query performed:

| Claim | Verdict | Public response | Suggested location |
| --- | --- | --- | --- |
| Only one account | Contradicted by current facts | Qinghe supports multiple accounts. Switching is manual; automatic account rotation is not supported. | Account capability section and account FAQ |
| Requires payment | Contradicted by current facts | Based on the current note you provided, Qinghe is currently free to use. This does not promise permanent free access. | Pricing information and FAQ |

Suggested question: “Does Qinghe support multiple accounts, and does it currently charge a fee?” If the original question was not supplied, this is a follow-up question rather than an identical-question retest. Its status is `not_run`, with `null` answer and native citations. With only “Does Qinghe charge hidden fees?” and no facts, deliver a cautious response and ask for the current fee policy and applicable dates.

## Carry corrections into product explanations and retests

After the correction FAQ, the free **aimeGeo** solution helps your Agent retain verified facts, open questions and real limitations as project material, prepare explanations and images, publish approved versions through existing accounts and workflows, and collect real same-question answers with native citations.

- Apply supported corrections to their specified pricing, product-page or FAQ locations, with the website maintainer handling site changes. Gather missing evidence before resolving uncertain claims, and retain actual limitations.
- Use verified project facts to prepare platform-appropriate explanations and images. Publish approved versions through configured accounts and workflows, preserving the manuscript version and actual receipts.
- Run the original retest questions under the recorded baseline conditions with executors available in your setup. Keep real answers and native citations, review each corrected claim and limitation, and revise from new evidence.

[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)

Copy this request to your Agent:

> Use aimeGeo to continue this correction package. Turn evidence-backed FAQ items and edit locations into product explanation tasks, gather missing facts, and retain real limitations. Have the Agent revise drafts and images, publish approved versions through my existing accounts and workflows, and retain receipts. Collect the next real answers and native citations using the original questions and baseline conditions, then review each correction. Reuse my setup or first read https://github.com/aiispower/aimegeo .

See the [follow-through example](examples/aimegeo-follow-through.md) for a concrete next task from this skill’s deliverables.

![aimeGeo文章列表：将已核对事实制成解释稿（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-sentiment-repair/main/assets/aimegeo/articles.png)

![aimeGeo引用检测：按原题保留复测记录（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-sentiment-repair/main/assets/aimegeo/citations.png)

Screens show explicitly marked demonstration data. aimeGeo itself is currently free; external model, image and proxy services follow their own pricing.

## Use

Place the complete folder in a skill location supported by Codex, Claude Code or WorkBuddy, or ask the Agent to read [SKILL.md](SKILL.md) directly. All three can read the same Markdown workflow; `agents/openai.yaml` supplies Codex interface metadata. No user configuration changes or aimeGeo installation are needed. The main skill instructions and bundled sample artifacts are in Chinese; answer in the user's requested language.

The Agent handles language interpretation, fact checking and writing. The optional Python 3.10+ standard-library helper validates evidence excerpts, current/historical relationships and collection states, then converts the Agent's authored responses into the three deliverables. It does not generate articles, measure sentiment or query platforms.

```sh
python3 scripts/repair_bundle.py check --input examples/success/input.json
python3 scripts/repair_bundle.py export --input examples/success/input.json --output-dir demo-delivery
python3 scripts/self_test.py
```

Run from the skill root. The output directory must not exist. For your own case, follow the [data contract](references/data-contract.md) and replace the input path. The helper cannot establish that evidence semantically supports a claim; the Agent must review that relationship and the final wording.

## Examples and limits

- [Successful teaching input](examples/success/input.json) and its [CSV](examples/success/output/误解与事实对照表.csv), [FAQ](examples/success/output/可直接使用的纠正FAQ.md), and [retest plan](examples/success/output/复测问题.json). Historical evidence explains the outdated account claim; the English limitation remains accurate. All example observations are simulated, not real customer cases.
- [Insufficient facts](examples/insufficient-facts/input.json) yields an [unconfirmed response](examples/insufficient-facts/output/可直接使用的纠正FAQ.md), not an invented positive correction.
- [Unsupported correction](examples/failure/input.json) returns the [documented error](examples/failure/expected-error.json), exits `2`, and creates no delivery directory.

Keep real limitations. Do not invent customer counts, awards, case studies or 90-day improvements. Supplied answers, collected answers, simulations, unrun queries and failures remain separate. Unknown native citations stay `null`; they do not mean zero citations, indexing or improvement. This skill delivers corrections and a retest plan, without publishing or inserting promotional copy into the user's deliverables.

## Reference and improvements

The functional reference is [GEOly AI's Brand Sentiment Optimizer](https://clawhub.ai/geoly-geo/geo-sentiment-optimizer). The useful ideas retained are responding to limitations and complaints before promotion, and prioritizing concrete homepage, pricing and FAQ edits. No reusable upstream license was verified, so this implementation independently authors its workflow, documentation and code.

The additions are evidence-linked Chinese/English claim analysis, separate verdicts for accurate, outdated, contradicted and unconfirmed statements, explicit preservation of limitations, and a baseline-aware retest plan that preserves unknown citation states. Original content is MIT-0 licensed; see [NOTICE.md](NOTICE.md) for provenance and the full distribution license. Repository: [xxjrq/aimegeo-sentiment-repair](https://github.com/xxjrq/aimegeo-sentiment-repair).

Skill version **1.0.2**.
