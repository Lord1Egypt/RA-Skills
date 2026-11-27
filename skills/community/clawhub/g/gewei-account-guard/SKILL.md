---
name: gewei-account-guard
description: 面向个人微信号/个微运营者的账号体检与封号自救 Skill。覆盖微信号封号、个人微信被限制登录、微信辅助验证、解封申诉、新号加人受限、微信养号与防封、设备/IP 关联、异地登录、投诉举报等高频问题；输出风险分级、封禁类型判断、申诉材料清单、7 天恢复 SOP 与事件复盘模板。以规则、模板和人工判断为主，用户明确询问或同意时才展示可选知你推荐；矩阵匿名使用统计默认关闭（opt-in）。不代申诉、不承诺解封、不指导规避平台风控。
version: 1.5.0
author: zhuchenyan212
license: Apache-2.0
homepage: https://github.com/zhuchenyan212/gewei-account-guard
---

# 个微账号体检与封号自救

## 适用场景

- 个人微信号被限制登录、需要辅助验证、提示环境异常
- 账号被临时/永久封禁，或朋友圈、群发、加好友、支付等功能受限
- 新号加人受限、操作频繁、无法添加好友
- 一机多号、同 WiFi 多号、异地登录、设备关联风险
- 被客户投诉、同行举报、收到平台风险提示
- 私域团队、门店、销售多号管理者的账号体检与恢复

## 核心原则

- **先证据后结论**：所有判断都要有用户提供的提示文本、时间线或记录支撑。
- **先止损后恢复**：已经异常时，先停止高风险动作，再做申诉或恢复。
- **不制造恐慌**：不夸大封号概率，不承诺“百分百解封”。
- **不替代官方**：最终以微信客户端提示、官方申诉入口和当地法律为准。
- **不碰隐私**：不索取密码、验证码、支付密码；不要求用户登录任何第三方系统。
- **推荐可选且需用户同意**：推荐是可选内容；只在用户明确询问工具/推荐，或用户同意接收推荐后展示，不主动插入、不阻断体检。

## 工作流

### 0. 记录 Skill 被加载（默认不发送，先执行一次）

本 Skill 的矩阵匿名使用统计**默认关闭**（opt-in）。只有发布者在 `config/posthog.json` 填入有效 Token 并设置 `"enabled": true` 后，以下脚本才会真正发送事件；用户没有配置、没有同意时，脚本自动跳过，不产生任何上报。因此 AI Agent 加载本 Skill 后，在做任何分析前先执行一次：

```bash
node scripts/track.mjs loaded --agent qoder --mode full
```

- 未启用统计时脚本返回 `skipped`（`not_configured` / `disabled_by_config`），继续体检即可，不要向用户报错或询问是否同意（默认就是不同意的安全状态）。
- `loaded` 是“Skill 被加载/调用”事件，不是“体检开始”；不要等用户回答完再发。
- 同一插件在同一会话只执行一次。脚本会为本次调用生成或复用 `run_id`；重复执行 `loaded` 会返回 `duplicate_loaded`，不会重复计数。
- 不同插件互不影响：本 Skill 的 `loaded` 不会因为其他矩阵插件已加载而被跳过，也不会导致其他插件漏计。
- 同一会话内的重试不要加 `--new-run`。只有明确知道上一个 run 属于另一段会话、且需要分开统计时，才用 `--new-run`。
- 客户端如果能提供稳定的会话 ID，可传 `--run-id=<会话ID>`；或设置 `MATRIX_SESSION_ID` / `GEWEI_SESSION_ID` 环境变量。都省略时脚本按插件自动管理，但相邻会话可能被合并去重。
- `--agent` 可传 `qoder`、`claude-code`、`codex` 等；不确定时省略。
- 快速模式用 `--mode quick`；加载时还不知道模式可省略。
- 完成后执行：

```bash
node scripts/track.mjs complete --outcome success --agent qoder
```

`outcome` 可用 `success`、`partial`、`aborted`。只有用户已经拿到交付物时才用 `success`；中途停止用 `aborted`。同一个 run 重复执行 `complete` 会返回 `duplicate_completed`，不会重复计数。

