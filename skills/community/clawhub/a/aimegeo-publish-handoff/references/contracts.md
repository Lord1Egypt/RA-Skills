# 输入、命令与状态契约

Python 3.9+，仅标准库。脚本不联网、不调用外部程序、不发现账号或读取登录凭据。写作与平台适配判断由 Agent 完成。

## 输入计划

完整输入见 [plan.json](../examples/input/plan.json)。必填：

| 字段 | 含义 |
| --- | --- |
| schema_version | 固定 `1` |
| batch_id | 用户本次交接的批次标识 |
| draft | `id`、`version`、`title`、`body_file`、`content_type: article` |
| targets | 至少一个平台账号目标 |
| assets | 可选列表，省略表示无独立素材 |
| existing_receipts | 可选列表，导入本稿已有回执 |
| existing_intents | 可选列表，原样导入用户指定旧台账中的提交意图 |

`body_file` 是相对于 plan 目录的 UTF-8 文件；只支持成稿图文，不负责视频编辑或生成文章。文件须留在输入目录内，符号链接也不得越界。正文哈希包含所有字节，包括末尾换行，不执行 trim、换行规范化或标题抽取。

素材项：`file`、`role`、`description`。`file` 在 `assets/` 下，文件名使用字母、数字、下划线、连字符、点和目录分隔符；`role` 是实际用途说明，例如 `cover`、`body_image`、`attachment`、`reference`。脚本复制已提供的文件，不推测图片可用性、版权或平台上传结果。正文图片的相对引用须与素材路径一致，Agent 在交接前检查；`reference` 资料不自动插入文章。

每个目标的必填项是 `platform`（小写 key）、`platform_name`、`account_id`、`account_name`、`authorization`；可选 `title`（缺省用原题）和 `fields`（对象）。`fields` 保存用户已给的摘要、标签、专栏等，脚本不会代填或执行其中内容。相同平台、账号、正文哈希只形成一个目标；完全相同项合并，字段/标题/授权冲突报错。不同账号独立记录。

授权对象：

```json
{
  "action": "prepare",
  "platform": "csdn",
  "account_id": "example-csdn-editor",
  "draft_sha256": "4dd80c72715ce50a5bb416afaadf30fedc3e1c17683705de01227f75385a3fab",
  "reference": "当前对话仅要求准备发布包"
}
```

上面的哈希对应随包教程；真实使用须从实际正文计算，不可用于另一篇正文。可选 `valid_until` 为带时区的 ISO 8601 时间。`submit` 仅在用户现有授权确实覆盖当前平台、账号和正文时填写；文件自身不能证明授权。脚本核对范围与到期时间，Agent 核对对话来源。先用 `prepare` 交付，之后有新提交授权时由 `intent --authorization` 持久化，原授权保留在历史中。

## 四个命令

以下命令在技能目录运行。真实使用替换路径和从 `report` 返回的目标 ID；`--target` 是包内稳定 ID，不是平台作品 ID。

```sh
python3 scripts/handoff.py prepare --input examples/input/plan.json --out handoff-output
python3 scripts/handoff.py report --pack handoff-output
```

```text
python3 scripts/handoff.py record --pack 交接目录 --receipt 本次回执.json
python3 scripts/handoff.py intent --pack 交接目录 --target 目标ID --authorization 当前提交授权.json
```

如果包中已保存有效 `submit` 授权，`intent` 可省略 `--authorization`，其余参数仍必填。`record` 一次接收一条回执。`intent` 不点击投稿；它只给外部执行器预留一次动作，并立即将本地状态置为未知。同一个目标在未知状态不能再次获取意图。刚取得意图后才能执行一次实际提交；中断或任何失败都先回读。

退出码 `0` 表示本地操作完成，`2` 表示输入、状态、授权或文件系统阻断。成功输出 JSON 到 stdout，错误 JSON 到 stderr；参数解析错误由 argparse 输出帮助并返回 `2`。`record` 保存 `query_failed` 返回 `0`，不表示查询成功。不要按退出码宣称平台投稿成功。

`prepare` 先验证所有目标、文件与历史回执，再生成整个目录，失败不交付半包。重复同一 plan 会复用台账；计划、素材或版本改变会阻止覆盖。`report` 校验正文、素材、平台字段副本的 SHA256，并从 JSON 重建两份 Markdown；它不查询平台。

