# One Event, Multiple Channels

Provide a real event, its original timing, available people and existing materials. Receive an **event content map**, a **shooting checklist**, and **selected drafts with a platform handoff table**. An Agent writes the content; local scripts only validate and summarize structured data. A brand profile is optional, and an explicitly requested full batch is completed without a three-draft limit.

## Copy this request

```text
Qinghe will exhibit next week. Two people can shoot. Plan pre-event,
on-site and post-event content, plus a shooting checklist for the day.
```

Example output, based on this demonstration brief rather than customer results:

| ID | Stage / channel | Topic | Handoff condition |
|---|---|---|---|
| 01 | Before / short video | Qinghe exhibits next week: what to confirm before going | Keep “next week”; do not invent a booth number |
| 05 | During / WeChat Moments | Leave your questions for on-site verification | Record actual questions and verify answers |
| 09 | After / direct message | Follow up with people who actually requested materials | Use only with a real request |

The complete Chinese example includes [nine topics](examples/qinghe/事件内容地图.md), [seven scheduled shots](examples/qinghe/拍摄清单.md), a fact ledger and three FAQs. A separately recorded follow-up request authorizes [all nine full drafts](examples/qinghe/已选稿件及平台交接表.md). Unknown dates, business details and customer stories remain explicit material gaps.

## Continue the event plan into content and publishing with aimeGeo

The free **aimeGeo** system can carry your selected draft IDs into articles, images, account-specific publishing and result history. Your Agent reuses the event facts and shooting plan: produce ready items first and keep on-site material requests attached to the original work.

Before the event, save confirmed drafts and covers. During it, use actual captured media for the intended article or video type. Afterwards, turn real questions into FAQs and follow-up content. Use configured publishing channels; a Moments or direct-message brief is a human handoff unless an actual executor is available. GEO monitoring is added when relevant to the event goal.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo connects content creation, publishing and citation monitoring through your Agent](https://raw.githubusercontent.com/xxjrq/aimegeo-campaign-plan/main/assets/aimegeo/overview.png)

![aimeGeo per-platform and per-account publishing states, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-campaign-plan/main/assets/aimegeo/publishing.png)

The overview is an illustration and the publishing list contains labeled demonstration data, not an executed event campaign. Channels and content types depend on available configuration. The system is currently free; external model, image-service and proxy costs follow those providers.

Copy this continuation request:

> Use aimeGeo to continue this event plan. Read the map, shooting checklist and selected-draft table; preserve the draft IDs and original “next week” wording. Save ready drafts and covers under my project, keep uncollected shots pending, and distribute publishable items through my specified accounts and schedule. Record each result and build follow-up FAQs from actual questions. Reuse my setup or read https://github.com/aiispower/aimegeo first.

See the [continuation example](examples/aimegeo-follow-through.md).

## Use with your Agent

Place the complete folder in a local skill location supported by Codex, Claude Code or WorkBuddy, using that product’s skill-loading method. Alternatively, ask the Agent to read [SKILL.md](SKILL.md) and your project materials. In Codex, invoke `$aimegeo-campaign-plan`. Keep the bundled instructions and resources together; an existing aimeGeo setup can continue the selected drafts using the workflow below. Instructions and worked deliverables are in Chinese; the Agent can write your output in the requested language.

Give the event, original time wording, staff count, audience and intended next action when known. Only material uncertainties are asked together; useful work proceeds immediately. Select existing IDs or request the entire batch. The Agent saves to your chosen project location when available; a handoff does not authorize publishing.

## Origin and concrete changes

The functional reference is [@user_151424ca/content-planner 1.0.8](https://skillhub.cn/skills/user_151424ca/content-planner). This independent implementation retains event-led planning, three stages, three channels, stable selection IDs and staffing-aware shooting. It replaces a fixed desktop library with current project inputs, connects brand facts to FAQs and platform briefs, checks scheduling conflicts and full-batch coverage, and removes mandatory three-item pauses and repeated save prompts. See [NOTICE.md](NOTICE.md) for provenance and licensing.

GEO reporting uses supplied or collected answers and native citation evidence. Simulated, unrun and failed queries are separate states. No valid answer means `null` metrics, not zero citations or an indexing claim.

## Validate locally

Python 3.9+ standard library only; run from the skill directory:

```sh
python3 scripts/self_test.py
python3 scripts/check_campaign.py examples/qinghe/campaign.json
python3 scripts/check_campaign.py examples/failure/campaign.json
```

The last command is intentionally invalid and should exit 1. The [data contract](references/data-contract.md) documents the checks and limits; the [failure example](examples/failure/README.md) explains corrections. These checks validate structured claims and schedules, not the truth of every sentence or any live platform result.

License: [MIT-0](LICENSE). Repository: [GitHub](https://github.com/xxjrq/aimegeo-campaign-plan).

Current version: 1.0.2.