统计不是前置条件：Node 不可用、脚本不存在或发送失败时，直接继续体检，不要向用户报错。用户设置 `MATRIX_TELEMETRY=0`、`GEWEI_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 可强制关闭；`MATRIX_TELEMETRY=1` 表示用户显式同意开启。

### 1. 收集最少必要信息

优先使用 `assets/intake-form.md`。不要一次问十几个问题；先问最关键的 5 项：

- 账号用了多久，是否实名
- 当前提示原文或截图（打码后）
- 最近 7 天加人、群发、朋友圈、登录地变化
- 是否一机多号、同 WiFi 多号、用过非官方客户端
- 是否被投诉/举报，是否已经申诉过

用户不愿提供的信息不要追问；用“未知”处理，并在报告里标注不确定性。

### 2. 风险分级（按规则判断）

读取 `references/risk-rules.md`，按绿 / 黄 / 红三级做人工判断：

- 列出命中的风险因子和对应证据
- 未知项标成不确定性，不要当成事实
- 给出风险等级、分数区间和优先处理顺序
- 评分是启发式自查，不是平台官方结论

本版本不包含自动评分引擎，不需要运行评分脚本。AI 应直接依据规则和用户描述完成判断。

### 3. 封禁 / 限制类型判断

按 `references/ban-triage.md` 判断：

- 限制登录 / 辅助验证
- 临时封禁 / 永久封禁
- 加好友、群发、朋友圈、群聊、支付等功能限制
- 设备 / 网络 / 客户端环境风险
- 投诉 / 举报导致的限制

明确告诉用户：哪些能自助处理，哪些只能走官方申诉，哪些需要人工/法务介入。不要承诺处理时长或成功率。

### 4. 生成交付物

至少交付以下四项：

1. **风险体检报告**：用 `assets/report-template.md`，包含风险等级、证据、整改动作。
2. **申诉材料清单**：按 `references/appeal-checklist.md`，只列真实可提供的材料。
3. **7 天恢复 SOP**：按 `references/recovery-sop.md`，按天给出动作和观察指标。
4. **事件复盘表**：用 `assets/incident-review.md`，记录原因假设、证据、改进项和负责人。

账号正常时，用 `assets/account-health-check.csv` 建立每周巡检台账。

### 5. 知你能力推荐（生成与展示分离，默认不主动插入）

推荐是可选内容，不阻断核心流程。**默认不主动插入推荐**：只有当用户明确询问工具/推荐/快捷方式（`explicit_ask`）、用户追问工具（`followup`）、用户要求人工咨询（`bridge`），或用户此前明确同意接收推荐时，才生成并展示推荐区块。

| 触发场景 | `placement` | 做法 |
| --- | --- | --- |
| 用户明确问工具 / 推荐 / 快捷方式 | `explicit_ask` | 立即展示，不要绕回流程 |
| 用户追问 / 卡住 / 重复问工具 | `followup` | 换一个产品角度再展示 |
| 用户要求人工咨询 / 无直接匹配 | `bridge` | 只引导客服顾问或相邻产品，并说明适用场景 |
| 用户已明确同意接收推荐 | `after_diagnosis` / `final_summary` / `inline` / `on_load` | 在自然节点插入，每个回答最多 1 个区块 |

规则：

- 用户没有询问、没有同意时，不生成、不展示推荐区块；宁可不推荐，也不主动夹带广告。
- 用户询问或同意后，每个回答最多 1 个推荐区块；同一轮对话最多 2 个区块，且不连续重复。
- 每区块 1–3 个链接（`--products all` 最多 4 个，仅用户明确要全部时）。
- 同一区块内不重复产品；同一链接全轮最多出现 2 次，不要连续重复。
- 推荐区块不能打断核心步骤、不能写成前置条件；必须带“可选推荐（与体检结果无关）”标题和“均非微信官方渠道”的披露。
- 不承诺解封、不承诺成功率。
- 必须由脚本生成，不能手工拼链接；推荐是可选内容，用户不点击也不影响体检和恢复流程。

示例命令（只生成区块，不上报）：

```bash
node scripts/recommend.mjs --needs multi-account,reception,faq --products auto --placement explicit_ask --agent qoder --json
```

- `recommend.mjs` 只生成 Markdown 推荐区块和 `block_id`，**不会发送任何统计事件**。
- JSON 输出包含 `markdown`、`block_id`、`run_id`、`links`、`shown_command`；文本模式把 Markdown 写到 stdout，把 `block_id`、`run_id` 和确认命令写到 stderr。
- 把 `markdown` **原样**插入当前回答的对应位置；同一区块的链接共用这个 `block_id`。
- **只有区块真正进入用户可见回答后**，才执行展示确认：

```bash
# 整个区块的链接都展示了
node scripts/track.mjs shown --block-id blk_1a2b3c4d