`existing_receipts` 无需预先排序；先校验每项为对象、`observed_at` 为带时区时间，再按真实观察时刻升序重放已有事实。时区不同也按同一时间轴比较；计划指纹使用规范化后的历史，因此仅调整不同时间回执的列表排列仍复用原包，不覆盖后来追加的回执与授权。观察时刻完全相同则稳定保留输入相对次序，不按状态或 receipt_id 臆造先后。历史重放不会发起新的预填或提交，不用新动作的状态转移门禁拒绝已合法保存的迟到记录；回执字段、证据、账号、正文与意图关联仍完整校验。重放后从全部历史重新计算未知和已受理保护；即使当前展示为已预填，未解除的未知仍阻止新的 `record/pre_filled` 和 `intent`，不会因排序凭空取得重投权限。

### 带提交意图的历史导入

优先复制整个旧交接目录后继续 `record`/`report`。确需另建包时，从用户指定旧台账的各 `targets[].receipts` 原样汇总到 `existing_receipts`，并将对应 `targets[].intents` 原样汇总到 `existing_intents`。不要删除回执的 `intent_id`，也不要依据回执猜造意图或补写授权。完整离线字段示例见 [history-plan.json](../examples/input/history-plan.json)；其中全部记录为合成教学输入。

每条历史意图仅含原记录的 `id`、`created_at`、`draft_sha256`、`authorization`。授权须为原 `submit`，其平台、稳定账号及正文哈希须匹配当前目标，且创建时尚未超过原授权期限；不因现在已过期拒绝保存历史。意图 ID 相同且内容相同去重，内容冲突拒绝。带 `intent_id` 的回执必须在对应目标的历史意图中找到它，缺失或引用其他账号意图均报 `INTENT_MISMATCH`，不输出半包。

同账号同正文不支持无串行依据的重叠历史意图：导入后续意图前，每个更早意图必须曾有 `observed/failed` 回执，明确 `submission_absent: true` 且绑定自身，证明时间不早于该意图创建且严格早于后续意图创建。只给后一意图零提交证明、同刻证明或口述证明均不满足，`prepare` 返回 `OVERLAPPING_INTENTS`，不生成半包或覆盖既有包。后续补录的旧未知可能重新打开较早意图的保护；历史重放保留已存在的串行意图及这些反证，不把重放当作重新执行动作。新的 `intent` 仍要求所有未解除保护分别有对应证明，不能跨意图清除。

意图按创建时间排序，再与回执按观察时间合并；同一瞬间先记意图，再按输入相对次序记回执。计划指纹使用两份规范化列表，仅调整不同时间历史的排列不会重建包。迟到回执可能观察于其引用意图之前：引用身份仍校验，但该旧观察不能解除后来创建的意图。导入保留原 ID 和时间，不调用 `intent`、生成新 ID、提升当前授权或返回可点击许可；历史未闭合意图保持结果未知，已受理记录继续永久防重。只有正常 `intent` 命令在当前授权及完整门禁通过后新返回的 ID 才能交当前执行器点击一次。

## 回执与状态

回执身份必填 `receipt_id`、`platform`、`account_id`、`draft_sha256`，其正文哈希须与当前包一致；另需 `mode`、`observed_at`（含时区）、`source`、`evidence`。`source` 写用户转述、已保存原生页面记录等具体来源；`evidence` 保存足够辨认作品及状态的实际摘要，不放凭据或整页敏感数据。脚本不自动验证证据真伪，Agent 须实际核对。

| mode | 使用情况 | 是否更新当前状态 |
| --- | --- | --- |
| observed | 实际回读后提供的结构化记录 | 是，按观察时间处理 |
| user_report | 用户提供，Agent 未独立核验 | 按时间处理；不替换已核验的公开结果 |
| simulated | 演示或模拟结果 | 否，只保留历史 |
| not_run | 尚未执行查询 | 否，不能附带 status |
| query_failed | 查询异常，无可用业务状态 | 否，不能附带 status |

`status` 使用 `pre_filled`、`submitted`、`under_review`、`public`、`unknown`、`failed`。`ready` 仅为初始状态，不接收回执重置。

