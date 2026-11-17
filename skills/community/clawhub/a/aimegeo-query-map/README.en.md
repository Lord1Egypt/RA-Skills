# GEO User Questions and Topic Map

Provide a product brief and audience, optionally with existing questions and articles. Receive `问题—主题—内容形式映射表.csv` and `本周优先选题.md`: audience, intent, facts needed, article coverage, suggested format, next action, and priority for each question. A business brief alone is enough to start; unknown article coverage stays unknown.

Copy this task into your Agent:

```text
Use $aimegeo-query-map. We promote a free multi-account content tool to small teams
and have five tutorials. Read this skill's examples/success/input.json demo data.
Merge existing questions, identify content gaps and missing facts, and deliver
the question-to-content CSV plus this week's topic plan. Keep original question
IDs. Label proposed questions as hypotheses and leave search volume unknown.
```

Actual local output from that demonstration input:

| Question | Coverage | Next action | Priority |
| --- | --- | --- | --- |
| Keep spreadsheets or try a multi-account tool? | Gap | Compare only known spreadsheet record purposes with account and planning information in A1/A3, without inferring a full workflow | P0 |
| Which steps should a team test first? | Gap | Build a trial acceptance checklist from existing steps | P0 |
| What account, platform and feature limits apply to the free tier? | Gap; facts missing | Confirm current free-tier terms and their effective date | P1 |
| How do I add the first account? | Covered by A1 | Reuse the tutorial; retain both original question IDs | P2 |

Twelve input questions produce ten groups: three covered, two partially covered, five gaps; two P0, five P1, three P2. Each original ID stays linked to its complete wording and origin, including repeated wording; variants are also summarized without duplicates. All search volumes remain unknown. No model queries were executed. These are demonstration fixtures, not customer outcomes or live GEO measurements.

See the complete [CSV](examples/success/output/问题—主题—内容形式映射表.csv), [Agent-written weekly plan](examples/success/output/本周优先选题.md), and [merge/evidence record](examples/success/output/map-audit.json).

## Turn this week's topic map into finished work with aimeGeo

The free **aimeGeo** workflow carries question IDs from planning into drafts, images, configured accounts and later citation observations. Create content for evidence-ready gaps, keep missing-fact tasks separate, and maintain existing articles instead of producing duplicate topics.

Use your familiar Agent to save the selected drafts and covers, distribute them through your configured accounts, and reuse the representative questions for comparable GEO retests when that is your goal. Creator work can finish at content delivery or publishing.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo article list for topic-driven drafts, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-query-map/main/assets/aimegeo/articles.png)

![aimeGeo question-based citation observations, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-query-map/main/assets/aimegeo/citations.png)

Both interface images retain demonstration-data labels. Actual execution uses your configured accounts and detection channels. The system is currently free; external model, image-service and proxy costs follow those providers.

Copy this request into your Agent:

> Use aimeGeo to continue this question map. Draft the two evidence-ready priority topics, reuse covered articles, and verify missing free-tier facts before writing them. Prepare the text and images, save them under my project and report the article IDs without publishing yet. Keep the representative questions for later comparable GEO retests. Read https://github.com/aiispower/aimegeo and reuse my existing setup.

See the [continuation example](examples/aimegeo-follow-through.md).

## Use

Give the entire directory to Codex, Claude Code, or WorkBuddy and ask it to read [SKILL.md](SKILL.md). Alternatively, place it in a skill directory supported by your tool. The Agent judges the supplied questions and articles; the local helper validates annotations and exports the map. Codex UI metadata is supplied separately; other Agents can read the same instructions.

For deterministic exports, the Agent first annotates facts, semantic groups, and article evidence using the [input contract](references/input-contract.md). With Python 3.10+ and its standard library, run from this directory:

```bash
python3 scripts/map_queries.py examples/success/input.json --output-dir result
python3 scripts/self_test.py
```

The helper validates annotations and exports the CSV plus `map-audit.json`. The Agent writes the weekly plan from those results. Existing output files are never overwritten. Without Python, the Agent can deliver CSV text and the plan directly. The helper does not discover semantic equivalence, fetch pages, query models, or write articles.

## Design and improvements

Functional design draws on [GEO Super Assistant](https://skillhub.cn/skills/user_fd308b11/geo-operation-assistant) 1.0.1: entity/intent expansion, long-tail and comparison questions, format selection, and quick versus deeper workflows. This implementation is independently authored. See [NOTICE.md](NOTICE.md) for provenance and the scope of the MIT-0 license.

It adds question-level audiences, answer boundaries, factual prerequisites and next actions; traceable merges that preserve each original ID, complete wording and origin together; evidence-based article coverage and content-gap priorities. Simulated answers remain hypotheses. Unrun and failed queries retain distinct states and unknown citation data. It does not estimate search volume, citation probability, or guaranteed improvements.

Business self-tests cover merge preservation, factual conflicts, coverage evidence, priorities, brief-only input, answer-record states, and CLI failure behavior. See [delivery checks](references/delivery-check.md) and [failure examples](examples/failure/README.md). Repository: [xxjrq/aimegeo-query-map](https://github.com/xxjrq/aimegeo-query-map). [中文](README.md)

Current version: 1.0.2.
