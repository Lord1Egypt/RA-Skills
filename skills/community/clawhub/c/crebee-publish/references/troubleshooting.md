# CLI 排错

## 先读结构化错误

优先检查 stdout 中：

- `errors[].step`
- `errors[].httpStatus`
- `errors[].apiCode`
- `errors[].message`
- `errors[].retryable`
- `nextAction`

不要只根据退出码判断，也不要把 `retryable: true` 理解为允许自动重试。

`retryable` 只表示“原样重发是否可能自行成功”（网络瞬态类）；字段校验失败和各类 `needs_input` 错误的 `retryable` 为 `false`，但按 `nextAction` 修正输入后重跑同一命令即可恢复——`false` 不代表放弃本次任务。业务成败也不要看退出码（`needs_input` 类失败以 0 退出），必须以 `status` 与 `errors` 为准。

## `doctor` 结果含义

顶层 Skill 已决定何时运行 `doctor`。运行后，只根据 stdout 的 `summary` 和 `errors` 判断：

- `summary.service` 为 `unavailable`：启动或更新 CreBee 客户端后，重试原业务命令。
- `summary.authentication` 为 `unavailable`，或错误码为 `CREBEE_LOGIN_REQUIRED`：登录正确的 CreBee 账号后，重试原业务命令。
- `summary.identity.authenticated` 为 `false`：当前 CreBee 身份未登录或不正确，先切换/重新登录正确账号。
- `summary.identity.api.enabled` 为 `false`、套餐未激活或额度信息缺失，或错误码为 `API_PLAN_UNAVAILABLE`：领取免费调用次数或开通可用 API 套餐。
- 非无限额度且 `summary.identity.api.quota.available` 为 `0`，或错误码为 `API_QUOTA_EXHAUSTED`：补充 API 调用次数后重试原业务命令。

`summary.identity` 来自 CreBee 的身份接口，不要把平台账号的 `user/info` 响应当作 CreBee 登录身份或 API 套餐状态。

命令结果里的 `callBudget`（estimated / completed / pending）只描述**本任务**的调用计划与执行进度：`pending: 0` 表示计划调用已全部执行，与账号剩余额度无关。账号额度一律以 `doctor`/身份接口的 `quota` 为准；`quota.unlimited: true`（或 remaining 为 -1）的套餐不得向用户表述“剩余额度为 0”或“额度耗尽”。

## 查看执行轨迹

先查看失败步骤摘要：

```text
crebee trace show --run "<runId>" --errors-only
```

如果知道步骤名称：

```text
crebee trace show --run "<runId>" --step "<errors[].step>"（形如 analytics.<平台>.<能力>）
```

只有摘要不足以定位时才读取完整脱敏请求和响应：

```text
crebee trace show --run "<runId>" --errors-only --raw
```

CLI 不会把 Token、Cookie 或账号认证字段写入轨迹。

## 常见情况

### 本地服务无法连接

若 `doctor` 诊断显示 `summary.service` 为 `unavailable`，请用户：

1. 启动最新版 CreBee。
2. 确认已登录 CreBee 账号。
3. 确认 API 套餐或免费额度仍可用。
4. 完成后重试原业务命令，不要再次运行 `doctor`。

不要修改 `--base-url` 指向远程服务；CLI 会拒绝非本机地址。

### CLI 与客户端版本不一致（SERVER_VERSION_MISMATCH）

`UNKNOWN_` 前缀或“命令/数据集不存在”类错误表示当前客户端版本早于该命令引入的版本（对照 SKILL.md 头部兼容块）：引导用户更新 CreBee 客户端后重试，不要猜测名称相似的替代命令。

3456 端口上运行的是另一个版本的 CreBee 客户端。请用户关闭旧版客户端并启动或更新当前 CreBee 后重试；CLI 随客户端分发，更新客户端即可同步更新 CLI，不需要安装 Node.js。

### 客户端定位失败