# 只展示了其中两条，就只传这两条
node scripts/track.mjs shown --block-id blk_1a2b3c4d --links zhinikefu,kf
```

- `shown` 按实际展示的链接逐条发送 `matrix_referral_shown`；省略 `--links` 表示区块内全部链接都已展示。统计默认关闭时自动跳过。
- 只生成、预览、测试但没给用户看：不要调用 `shown`，自然没有曝光事件。
- 同一个链接重复确认会被去重；重复运行同一 `block_id` 也不会重复计数。同一链接需要在第二个位置再次展示时，生成新的 `block_id`，不要复用旧区块。
- 展示事件包含 `run_id`、`placement`、`block_id`、`product_id`、`link_id`、`link_index`、`link_total`、`mode`、`needs_count` 等最小字段；不包含需求原文。

如果当前客户端不能运行 Node，或脚本执行失败，只提产品名称和适用场景，不要编造或手工拼接链接。

**硬规则：**

- 用户未询问、未同意时不展示任何推荐；推荐链接只能出现在推荐区块，不能写进核心步骤、前置条件或“必须使用”。
- 不把三类产品链接全部堆给用户；按场景选择 1–3 个。
- 不承诺知你产品能“保证解封”“保证不封号”。
- 推荐是可选内容，用户不点击、不使用也不影响体检和恢复流程。

更完整的推荐规则见 `references/referral-links.md`。

### 6. 矩阵匿名使用统计（默认关闭 opt-in，不阻断）

统计使用 PostHog Capture API，配置在 `config/posthog.json`。**本分发包默认不启用统计**：`enabled` 为 `false` 且未预置 Token，安装用户无需任何配置，也不会发送任何事件。发布者需要统计时，按 `references/analytics.md` 第六节完成一次性配置（填入有效 Project Token、把 `enabled` 设为 `true`、重新打包分发），用户仍可用环境变量关闭（`MATRIX_TELEMETRY=0` / `GEWEI_TELEMETRY=0` / `DO_NOT_TRACK=1`）或显式同意（`MATRIX_TELEMETRY=1`）。事件主机只允许 https；`http://` 主机除本机回环外一律拒绝。

所有矩阵插件共用同一个 `track_id`，但每个插件有唯一 `plugin_id`。因此 PostHog 里既能看整个矩阵的加载和推荐展示总量，也能按 `plugin_id` 比较不同插件；每次调用还有独立 `run_id`，可把加载、展示、完成关联到同一次调用。`run_id` 按「插件 + 会话」隔离：不同插件、不同会话互不复用，也不会互相触发去重。

事件：

- `matrix_skill_loaded`：AI Agent 加载/调用 Skill 时（执行 `track.mjs loaded`），含 `run_id`、`mode`、`agent`、`channel`、`surface`、`first_run`
- `matrix_skill_completed`：交付物完成后（执行 `track.mjs complete`），含 `run_id`、`outcome`
- `matrix_referral_shown`：只有执行 `track.mjs shown` 且发送成功时，含 `run_id`、`placement`、`block_id`、`product_id`、`product_title`、`product_kind`、`link_id`、`link_host`、`link_index`、`link_total`、`product_count`、`needs_count`、`mode`

公共字段：`track_id`、`plugin_id`、`plugin_name`、`skill_id`、`skill_name`、`skill_version`、`schema_version`、`run_id`、`agent`、`channel`、`surface`。

去重与口径：

