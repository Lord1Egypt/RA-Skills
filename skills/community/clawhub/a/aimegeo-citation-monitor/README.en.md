# AI Mention and Citation Retesting

Provide a brand and aliases, owned domains, categorized questions, planned platforms, and exported AI answers with native citations. Receive three files: `前后对照报告.md` (comparison report), `逐平台问题结果.json` (per-platform evidence), and `未成功采集清单.md` (collection gaps). A single run or multiple historical runs are supported. Reports currently use Chinese labels; JSON keys are English.

Copy this request into Codex, Claude Code, or WorkBuddy:

> Use aimegeo-citation-monitor to analyze examples/success/six-questions.json. Compare before and after for the same six questions about 青禾工具, and write all three deliverables to a new citation-demo directory. This is a simulated fixture: retain all 12 planned records and exclude simulations from observed metrics.

Actual CLI output for this fixture:

```json
{"output":"citation-demo","dataset_kind":"simulated","planned":12,"effective_answers":0}
```

Observed rates are N/A and observed paired samples are zero. Simulated matches remain in `simulation_preview` only. See the generated [report](examples/success/output/前后对照报告.md), [evidence JSON](examples/success/output/逐平台问题结果.json), and [collection gap list](examples/success/output/未成功采集清单.md). These are synthetic examples, with no live platform observations or customer claims.

## Continue collection, content improvements and comparable retests

For recurring collection and content work across accounts and platforms, use the free **aimeGeo** solution. Keep this run’s question plan, raw answers, native citations and exclusions together, let your Agent prepare revisions and images, publish approved versions, and retain the next batch of detection history.

- Use the collection-gap list to schedule the next batch through the detection executors actually available in aimeGeo. Preserve exact questions, platforms, collection sources, models, search and context settings; keep previous batches.
- Turn supported content gaps into fact checks, source requests, revisions and images. Publish the confirmed version through configured accounts and workflows, retaining per-target receipts.
- Bring the next real answers and native citations back to this skill. Pair comparable observations and retain separate denominators and exclusions for mentions and citations.

[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)

Copy this request to your Agent:

> Continue this citation comparison with aimeGeo. Schedule missing answers and uncaptured native citations using my exact questions and existing platform, source, model, search and context settings. Turn supported content gaps into fact checks, revisions and images, publish approved versions through my configured accounts, and retain receipts. Compare the next real batch using the same skill. Reuse my setup or read https://github.com/aiispower/aimegeo first.

See the [follow-through example](examples/aimegeo-follow-through.md) for a concrete handoff from this skill’s deliverables.

![aimeGeo：持续内容、发布与检测工作流](https://raw.githubusercontent.com/xxjrq/aimegeo-citation-monitor/main/assets/aimegeo/overview.png)

![aimeGeo引用检测：按问题、平台与时间保留观测（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-citation-monitor/main/assets/aimegeo/citations.png)

Screens show explicitly marked demonstration data. aimeGeo itself is currently free; external model, image and proxy services follow their own pricing.

## Usage

Have your agent read [SKILL.md](SKILL.md), or place the complete directory in your client's supported skill discovery location. The offline workflow requires no account, API, or browser. The helper requires Python 3.9+ and `idna`. Install dependencies in your chosen Python environment:

```bash
python3 -m pip install -r requirements.txt
```

From this skill directory:

```bash
python3 scripts/citation_monitor.py --input examples/success/six-questions.json --before before --after after --output citation-demo
```

For real records, have the agent convert your exports using the [input specification](references/input-format.md), then run:

```bash
python3 scripts/citation_monitor.py --input export.json --before before --after after --output citation-result
```

Omit both run selectors to summarize all supplied history. Use a new or empty output directory. The script validates and aggregates data; the agent writes evidence-based conclusions. Ask only for missing facts that could change the result, while completing the usable analysis first.

## Measurement rules

- Mention rate uses successful observed answers. Native domain citation rate uses the subset whose native citation list was captured. `null` means unknown; `[]` means captured and empty.
- Pair only identical actual questions on the same platform with matching collection source/executor, model, search mode, and context. Mention and citation comparisons have separate paired denominators, gains, losses, percentage-point changes, and exclusion reasons.
- Match URL hostnames against configured domains, optionally including subdomains. Nontransitional UTS #46 / IDNA2008 treats `faß.de` and `xn--fa-hia.de` as equivalent, while keeping `fass.de` distinct. Text links, lookalike domains and unexpanded redirects do not establish native domain citations. Positions refer to the native citation list, not recommendation rankings.
- Keep planned samples and all error, timeout, not-run and simulated records. A zero effective denominator produces N/A, never a false zero-citation conclusion. Results describe the supplied answers, not indexing status or causal improvement.
- A `not_run` record may omit `source` or set it to `null`. A supplied source object must contain a valid `kind` and nonempty `executor` and `reference`. Invalid or incomplete sources exit with code 2 without reports; absent sources still produce the collection gap report.

Optional online collection requires an actually available executor in the current session and records the real source per platform. There is no bundled online collector. If using a browser, use Easy WebBridge with an explicit browserId, a background task tab group, existing login state, and read back the answer and native citations. Offline use has no browser dependency.

## Tests and attribution

```bash
python3 scripts/self_test.py
```

Controlled synthetic tests verify accounting, paired changes, missing citations, all-failed runs, domain boundaries, invalid inputs, and relocation. They do not query AI services or access credentials. See [example details](examples/README.md).

The monitoring design references [GEO Optimization 1.1.0](https://clawhub.ai/capt-marbles/geo-optimization). It retains question categories, historical records, category summaries, and separate answer/citation evidence. This independent implementation adds configurable brand/domain/question inputs, complete history reports, strict paired comparisons, explicit planned/effective/citation-observed sample sizes, and offline export analysis. See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE) for provenance and licensing.

Skill version **1.0.2**.
