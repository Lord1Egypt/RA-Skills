# 数据契约

请求必须包含 `runtime: easy-webbridge`、非敏感 `accountAlias`，以及含 `niche`、`audience`、非空 `contentPillars` 的 `accountProfile`。`keywords` 可省略或包含 0-5 项，`browserId` 可省略，`searchLimitPerKeyword` 为 1-20。输出数量固定为 5；若请求带 `planCount`，它只能是 5。

成功快照为 `schemaVersion: 1.0`、`kind: douyin-visible-topic-snapshot`、`status: success`。它包含唯一 `runId`、账号别名和定位、采集时间、来源范围及来源数组。每个 `sourceId` 以本次 `runId` 开头；重复作品只保留一个来源对象，但 `evidence` 保留其在热点页和搜索页各自可见的标题、作者、时间与指标原文。

草稿为 `kind: douyin-topic-plan-draft`、`status: draft`，必须绑定同一快照的 `accountAlias`、`sourceRunId` 和 `snapshotId`，并固定含 5 个 `plans`。每项必须包含 `topic`、单个 `title`、`hook3s`、`angle`、`accountFit`、本次快照的 `sourceIds`，以及严格按“开场、核心展开、结尾行动”排列的三段 `outline`。风险状态保留在内部字段，不得把待复核内容写成确定事实。

最终输出为 `publishable-plan.json` 和 `publishable-plan.md`，包含本次可见来源清单与 5 条选题，状态固定为 `ready_for_human_review`，不得表示已发布。失败时写脱敏 `run-diagnostic.json` 并清理旧成功文件。

退出码：0 成功；1 页面、连接或门禁失败；2 输入或数据契约错误。不得持久化 Cookie、Token、Authorization、Local Storage、登录身份、session、tab ID 或 Bridge 原始响应。