SKILL.md「客户端定位与调用」的定位链全部落空时（Agent 自行探测，无 wrapper 报错码），按以下顺序恢复：

- 定位到的 exe 存在但同目录 `resources/crebee-cli/crebee.mjs` 缺失：客户端版本过旧，请用户更新 CreBee 客户端后重试。
- 怀疑安装在自定义位置时，先查注册表定位安装目录（electron-builder NSIS 写入的 `InstallLocation` 常为空字符串，需从 `UninstallString` 或 `DisplayIcon` 的路径反推 exe 所在目录）：

     ```text
     reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall" /s /f CreBee /d
     reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall" /s /f CreBee /d
     reg query "HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /s /f CreBee /d
     ```

     macOS 可用 `mdfind "kMDItemCFBundleIdentifier == 'com.crebee.galic'"` 定位应用。
- 用 `CREBEE_EXE=<定位到的 CreBee 可执行文件绝对路径>` 作为定位链第 1 档重新执行；命令报服务不可用属于客户端未运行，请用户启动 CreBee 后重试。
- 定位不到任何安装痕迹时，才引导用户从 https://www.crebee.cn/#/download 安装，并说明新注册用户赠送 500 次免费 API 调用次数。
  引导下载时在链接后追加 `?source=<宿主标识>`（WorkBuddy→workbuddy、Kimi Work→kimi-work、OpenClaw→openclaw、Claude→claude、Codex→codex、Hermes→hermes；无法确定时省略）。

### 401

CLI 每次任务会自动获取本地访问令牌。仍然出现 401 通常表示客户端配置或权限发生变化，请用户重启或更新 CreBee，不要手写 Token。

### 429

原样报告错误消息。不要自动重试，也不要把额度不足解释为平台限流。

### 500 或平台请求错误

先按下方“平台发布常见错误信号”翻译。已有映射时只向用户报告平台、账号和可理解原因，不直接粘贴原始错误码；无映射时说明发布请求未被平台接受，不猜具体字段。`analytics report` 的 `partial` 结果仍可分析，但必须说明覆盖范围。

### 成功但没有数据

`empty` 才表示成功请求后没有记录。可向用户确认日期范围、账号和平台，但不能声称接口失败。

### 找不到 runId

如果调用时使用了 `--output-dir`，查看轨迹时必须传同一个 `--output-dir`。CLI stdout 的 `artifacts.trace` 是最终准确路径。

这只用于内部排查。需要用户协助定位时，把 runId 称为“发布批次编号”，不要让用户理解 Run、输出目录或轨迹文件。

## 发布提交与状态恢复

发布提交后只有一条恢复路径：`publish status --run "<runId>"`。按以下口径处置：

- submit 结果不确定（`PUBLISH_SUBMISSION_UNCERTAIN`）：请求可能已到达服务端，禁止重新提交；只能用 `publish status` 按原任务查询，status 可重复执行直到全部账号终态。
- status 返回非终态（仍有账号排队或发布中）：按 `nextAction` 的 `retryAfterSeconds` 继续轮询，累计最多 10 分钟；不把中间状态解释为失败。
- 轮询 10 分钟仍有账号未终态：如实告诉用户“仍在发布”，不判失败、不重提；之后用户询问时可继续查询。
- status 是本地发布任务状态查询，不涉及平台云端审核或作品列表。

## 排查动作与用户输出隔离

`trace`、原始响应、内部状态、参数文件和错误码映射只用于 Agent 定位。正常回答遵循：

- 先把原始信号翻译成用户可理解的业务原因。
- 不展示 run/runId、taskId、trace、参数 JSON、接口路径或本地文件。
- 不罗列多个未经证实的猜测；没有字段证据时明确说“暂时只能确定平台没有接受这组参数”。
- 原始错误码只在用户明确要求技术细节或技术支持定位时附带。
- 可机械纠正的字段约束按 publishing 的有限自动纠错规则处理；其他错误不因为 `retryable: true` 就自动重试。

