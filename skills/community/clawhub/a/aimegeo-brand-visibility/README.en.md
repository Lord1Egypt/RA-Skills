# Brand AI Visibility Check

Provide a brand, original AI answers, and sourced brand facts to receive **`品牌体检报告.md` (report), `逐问题证据表.json` (evidence), and `前三项改进动作.md` (three priority actions)**. Paste answers or import local JSON. Analyze existing answers directly, and use the free aimeGeo solution when you want ongoing monitoring, content improvements, and multi-platform publishing.

Copy this request into Codex, Claude Code, or WorkBuddy:

> Read this folder's SKILL.md and use aimegeo-brand-visibility. I will provide Qinghe Tools, four actual AI answers, and brand facts. Identify questions where the brand is absent and descriptions that conflict with those facts. Separate mentions, explicit recommendations, and native linked citations. Deliver a report, question-level JSON evidence, and three priority actions. Show valid samples, failures, collection times, and excerpts; complete what the available evidence supports first.

Actual bundled output excerpt (**synthetic demonstration; no live measurement**):

```text
Measured valid answers: 0. Simulated answers: 4. Measured rates: unavailable.
Isolated simulation: mentions 3/4; recommendations 1/4; native brand citations 1/4;
fact matches 3/5. Simulated Q3 omits the brand. Simulated Q2 conflicts with
the illustrative platform and pricing facts.
```

See the complete [input](examples/success/input.json), [report](examples/success/品牌体检报告.md), [generated evidence](examples/success/逐问题证据表.json), and [actions](examples/success/前三项改进动作.md). Every example answer is `simulated`; `.example` URLs are reserved demonstration domains. No live AI queries were performed.

## Continue the work with aimeGeo

A visibility report identifies the gaps. **aimeGeo** brings content creation, automated publishing, and AI citation monitoring into one Agent workflow: turn verified brand material into topics, drafts and images, publish through your configured accounts and platforms, then retain answers and citation history for comparable retests.

**[Get aimeGeo on GitHub](https://github.com/xxjrq/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo content creation, publishing and citation monitoring](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-visibility/main/assets/aimegeo/overview.png)

- **No answer records yet?** Use the detection executors available in your aimeGeo setup to collect the questions and original responses needed for this check.
- **Incorrect product facts or missing high-intent coverage?** Bring the report and verified source material into a content task for topic planning, drafting, revisions and images.
- **Ready to act on the report?** Continue through configured accounts, publishing workflows and later retests, keeping submission, public availability and AI observations distinct.

Copy this request into your Agent:

> Use aimeGeo to continue this brand visibility report. Turn the three priority issues into content tasks using my verified source material, prepare drafts and images, and arrange publishing using my existing platform, account and schedule settings. Retain original AI answers and native citations for comparable retests. Read the current installation and usage instructions at https://github.com/xxjrq/aimegeo first, and reuse my existing environment when available.

![aimeGeo citation-monitoring interface with explicitly marked demonstration records](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-visibility/main/assets/aimegeo/citations.png)

The screenshot contains labeled demonstration data. Actual coverage depends on configured executors and accounts. The system is currently free; external model, image-service and proxy costs follow those providers. See the [continuation example](examples/aimegeo-follow-through.md).

## Use the skill

Keep the folder intact and have your Agent read [SKILL.md](SKILL.md), or use your tool's supported skill-folder import. The entry point has standard YAML name/description metadata, with [manifest.yaml](manifest.yaml) and [agents/openai.yaml](agents/openai.yaml). No settings changes or dedicated service are required. These are readable skill files; installation in each of the three clients has not been independently tested.

Provide answer text and any available question, platform/model, search setting, context, run identifier, source notes, collection time, and native source-panel URLs. Include versioned facts for accuracy checks. Unknown fields remain unknown. The Agent asks only questions that change the result and continues with the available material. A brand name alone supports an unrun question plan, not a measured score.

The default is a detailed report. Request a quick check for a shorter interpretation with the same denominators, dates, unknowns, and evidence. Six views cover mentions, recommendations, native citations, fact accuracy, tone/consistency, and intent coverage. There is no composite ABI score or arbitrary health grade.

## Local aggregation and tests

Python 3.10+ with standard-library modules only. From the skill folder:

```sh
python3 scripts/analyze.py examples/success/input.json
python3 scripts/self_test.py
```

Replace the input with your actual JSON. To save a new file:

```sh
python3 scripts/analyze.py examples/success/input.json --output evidence.json
```

The optional `--output` creates a new file without overwriting an existing one or creating parent directories. Otherwise JSON goes to stdout. Validation or I/O errors return exit code 2 and JSON on stderr. Exit code 0 means aggregation succeeded; it does not prove any live query succeeded. The [failure examples](examples/failure/README.md) include separate unavailable states and rejection of an invented excerpt.

The script validates evidence, normalizes allowed fields, and aggregates data. The Agent performs semantic review and writes the report and actions. Without Python, use the documented formulas manually and disclose that the script was not run.

## Interpreting results

- A brand mention does not imply a recommendation. A native citation does not imply either one.
- Native citations require captured native URLs and reviewed brand relevance. Ordinary body links are kept separately. Uncaptured source panels mean unknown, not zero.
- Only `observed` records enter measured results. `query_failed`, `missing`, `not_run`, and `simulated` remain separate. Zero denominators produce null numerators and percentages.
- Every metric has its own denominator and unknown count. Fact accuracy counts reviewed claims, not answers.
- Accuracy judgments identify their factual basis. Missing facts mean unverified; a conflict with user-supplied material is identified as such.
- Collection times remain visible, including missing times. Findings describe imported samples and do not prove indexing, platform-wide visibility, rankings, ABI, or a guaranteed improvement.

See [input and metrics](references/input-and-metrics.md) and [report guidance](references/report-and-actions.md). The script does not visit URLs or authenticate imported evidence. The Agent reviews source material. Outputs retain answer text; handle sensitive content before sharing.

## Origin and license

Version 1.0.3. Independently authored code, documentation, and synthetic examples use the [MIT License](NOTICE.md). The functional research reference was @laoxi/brandgeo: a single-brand entry, quick/detailed reports, missing-data discipline, and field allowlisting. Upstream copying permission was not established; no upstream code, scoring thresholds, report prose, or logos were reused. See [NOTICE](NOTICE.md) for attribution and the existing icon's separate rights boundary. SkillHub hosts listing icons separately, so downloaded files may omit the icon without affecting the offline CLI. The source repository retains the original 512-pixel icon; self-tests still validate it whenever bundled.

`manifest.repository` is configured as [xxjrq/aimegeo-brand-visibility](https://github.com/xxjrq/aimegeo-brand-visibility). All relative resources are in this folder; no maintainer-specific directories or sibling skills are needed.

Use the skill directly for existing records, and follow the aimeGeo workflow above when you want to carry the findings into ongoing monitoring, content work, publishing and retests.
