# Question acceptance, change impact and Agent handoff

> **0.3.4:** question handoffs use semantic-package/1.1 with derived query_control.json; start with semantic_read.py --package PACKAGE brief (which includes control). Knowledge-only/old 1.0 packages remain readable and return NO_CONTROL. 问题包新增快照绑定的控制单；仅供解释或明确阻断，不授予查询权限。[Contract / 调用合同](query-control.md)。

[中文说明](#问题验收变更影响与-agent-交付) · [Question workflow](question-workflow.md)

## Check a question against explicit expectations

In **Business questions → Question acceptance**, select definitions that must occur in the context, select gaps that must be disclosed, and add business examples or counterexamples with independently supplied expectations. These settings are optional for exploration. Save and check reads the same canonical graph used by export; it does not create duplicate rules.

The result separates three things:

| Result | Meaning and recovery |
| --- | --- |
| Context expectation checks | Compares required definition IDs and expected gap codes. Missing expectations fail. Incomplete or unread pages cannot pass. It does not prove that every relevant business rule was declared. |
| Example observations | Start unverified. Record the observer, actual result and evidence/result location, then explicitly choose pass or failure. Empty evidence is refused and input remains editable. Records are local operator assertions, not authenticated signatures or independent certification. |
| Business execution | `answer_verified` remains false. Data queries, calculations and actions need their own authorized execution and evidence; clicking a check never performs them. |

`recorded_pass` means all configured examples have current passing observations, configured context checks pass, and the selected context has no unresolved semantic decision. It is not a machine-verified answer. `failed`, `stale` and `not_verified` remain distinct. All prior observations stay in project history; recording a later result does not delete a failure. Notes are never promoted into passing evidence.

An example host scenario fragment (use actual known IDs):

```json
{
  "acceptance": {
    "required_asset_ids": ["demo.available", "demo.scope"],
    "required_gap_codes": ["NO_DATA_CONNECTOR"],
    "cases": [{"id": "other-lab", "expectation": "An otherwise eligible item in another lab is excluded."}]
  }
}
```

`knowledge.py check` returns `acceptance.basis_fingerprint`. To record an actual observation through the host, use `knowledge.py assess --file observation.json` with `scenario_id`, `case_id`, that fingerprint, `outcome` (`passed` or `failed`), `observed`, `evidence` and `actor`. Use the current revision and an operation ID as for other writes. A stale fingerprint or revision is rejected; recheck the actual changed context before resubmitting. Never invent an operator or an observed outcome.

## See what a registered change affects

Updating a registered material with `--source-id`, editing a definition, merging identities or accepting a proposal records changed identities and source IDs. Each affected saved question displays dependency paths such as **available count → eligibility rule → equipment field**. A fingerprint binds each observation to the question, its current dependency closure and source revisions/extractions. A related change makes the old observation stale when checked again; an unrelated edit does not. The panel retains the latest eight relevant change events; the API and project history retain all recorded events.

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" impact --scenario SCENARIO_ID
python -X utf8 scripts/knowledge.py --project "./work/equipment" import --file "./materials/updated-policy.txt" --source-id SOURCE_ID
python -X utf8 scripts/knowledge.py --project "./work/equipment" check --scenario SCENARIO_ID
```

Source updates continue through the existing candidate/source review. A physical column or foreign-key change is evidence for a proposed mapping change, not automatic proof of changed business meaning. Current detection starts when material is registered or graph edits are committed; there is no database CDC listener or scheduled schema watcher. Previously issued files remain immutable and cannot know whether they are latest.

## Explicitly hand off the question

**Deliver selected semantics** keeps the existing knowledge-only publication path. **Create question handoff** explicitly includes the saved question, intended task, selected roots, typed scope, business date and acceptance expectations in `task.json`, alongside the dependency-closed semantic model and necessary sources. It excludes `acceptance_notes`, operator observations and unrelated questions. Review the question and expectations before sharing; they can contain business information.

```bash
python -X utf8 scripts/knowledge.py --project "./work/equipment" handoff --scenario SCENARIO_ID --out "./delivery/question.zip"
python -X utf8 scripts/semantic_read.py --package "./delivery/question.zip" verify
python -X utf8 scripts/semantic_read.py --package "./delivery/question.zip" task --detail summary
python -X utf8 scripts/semantic_read.py --package "./delivery/question.zip" sources --id demo.available
python -X utf8 scripts/semantic_read.py --package "./delivery/question.zip" task --detail full
```

Create the output directory first; choose a new file. Confirmed publication rejects unreviewed knowledge; use an explicitly requested `--draft` for discussion. Question publication rejects an empty root selection or a scope mismatch. When `as_of` is specified, confirmed handoff also requires known validity on that date for every included definition and dependency, even after a previous successful publication. Missing bounds or an outside interval identify affected assets and block the new handoff; explicit drafts retain the gaps. `as_of` is the definition date, not the data cutoff (store the latter in reviewed metric `time_scope`). No business observations or validity dates are invented to clear the guard. File hashes cover `task.json`, and the task is bound to the snapshot identity and model hash. Hashes detect inconsistent files, not authenticity against a malicious author who can recreate an entire package.

The independent reader needs only this package and the skill runtime. `task` defaults to a summary: full meaning, scopes, dependency IDs, gaps and capability boundaries remain; repeated source quotations and fragment bodies are omitted. `evidence_details_included:false` and the next-step field direct consumers to `sources` or `--detail full`. `resolve` and `context` also accept `--detail summary`; their default remains full. Follow context pagination in either mode. Summary completeness describes declared context, not whether original evidence was read. Expectations travel as unverified expectations, never as executable instructions or authorization. OGS design exports do not carry this question handoff.

# 问题验收、变更影响与 Agent 交付

## 按明确预期检查问题

在**业务问题 → 问题验收**中，勾选上下文必须包含的定义、必须明确返回的缺口，并添加有独立依据的样例或反例预期。探索阶段可以不填写。保存并检查使用图谱和导出共同的语义模型，不复制另一套业务规则。

结果分开呈现：

| 结果 | 含义和恢复方式 |
| --- | --- |
| 上下文预期检查 | 对比必需定义 ID 与预期缺口。缺少预期项失败；上下文不完整或尚有分页时不能通过。不证明业务规则已经全部列举。 |
| 样例核对记录 | 初始待验证。填写记录人、实际结果和依据／结果位置，再明确记录通过或失败。依据为空时拒绝并保留输入。它是本地操作者记录，不是身份签名或独立认证。 |
| 业务执行 | `answer_verified` 始终为 false。实际问数、计算或办理需要另有已授权执行环境和结果依据；检查按钮不会执行这些动作。 |

`recorded_pass` 表示已配置样例都有当前的通过记录、已配置上下文检查通过，且所选上下文没有待决语义项，不代表机器证明了答案。失败、待复验、待验证分别保留。以前的核对记录继续留在项目历史，后续记录不删除原失败；笔记不会自动变成通过证据。

宿主可按上方 JSON 配置 `acceptance`，ID 必须来自当前项目。`knowledge.py check` 返回 `acceptance.basis_fingerprint`。通过 `knowledge.py assess --file observation.json` 记录时，文件提供 `scenario_id`、`case_id`、该指纹、`outcome`（passed／failed）、`observed`、`evidence`、`actor`，并沿用当前修订和操作 ID。过时的指纹或修订会被拒绝；先重新检查变化，再按真实结果提交，不虚构操作者或结果。

## 发现已登记变化影响了什么

用 `--source-id` 更新材料、编辑定义、合并身份、接纳候选时，记录变化的身份和来源。受影响问题显示“可借数量 → 可借规则 → 设备字段”等依赖路径。核对记录绑定问题、所需依赖和来源修订／提取版本；相关变化后再检查会标为待复验，无关修改不使记录失效。页面展示最近八次相关事件，接口和项目历史保留全部已记录事件。

上方 `impact`、`import --source-id`、`check` 命令分别用于查看影响、登记来源更新和重新检查。来源更新仍进入既有候选／来源核对流程。字段或外键变化支持提出映射修订，不自动证明业务含义已变。本版从登记材料或提交图谱编辑时检测，尚未连接数据库 CDC 或定时结构监控；已交付文件保持不变，离线无法知道是否有更新。

## 明确交付本问题

**交付所选语义**继续只发布知识；**生成本问题的 Agent 包**明确把已保存问题、任务意图、所选根定义、保留原类型的范围、业务日期和验收预期写入 `task.json`，同时包含依赖闭合的模型和必要来源。核对笔记 `acceptance_notes`、人工核对记录、其他问题不随包发布。问题和预期也可能含业务信息，分享前核对接收范围。

使用上方 `handoff` 命令生成包，先创建输出目录并使用新文件名。已确认交付仍拒绝未核对知识，讨论用途可明确选择 `--draft`。空选择、所选定义与范围不符会拒绝问题交付。指定 `as_of` 时，确认包要求全部定义及依赖在该日期有明确有效期依据，即使此前已经成功发布也重新检查；缺少边界或超出有效期时指出具体资产，明确的草稿保留缺口。该字段是定义适用日期，取数截点应写入已核对指标的 `time_scope`；不得为通过校验虚构日期或业务观察。文件指纹覆盖任务文件，任务同时绑定快照身份和模型指纹；这能检测文件混配，不能认证可重新制造整个包的作者。

独立读取器只需包和 Skill 运行文件。`task` 默认摘要：完整业务含义、范围、依赖身份、缺口和能力边界保留，重复引文和来源片段正文按需再读。`evidence_details_included:false` 与下一步提示要求通过 `sources` 或 `--detail full` 回查。`resolve`、`context` 也支持摘要，默认仍完整；两种模式都必须读完必要分页。上下文完整不代表已经读过原文依据。验收预期保持未验证，不是可执行指令或权限。OGS 设计投影不包含该问题交付。