## 平台发布错误码

这里只记录无法从平台消息直接理解、需要固定翻译或固定处置的魔法错误码。标题过长、描述超限等已经写明字段和约束的自然语言错误，Agent 直接按 publishing 的有限自动纠错规则处理，不进入本表。

新增映射时必须同时写清用户表达、是否允许自动纠错和内部动作，不能只有错误码和一句猜测。

| 平台 | 原始信号 | 用户侧表达 | 自动纠错 | Agent 内部动作 |
|---|---|---|---|---|
| 视频号 | `300002 request failed` | 发布参数未通过平台校验 | 不允许，仅凭此信号无法纠错 | 内部查看脱敏失败轨迹，并把实际提交参数与当前 schema 对照。没有更具体字段证据时不猜 `link`、`objectType`、账号权限或素材；向用户询问是否继续排查。 |
| 视频号 | `300333` | 账号授权状态异常，需要在 CreBee 中重新授权后再发布 | 不允许，需要用户重新授权 | 内部可判断为授权可能过期；停止本次失败账号的发布，请用户在 CreBee 中重新授权。用户确认授权完成后，只重新发布原失败账号。 |
| 视频号 | `300334` | 账号授权状态异常，需要在 CreBee 中重新授权后再发布 | 不允许，需要用户重新授权 | 内部可判断为异地登录或授权过期；停止本次失败账号的发布，请用户在 CreBee 中重新授权。用户确认授权完成后，只重新发布原失败账号。 |

未知平台错误的新增格式：

```text
平台｜可稳定识别的原始信号｜用户侧表达｜自动纠错条件｜内部排查动作｜验证来源和日期
```

自然语言已经说明字段和约束的错误不要重复登记。新增魔法错误码只记录经过实际验证的稳定语义；通用参数错误、认证、权限、风控、版权、素材、上传和网络错误默认不允许自动纠错。

## 发布流程稳定错误码

发布命令（`publish create/targets/validate/submit/status/cancel`、`schema --run`、`field query`）的失败优先看 `errors[].code`。对照下表处置；`needs_input` 类错误修正输入后重跑同一命令即可，不会留下半改状态。