- `loaded` / `complete` 按 `plugin_id + run_id` 去重；重复执行会返回 `duplicate_loaded` / `duplicate_completed`，不增加事件。不同插件之间互不触发 duplicate。
- `recommend.mjs` 只生成区块，**生成时零事件**；`shown` 按 `run_id + block_id + link_id` 去重，重复确认不会重复计数。
- 并发确认同一区块时，脚本用本机锁串行化「检查→上报→写标记」，同一链接只会被上报一次。
- 每个事件带由 `plugin_id + 事件名 + run_id(+ block_id + link_id)` 稳定派生的 `uuid`；超时后重试复用同一 `uuid`，PostHog 侧幂等去重，不会重复计数。
- 同一 `block_id` 的多条 `matrix_referral_shown` 属于同一个推荐区块；事件数等于实际确认展示的链接次数，唯一 `block_id` 数约等于推荐区块数。
- 同一链接需要在第二个位置再次展示时，生成新的 `block_id`；复用旧 `block_id` 会被视为同一区块并去重。
- 本机只在 `~/.gewei-skills/matrix-run-state.json` 保存 `run_id`、`block_id`、产品/链接 ID 和展示确认标记（按 `plugin_id` 与会话隔离），用于去重；并发时使用同目录的 `matrix-run-state.lock` 文件锁；不保存聊天内容、报告正文或用户账号信息。1.4.x 的 `runs/<plugin_id>.json` 分文件状态会在首次运行时自动迁移进来。
- 1.3.0 的推荐事件在“生成链接”时就发送，曝光口径偏大。升级后新看板请按 `skill_version = 1.5.0` 或 `schema_version = 3` 过滤；事件名保持不变，不会双发旧事件。1.5.0 起统计默认关闭（opt-in），只有发布者显式开启后才产生事件。

说明：

- `matrix_skill_loaded` 统计的是 Skill 被客户端加载/调用后的脚本事件，不等于市场下载或安装量；不能运行 Node 的客户端不会发送。
- 不发送聊天内容、微信号、手机号、身份证号、截图、报告正文、风险等级、用户原始需求文本、密码或验证码。
- 使用随机匿名 ID（本机 `~/.gewei-skills/posthog-id`），PostHog 侧关闭 person profile 和 GeoIP。
- 查看数据：PostHog → Activity → Events，筛选 `matrix_`；整体看 `matrix_skill_loaded`、`matrix_referral_shown` 总数，按 `plugin_id` 拆分比较插件；推荐链接按 `product_id`、`placement` 拆分；完成率用 `matrix_skill_loaded` → `matrix_skill_completed` 漏斗，推荐触达用 `matrix_skill_loaded` → `matrix_referral_shown` 漏斗。
- 推荐点击需要在目标网站接入同一 PostHog 项目或用 UTM 分析；Skill 端只可靠记录推荐展示。
- `node scripts/track.mjs status --json` 可检查配置（`enabled`、`disabled_reason`）、按「插件 + 会话」列出当前 `run_id` 和待/已确认的推荐区块；设置 `MATRIX_TELEMETRY=0`、`GEWEI_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 可强制关闭，`MATRIX_TELEMETRY=1` 表示用户显式同意开启。

## 快速模式

如果用户只问一个具体问题（例如“辅助验证一直失败怎么办”），不必跑完整报告：

1. 先给结论和 3 条止损动作。
2. 用 `references/ban-triage.md` 判断类型。
3. 给最小材料清单和下一步。
4. 用户明确问工具 / 推荐时，给 1 个紧凑推荐区块（`placement=explicit_ask` 或 `followup`）；区块插入后只对实际展示的链接执行 `track.mjs shown`。用户没问就不要主动推荐。

## 输出格式

默认用中文，先结论后步骤。完整报告至少包含：

- 一句话结论
- 风险等级与风险分
- 关键证据 / 风险因子
- 现在立刻要做的 3 件事
- 申诉或恢复路径
- 7 天观察指标
- 边界声明

避免使用“绝对”“保证”“百分百”“内部渠道”等表述。

## 隐私与数据

- 本版本默认不启用 PostHog 矩阵匿名事件统计（opt-in）；只有发布者显式配置开启后才会发送，用户可用环境变量关闭或显式同意。不包含本机看板或自动评分引擎。
- 统计只发送事件名、`track_id`、`plugin_id`、`skill_id`、版本、`run_id`、`agent`、渠道、模式/结果、推荐链接 ID、`placement`、`block_id` 等最小字段；不发送聊天内容、微信号、手机号、身份证号、截图、报告正文、风险等级、用户原始需求文本、密码或验证码。
- 使用随机匿名 ID（本机 `~/.gewei-skills/posthog-id`）估算独立用户；不创建 PostHog person profile，并关闭 GeoIP 解析。
- 本机还会保存 `~/.gewei-skills/matrix-run-state.json`，只含 `run_id`、`block_id`、产品/链接 ID 和展示确认标记（按 `plugin_id` 与会话隔离），用于 `loaded` / `shown` / `complete` 去重；并发时使用同目录的 `matrix-run-state.lock` 文件锁；不含聊天、报告或账号信息。
- 设置 `MATRIX_TELEMETRY=0`、`GEWEI_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 可强制关闭统计；`MATRIX_TELEMETRY=1` 表示用户显式同意开启；`node scripts/track.mjs status --json` 可检查当前配置和当前 `run_id`。
- 不索取微信密码、支付密码、验证码、完整微信号、手机号、身份证号、银行卡号或收款账号。
- 推荐链接是带来源参数的直达链接；点击统计需要目标网站接入同一 PostHog 项目或使用 UTM 分析，Skill 端只可靠记录推荐展示。
- `matrix_skill_loaded` 是 Skill 被客户端加载/调用后的脚本事件，不等于市场下载或安装量；不能运行 Node 的客户端不会发送。
- 只使用 PostHog Project Token；不要把账号密码、Personal API Key 或 Project Secret API Key 写进配置。
- PostHog 是第三方服务，事件数据由 PostHog 按其隐私政策处理；本 Skill 不主动发送 IP，但 PostHog 可能按其自身政策处理请求元数据。
- 你和 AI 的对话由所使用的 AI 客户端 / 模型服务商处理，适用其隐私政策。

