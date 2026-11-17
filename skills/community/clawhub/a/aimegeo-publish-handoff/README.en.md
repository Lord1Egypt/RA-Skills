# Multi-account publishing handoff and receipts

Provide a finished UTF-8 article, assets, target platforms and stable account IDs, current authorization, and any existing receipts. Receive `发布交接包.json`, a verbatim manuscript and metadata for each account, `平台稿件及素材清单.md` (manuscript and asset inventory), and `回执状态表.md` (receipt status table). Pending review and uncertain submissions require readback before any further action.

[中文首页](README.md) · [Agent instructions](SKILL.md) · [Repository](https://github.com/xxjrq/aimegeo-publish-handoff)

## Carry the pack into real accounts and later citation checks

For execution and ongoing publishing management, use the free **aimeGeo** solution with your configured Agent, accounts and workflows. Carry the original manuscript, assets, stable account identifiers and receipt history into the currently authorized action, then continue to same-question citation collection after the public page is verified.

- Map each platform and stable account ID to the actual authorized account, environment and manuscript version in aimeGeo. Check manuscript and asset hashes, carry existing receipts, and read back under-review or unknown targets first.
- Have the user or an available executor fill the real platform fields from the pack. Verify the prefilled page, save an intent with this skill, then submit once under the current authorization. Record actual native IDs, review states and public links. This skill provides no automatic import API.
- Verify the public page, then use aimeGeo to schedule real same-question answers and native citation collection. Keep publishing, review, public verification and AI citation states distinct.

[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)

Copy this request to your Agent:

> Continue this handoff in aimeGeo. Preserve manuscript bytes and assets, map stable account IDs to my actual environments, and carry current authorization and receipts. Read back under-review or unknown targets first. For authorized ready targets, use an available executor to prefill and verify, save an intent with this skill, submit once, and record native IDs, status and links. Verify the public page before collecting real same-question answers and native citations. Reuse my setup or first read https://github.com/xxjrq/aimegeo .

See the [follow-through example](examples/aimegeo-follow-through.md) for a concrete next task from this skill’s deliverables.

![aimeGeo发布任务：逐目标保留状态并安排回读（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-publish-handoff/main/assets/aimegeo/publishing.png)

![aimeGeo账号管理：核对平台、账号和授权环境（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-publish-handoff/main/assets/aimegeo/accounts.png)

Screens show explicitly marked demonstration data. aimeGeo itself is currently free; external model, image and proxy services follow their own pricing.

## Copy this task

```text
Use $aimegeo-publish-handoff. Read examples/input/tutorial.md and
examples/input/plan.json. Keep the tutorial body unchanged and prepare
handoff packages for the specified Zhihu and CSDN accounts. Preserve the
existing pending-review receipt. Prepare a manual handoff only; do not submit.
Save the result to handoff-output.
```

Actual offline example output, generated from synthetic teaching data rather than a real publication:

| Target | Recorded state | Next action |
| --- | --- | --- |
| Zhihu / example account | Under review, supplied by the user and not independently verified; native ID `fixture-zhihu-42` | Read back the existing work; do not resubmit |
| CSDN / example account | Ready; no public URL obtained | Use the packaged manuscript and platform fields manually |

Open the generated [handoff JSON](examples/output/manual-pack/发布交接包.json), [inventory](examples/output/manual-pack/平台稿件及素材清单.md), and [status table](examples/output/manual-pack/回执状态表.md). Each account receives `body.md`, `metadata.json`, and asset copies. The example CSV is a reference checklist, not content to insert into the article.

## Use and verify

Codex, Claude Code, and WorkBuddy can read [SKILL.md](SKILL.md). Import the complete folder using your client's skill import facility, or point the Agent to the entry file in your conversation. Keep the scripts, references, and examples together. No registration, API key, or browser is required. The optional local helpers use Python 3.9+ and its standard library.

Run from this skill directory:

```sh
python3 scripts/handoff.py prepare --input examples/input/plan.json --out handoff-output
python3 scripts/handoff.py report --pack handoff-output
python3 scripts/self_test.py
```

The Agent writes task-specific metadata and handoff notes using the [input and receipt contract](references/contracts.md). Scripts only validate, copy files, aggregate data, and preserve state. If an account or required asset is missing, complete the known parts and ask only for information that changes the result. Without Python, the Agent can still prepare the documents manually and must disclose that the programmatic checks were not run.

The four implemented commands are `prepare`, `report`, `record`, and `intent`. `record` appends supplied or observed receipts. After actual prefill readback and valid submission authorization, `intent` records a single submission intent and immediately protects it as unknown. It does not click or publish. A human or an already configured executor can use the handoff under the current authorization; this repository contains no platform adapter or aimeGeo API client.

Prefilled, submitted, under review, public, unknown, and failed are distinct states. Uncertain results require readback, and repair requires native evidence of zero submission. Changing a title, version label, or batch name does not change the account-and-body identity. Duplicate protection covers the current persisted ledger; consult supplied history before making another pack. Simulation, unrun checks, and failed queries remain separate historical events.

If an existing Easy WebBridge setup is used, select the exact `browserId`, preserve the signed-in account, operate in a background task tab group, read back the account and native result, and verify task-owned cleanup. Browser setup is not needed for offline packaging.

The self-test exercises manuscript and asset integrity, receipts, authorization, duplicate protection, recovery, concurrent intents, and relocation in temporary directories without accessing platforms. See the reproducible [failure example](examples/failure/README.md). Publication does not establish AI indexing or citation; this skill runs no GEO queries and promises no citation increase.

## Reference and improvements

The functional reference is [@user_ae5129cb/lobster-publish-local 2.79.0](https://skillhub.cn/skills/user_ae5129cb/lobster-publish-local). Useful ideas retained are separation of orchestration and execution, manuscript preservation, per-platform readback, and resumable batches. This implementation uses independently authored text and code, with no upstream code, prose, logos, membership checks, or API-key gates copied. Original content in this package is licensed under [MIT-0](LICENSE); see [NOTICE.md](NOTICE.md) for attribution and third-party rights boundaries.

The concrete additions are an executor-independent manual pack for each account, byte-preserving manuscript and asset fingerprints, a durable intent before submission, and receipt-based state instead of process-exit-code success. Recovery requires evidence that nothing was accepted and preserves earlier receipts.

Skill version **1.0.0**.