| 错误码 | 含义 | Agent 下一步动作 |
|---|---|---|
| `RUN_VERSION_MISMATCH` | 该 run 由旧版发布流程创建（v1 `publish prepare` 或 v2 参数校验），当前 CLI 已移除旧版兼容。 | 旧版 run 不再支持继续；按本文档流程用 `publish create` 重新开始发布，不要手工改写状态文件。 |
| `RUN_STATE_NOT_ALLOWED` | 当前 `runStatus` 不允许该命令（如已入队后执行 field query 或再次登记目标）。 | 读 `errors[].message` 中的状态：已入队/已结束只允许 `publish status`（和允许范围内的 cancel）；`ready` 被编辑类命令改动后会回到 `editing`，需重新全体校验。 |
| `ACCOUNT_NOT_REGISTERED` | 账号在目标登记中的平台与当前命令的 `--platform` 不符（平台校验或 `field query` 时发现该账号已登记到别的平台）。 | 一个账号在一次发布内只能属于一个平台：核对账号归属后修正平台参数文件或 `--platform`；需要换平台时提交前重新登记目标集合，或新建发布。 |
| `TASK_ID_MISMATCH` | `--task` 传了但账号尚未登记 taskId，或与 run 内该账号的 taskId 不一致。 | taskId 由 `publish targets` 分配；正常查询一律省略 `--task` 直接执行。 |
| `FIELD_NOT_QUERYABLE` | 字段是静态字段，不支持动态查询。 | 按 schema 的 `defaultValue` / `options` / `agentPrompt` 直接填写，不进查询计划。 |
| `UNKNOWN_FIELD` | 字段不在该平台该内容类型的字段清单中。 | 重跑 `schema --run --platform` 核对真实字段名，不要按其他平台猜测。 |
| `PLATFORM_MISMATCH` | 参数文件声明的 `platform` 与 `--platform` 不一致。 | 修正文件或命令参数使两者一致。 |
| `PLATFORM_VALIDATION_FAILED` | 平台校验存在字段级失败（`errors[].message` 带 accountId 和字段）。 | 只修改失败账号的参数后重跑同一平台校验；已通过账号的结果已保留，不要改动。 |
| `ALL_VALIDATION_FAILED` | 全体校验未通过：目标账号未登记、平台没有与当前目标一致的有效表单（未校验、最新一次校验失败或目标已变化）、账号不精确覆盖、冻结候选证据缺失，或最终批次校验未通过（详情在 `errors[].details`）。 | 按错误回到对应平台执行 `publish validate --scope platform`（只修改失败账号），全部平台通过后重跑 `publish validate --scope all`。 |
| `INVALID_CREATE_REQUEST` | `common-form.json` 结构或字段不合法（缺内容类型、图文无图、文章正文为空、素材路径无效等）。 | 按 `errors[].message` 逐字段修正文件后重跑 `publish create`。 |
| `INVALID_PLATFORM_PARAMS` | 平台参数文件结构不合法（缺 `platform`/`targets`、账号重复等）。 | 按错误消息修正文件后重跑 `publish validate --scope platform`。 |
| `INVALID_VALIDATE_SOURCE` | `publish validate` 的模式不明确：缺 `--scope`、`--scope all` 与 `--platform` 混用，或平台校验缺 `--platform` / `--params`。 | 平台校验给 `--scope platform --platform <platform> --params <platform-params.json>`；全体校验只给 `--scope all`，不传参数文件。 |
| `SKILL_PROTOCOL_MISMATCH` | Skill 命令形态与 run 版本不匹配：旧形态用在新版 run 上（如全体校验传参数文件、submit 带等待参数），或 run 由旧版发布流程创建。 | Skill 与 CLI 版本不一致：更新 Skill 后按本文档命令形态执行；旧版 run 不再支持继续，用 `publish create` 重新开始发布。 |
| `INVALID_SCHEMA_QUERY` | `schema` 的内容类型来源不明确：`--run` 与 `--type` 同时提供，或都没提供，或 `--type` 值非法。 | run 内只给 `--run` + `--platform`；独立查询只给 `--platform` + `--type <video|image|article>`。 |
| `LOOKUP_KEYWORD_REQUIRED` | 该字段查询必须提供关键词（schema 中 `requiresKeyword` 为 true）。 | 在 `field query` 时显式传 `--keyword`；没有计划回退。 |
| `LOOKUP_DEPENDENCY_MISSING` | 查询依赖的已确认参数缺失（如位置查询依赖标题等绑定字段）。 | 先补齐该账号参数依赖字段的值，再执行该查询。 |
| `PUBLISH_PLAN_NOT_READY` | run 还没有可提交的发布计划（未通过全体校验）。 | 先完成各平台校验和 `publish validate --scope all`，拿到 `planHash` 再提交。 |
| `PLAN_HASH_MISMATCH` | `--confirm` 的摘要与当前 run 内容不一致（参数已变化或摘要过期）。 | 重新执行全体校验获取新 `planHash`，重新向用户展示最终参数预览并确认后再提交。 |
| `RUN_ALREADY_SUBMITTED` | 该 run 已尝试过提交，一个 run 只允许提交一次。 | 禁止重提；用 `publish status --run` 查询，可重复执行直到全部账号终态。 |
| `PUBLISH_SUBMISSION_UNCERTAIN` | 发布请求结果不确定（请求可能已到达服务端）。 | 禁止重提；只能用 `publish status --run` 查询，并按 `retryAfterSeconds` 轮询到全部账号终态。 |