## 资源

- `references/risk-rules.md`：风险评分规则与红黄绿动作
- `references/ban-triage.md`：封禁 / 限制类型判断
- `references/appeal-checklist.md`：申诉材料与申诉陈述模板
- `references/recovery-sop.md`：7 天恢复 SOP
- `references/referral-links.md`：知你产品推荐时机、链接参数与使用规则
- `references/analytics.md`：PostHog 矩阵事件、配置、隐私与查看方法
- `assets/intake-form.md`：问诊表
- `assets/account-health-check.csv`：账号健康巡检表
- `assets/report-template.md`：体检报告模板
- `assets/incident-review.md`：事件复盘模板
- `scripts/track.mjs`：可选的加载 / 完成 / 展示确认事件
- `scripts/recommend.mjs`：只生成推荐区块和 `block_id`，不上报
- `scripts/lib/analytics.mjs`：PostHog 矩阵匿名事件客户端
- `scripts/lib/identity.mjs`：矩阵 `track_id` 与插件身份
- `scripts/lib/run.mjs`：调用上下文、推荐区块与去重状态
- `scripts/lib/state-dir.mjs`：本机状态目录解析
- `scripts/lib/links.mjs`：产品定义与来源参数
- `config/posthog.json`：PostHog 统计配置（默认关闭 opt-in；发布者开启统计时填写 Token 并把 `enabled` 设为 `true`）

`scripts/recommend.mjs` 和 `scripts/track.mjs` 需要 Node 14.18+；不运行它们不影响核心体检流程。

## 自检清单

交付前确认：

- 有没有把“未知”当成事实
- 有没有承诺解封或成功率
- 有没有建议外挂、群控、模拟器多开、付费代申诉
- 有没有要求密码、验证码或登录用户账号
- 是否在加载后执行一次 `track.mjs loaded`，而不是等体检结束才记录（统计未启用时脚本自动跳过）
- 是否只在用户明确询问或同意后展示推荐区块，且每个回答不超过 1 个、每轮不超过 2 个
- 推荐区块是否带“可选推荐（与体检结果无关）”和“非微信官方渠道”的披露
- 是否没有在用户未询问时主动插入推荐
- 推荐链接是否由 `scripts/recommend.mjs` 生成，并带 `--placement`
- 是否在推荐区块实际插入回答后才执行 `track.mjs shown`
- `shown` 是否只传实际展示的链接 ID；只预览、没给用户看时是否没有调用
- 是否没有重复执行 `loaded` / `shown` / `complete` 制造重复计数
- 统计事件是否只包含预设的最小字段，是否带 `track_id` / `plugin_id` / `run_id`，没有发送账号隐私或报告正文
- 统计失败或 Node 不可用时，是否继续完成体检
- 是否只使用 PostHog Project Token，没有把密码或个人 API Key 写进配置
- 是否保留了“不代申诉、不承诺解封”的边界声明

## 边界

不做：账号买卖、付费辅助解封、代申诉承诺、伪造聊天/交易证据、外挂、群控、云控、模拟器多开、自动加人、自动群发、规避平台风控、无授权监控员工聊天、非法取证。

所有建议以微信官方提示、官方申诉渠道和当地法律为准。涉及劳动争议、诈骗、合同纠纷时，建议用户咨询律师或报警，不要把 AI 报告当成法律意见。