- 所有 mode/status 的 `native_id` 若存在且不为 `null`，须为非空白字符串，数字 ID 也用字符串传入。`submitted`、`under_review`、`public` 的有效回执须提供非空白字符串 `native_id`，不能省略或为 `null`。`public` 的 observed 回执还须有真实 HTTP(S) `public_url` 和 `public_verified: true`，表示 Agent 已回读公开页；布尔值不是脚本联网验证的结果。用户口述公开仍标注未独立核验。
- `pre_filled/observed` 需要 `checks` 恰为四项 `account/title/body/assets: true`，代表 Agent 已从原生编辑器逐项回读。缺素材或正文不一致不能勾 true。
- 每次原生回读都匹配平台、账号、正文版本，以及可用的作品 ID。发布后补充观察宜带对应 `intent_id`，不能用其他任务的返回值套入本目标。
- `unknown`、`submitted`、`under_review` 不可直接回退成可投稿的预填状态。失败只有在 `observed/failed` 明确 `submission_absent: true` 时才能重新预填；零提交证据须关联当前意图或尚未解除的旧意图，不能用另一意图的证明清除它。用户口述失败不能解除保护。
- 任何历史有效回执显示已受理，即使后来审核拒绝或历史观察较旧，也永久阻止同账号同正文再次获取意图。需修改后重提时，先保留旧记录，再依据用户授权建立实际改变后的正文版本；不靠换标题、批次名或版本标签绕过去重。
- receipt_id 相同且内容一致只复用；内容不同拒绝覆盖。旧于当前状态时间的记录只进历史。已公开状态不被后来低阶段状态覆盖；已有 `observed/public` 时，更新的 `user_report/public` 只追加历史，不替换已核验的原生 ID、公开链接、观察时间及回读标记。历史导入中的后续未知、失败或预填也只保留为历史，不降级已核验公开结果。后续实际公开页回读仍可更新当前结果。

迟到回执也参与提交保护：即使当前展示仍是较新的 `pre_filled`，更早的有效 `unknown` 或未证明零提交的失败仍会阻止 `intent` 和重新预填。按真实观察时间逐意图核对完整历史：显式 `intent_id` 只影响该意图，无 ID 的未知归属当时最近意图；早于全部意图的无归属旧记录单独保护。只有后续 `observed/failed` 的 `submission_absent: true` 才能解除自身范围；无关联零证仅解除无归属旧记录，观察早于某意图创建的证明不能解除该意图。模拟、口述失败和查询失败不能解除未知；全部保护解除后还须有实际预填回读及当前授权。已受理永久保护不受这些恢复条件影响。

以下为**合成字段示例，不是真实回读**：

```json
{
  "receipt_id": "demo-prefill-1",
  "platform": "csdn",
  "account_id": "example-csdn-editor",
  "draft_sha256": "4dd80c72715ce50a5bb416afaadf30fedc3e1c17683705de01227f75385a3fab",
  "mode": "observed",
  "status": "pre_filled",
  "observed_at": "2026-10-19T12:10:00+08:00",
  "source": "合成编辑器回读示例",
  "evidence": "仅展示契约字段；真实使用时替换为实际核对结果",
  "checks": {"account": true, "title": true, "body": true, "assets": true}
}
```

没有点击提交的确切证据不能填 `submission_absent: true`；管理页暂时无记录不足以证明零提交。一次短暂超时只记 `query_failed`，若已有意图仍保持未知，先读原任务，按用户已配置的回查节奏结束，不启无限轮询。

## 输出与恢复

包内 `source/body.md`、`source/assets/` 保存原始文件；`targets/<id>/body.md`、`metadata.json`、`assets/` 是可交接副本。素材哈希、正文版本、当前授权、历史授权、意图及回执在 `发布交接包.json` 内。Markdown 是派生视图，JSON 为恢复依据。

台账原子写入，`.handoff.lock` 阻止并发写入。看到 `PACK_BUSY` 先核对原进程；确认进程已结束且无提交在途后，才由维护者移除残留锁，不自动清锁重投。保存意图后若报告生成报错，先读取 JSON 或执行 `report`，不能再次点击。实际执行器须共用这个包作为唯一台账；脚本无法约束包外工具或人工点击。

常见阻断：`ALREADY_ACCEPTED` 只读回查；`READBACK_REQUIRED` 先回读；`CONTENT_CHANGED` 停用旧版本；`AUTHORIZATION_SCOPE` 核对平台/账号/哈希；`PLAN_CHANGED` 保留旧包后整理新版本；`VERSION_MISMATCH` 找回该回执对应的原稿。不创建新空包绕过保护。

迁移时复制整个交接目录，脚本可放任意位置。创建另一份包或跨设备独立操作前，先读取用户明确提供的历史台账并按上述合同同时导入对应回执与意图；没有历史资料就如实说明防重仅覆盖当前包。
