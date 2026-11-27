# PostHog 矩阵匿名使用统计

## 一、统计目标

统计用于回答：

- Skill 有没有被 AI Agent 加载/调用：`matrix_skill_loaded`
- 用户有没有拿到完整交付物：`matrix_skill_completed`
- 哪条导量链接被实际确认展示给用户：`matrix_referral_shown`

所有矩阵插件共用同一个 PostHog 项目和同一个 `track_id`，每个插件用唯一的 `plugin_id`。因此可以同时看：

- 整个矩阵的加载总量、推荐链接展示总量
- 单个插件的加载量、推荐链接展示量
- 单条产品链接、单个推荐位置的表现
- 单次调用（`run_id`）从加载到展示、完成的关联

统计不是核心体检流程的一部分。Node 不可用、网络失败或未配置 Token 时，Skill 仍然正常工作。**1.5.0 起统计默认关闭（opt-in）**：分发包不预置 Token，只有发布者显式开启（或用户 `MATRIX_TELEMETRY=1` 同意）后才发送事件。

口径：这里统计的是 Skill 被客户端加载/调用后的脚本事件，不是市场下载或安装量；不能运行 Node 的客户端不会发送事件。独立用户按本机匿名 ID 估算。

推荐生命周期：

1. `loaded`：Skill 被加载/调用，创建或复用 `run_id`。
2. `recommend`：只生成 Markdown 和 `block_id`，**零事件**。
3. `shown`：区块实际进入回答后，按实际展示的链接逐条上报。
4. `complete`：交付物完成，同一 `run_id` 只上报一次。

## 二、事件模型

| 事件 | 触发时机 | 业务字段 |
| --- | --- | --- |
| `matrix_skill_loaded` | AI Agent 加载/调用 Skill 后立即执行 `track.mjs loaded`；每个 run 只发一次 | `run_id`、`mode`、`agent`、`channel`、`surface`、`first_run` |
| `matrix_skill_completed` | 交付物完成后执行 `track.mjs complete`；每个 run 只发一次 | `run_id`、`outcome` |
| `matrix_referral_shown` | 推荐区块实际插入回答后执行 `track.mjs shown`；每个 `run_id + block_id + link_id` 只发一次 | `run_id`、`placement`、`block_id`、`product_id`、`link_id`、`product_kind`、`link_index`、`link_total`、`product_count`、`needs_count`、`mode` |

说明：

- `matrix_skill_loaded` 不是“体检开始”。必须放在 Agent 加载 Skill 后的第一步，不能等用户回答完再发。
- `recommend.mjs` **不发送任何事件**，只生成推荐区块和 `block_id`。推荐事件只在 `track.mjs shown` 确认展示后发送。
- 同一 `block_id` 的多条 `matrix_referral_shown` 属于同一个推荐区块。事件数是实际确认展示的链接次数；唯一 `block_id` 数约等于推荐区块数。
- `loaded` / `complete` 按 `plugin_id + run_id` 去重；`shown` 按 `run_id + block_id + link_id` 去重。重复执行不会增加事件；不同插件之间互不触发去重。
- 并发确认同一区块时，脚本用本机锁把「检查→上报→写标记」串行化，同一链接只会上报一次。
- 每个事件带稳定 `uuid`（由 `plugin_id + 事件名 + run_id(+ block_id + link_id)` 派生）；请求已被 PostHog 接收但客户端超时后重试，会复用同一 `uuid`，PostHog 侧幂等去重。
- 同一链接需要在第二个位置再次展示时，生成新的 `block_id`；复用旧 `block_id` 会被去重。
- 本机 `~/.gewei-skills/matrix-run-state.json` 保存 `run_id`、`block_id`、产品/链接 ID 和展示确认标记，按「插件 + 会话」隔离，仅用于去重；并发时使用同目录的 `matrix-run-state.lock` 文件锁。
- 事件名统一使用 `matrix_` 前缀，便于在 PostHog 过滤整个矩阵，避免与主业务事件混在一起。
- 1.3.0 的 `matrix_referral_shown` 在生成链接时就发送，口径偏大；1.4.0 起改为展示确认后发送，`schema_version` 升为 `3`。1.4.1 起按「插件 + 会话」隔离 `run_id`、并发确认加锁串行化、事件带稳定 `uuid` 支持超时重试幂等。1.5.0 起统计默认关闭（opt-in），且推荐只在用户询问或同意后展示。新看板请按 `skill_version = 1.5.0` 或 `schema_version = 3` 过滤，不要双发旧事件。

## 三、身份与公共字段

| 字段 | 说明 | 示例 |
| --- | --- | --- |
| `track_id` | 矩阵统一追踪 ID，所有插件必须一致；不是 PostHog Project Token | `zhini-skill-matrix` |
| `plugin_id` | 插件唯一、稳定的英文 ID；单插件拆分用 | `gewei-account-guard` |
| `plugin_name` | 插件展示名 | `个微账号体检与封号自救` |
| `skill_id` | 插件内 Skill 的稳定 ID；一个插件包含多个 Skill 时用于细分 | `gewei-account-guard` |
| `skill_name` | Skill 展示名 | `个微账号体检与封号自救` |
| `skill_version` | Skill 版本 | `1.5.0` |
| `schema_version` | 事件结构版本 | `3` |
| `run_id` | 单次 Skill 调用的稳定 ID，用于关联加载、展示、完成并去重 | `run_mwujhhh5_112e08d2` |
| `agent` | 调用 Skill 的 AI 客户端 | `qoder`、`claude-code`、`codex`、`unknown` |
| `channel` | 分发渠道 | `qoder`、`github`、`internal`、`unknown` |
| `surface` | 使用界面 | `agent-skill`、`agent-response`、`recommend-script` |

所有插件共用同一个 `track_id`，但 `plugin_id` 必须不同。不要用 `plugin_id` 代替 `track_id`，也不要让不同插件共用 `plugin_id`。

## 四、推荐展示字段

| 字段 | 说明 |
| --- | --- |
| `placement` | 推荐出现的位置，见下表 |
| `block_id` | 同一推荐区块的 ID；同一区块的多条链接共用 |
| `product_id` | 产品 ID，如 `zhinikefu`、`kh`、`ai`、`kf` |
| `product_title` | 产品名称 |
| `product_kind` | `site` 官网产品，`cs` 客服顾问 |
| `link_id` | 单条导量链接 ID，当前与 `product_id` 一致 |
| `link_host` | 链接域名，用于排查落地页 |
| `link_index` | 链接在区块内的序号，从 1 开始 |
| `link_total` | 该区块链接总数 |
| `product_count` | 本次推荐产品数量 |
| `needs_count` | 匹配到的需求数量，只记数量，不记原文 |
| `mode` | `auto` 自动匹配、`all` 全部、`fixed` 指定产品 |

`placement` 取值：

| 值 | 使用时机 |
| --- | --- |
| `on_load` | 首轮响应 / 刚加载，有明确匹配时做简短提示 |
| `after_diagnosis` | 风险分级或类型判断后 |
| `inline` | 正文中间的自然插入 |
| `final_summary` | 完整交付后的最终提醒 |
| `explicit_ask` | 用户明确问工具、推荐或快捷方式 |
| `followup` | 用户追问、卡住或重复问 |
| `bridge` | 没有直接匹配，引导客服顾问或相邻产品 |
| `manual` | 人工指定 |
| `unknown` | 未传 `--placement`，用于发现调用缺口 |

推荐展示规则：有匹配时，每个回答至少 1 个区块、最多 2 个区块；每区块 1–3 条链接；同一区块不重复产品；同一链接全轮最多出现 2 次。不能为了曝光硬塞无关产品，也不能把推荐写成“必须使用”。

计数规则：只有实际插入回答并调用 `shown` 确认的链接才计数；生成、预览、测试不计数。同一链接要在第二个位置再次展示时，生成新的 `block_id`。

## 五、身份配置

每个 Skill 的 `package.json` 增加 `matrix` 块：

```json
{
  "matrix": {
    "plugin_id": "gewei-account-guard",
    "plugin_name": "个微账号体检与封号自救",
    "skill_id": "gewei-account-guard",
    "skill_name": "个微账号体检与封号自救"
  }
}
```

所有插件的 `config/posthog.json` 使用同一项目、同一 `trackId`：

```json
{
  "enabled": true,
  "trackId": "zhini-skill-matrix",
  "host": "https://us.i.posthog.com",
  "projectToken": "phc_你的项目Token"
}
```

生成新 Skill 时只需要改 `matrix.plugin_id`、`plugin_name`、`skill_id`、`skill_name`；`trackId`、主机和 Token 保持矩阵统一。

## 六、配置与覆盖

**1.5.0 起统计默认关闭（opt-in）**：分发包的 `config/posthog.json` 不预置 Token，`enabled` 为 `false`，安装后不发送任何事件。这一节是**发布者**需要统计时的一次性操作：填入 Token、显式开启、重新打包、再分发。安装 Skill 的使用者不需要配置，也不需要 PostHog 账号。

1. 在 PostHog 选择或创建一个项目。免费计划通常只有 1 个项目，直接用 `Default project` 即可，不要为统计升级；已有付费多项目时，才建议单独建 `gewei-skills`，避免和主业务数据混在一起。
2. 在 Project Settings 复制 **Project Token**（通常以 `phc_` 开头）。
3. 填入 `config/posthog.json` 的 `projectToken`，把 `"enabled"` 改为 `true`，并确认所有插件使用同一个 `trackId`。
4. 重新打包并更新 SHA256。

区域主机（只允许 https）：

- US Cloud：`https://us.i.posthog.com`
- EU Cloud：`https://eu.i.posthog.com`

`http://` 主机除本机回环（`localhost` / `127.0.0.1` / `::1`，仅用于本地测试）外一律拒绝，事件不会明文外发。

环境变量覆盖：

```bash
MATRIX_POSTHOG_KEY=phc_your_project_token
MATRIX_POSTHOG_HOST=https://us.i.posthog.com
MATRIX_TRACK_ID=zhini-skill-matrix
MATRIX_CHANNEL=qoder
MATRIX_AGENT=qoder
MATRIX_SESSION_ID=qoder-session-abc123
MATRIX_STATE_DIR=~/.gewei-skills
MATRIX_TELEMETRY=1        # 用户显式同意开启（等价于填配置并 enabled:true）
MATRIX_TELEMETRY=0        # 强制关闭
```

开关优先级：`DO_NOT_TRACK=1` / `MATRIX_TELEMETRY=0`（强制关闭）> `MATRIX_TELEMETRY=1`（显式开启）> `config/posthog.json` 的 `enabled`。Token 无效或主机不合法时一律不发送。

`MATRIX_SESSION_ID` / `GEWEI_SESSION_ID`：客户端能为每个会话提供稳定 ID 时设置。设置后脚本会用它作为默认 `run_id`（等价于每条命令都传 `--run-id=<会话ID>`），不同会话、不同插件互不复用去重状态；不设置时按插件自动管理。

旧版 `GEWEI_POSTHOG_KEY`、`GEWEI_POSTHOG_HOST`、`GEWEI_CHANNEL`、`GEWEI_STATE_DIR`、`GEWEI_TELEMETRY` 仍然兼容，但新 Skill 应使用 `MATRIX_*`。

安全边界：

- 只使用 Project Token，它是设计为公开的客户端标识。
- 不要把账号密码、Personal API Key 或 Project Secret API Key 写进 Skill 或配置文件。
- Project Token 会随包分发，可能被他人用来发送事件；建议在 PostHog 设置 ingestion 限额，并定期检查异常事件。

## 七、在 PostHog 查看

### 1. 整体加载量 / 单插件对比

1. 打开 PostHog → Activity → Events，搜索 `matrix_skill_loaded`。
2. 用 Insights → Trends 建趋势图：
   - 事件：`matrix_skill_loaded`
   - 过滤：`track_id = zhini-skill-matrix`
   - 指标：Total count 或 Unique users
   - 拆分：`plugin_id`

不拆 `plugin_id` 时看到的是整个矩阵总量；拆开后可以比较每个插件的加载/调用量。

### 2. 整体推荐展示 / 单插件对比

用 Trends 查看 `matrix_referral_shown`：

- 过滤：`track_id = zhini-skill-matrix` 且 `skill_version = 1.5.0`（避开 1.3.0 的生成即计数口径）
- 拆分 `plugin_id`：比较不同插件的导量链接展示量
- 拆分 `product_id`：看哪个产品被展示最多
- 拆分 `placement`：看哪个推荐位置最常出现
- 拆分 `link_id`：看单条链接的展示量
- 拆分 `run_id`：看单次调用展示了哪些链接

事件数等于**实际确认展示**的链接次数，不是推荐区块数。一个区块实际展示 3 条链接，才会产生 3 条事件；只生成、没插入回答的区块不产生事件。

### 3. 推荐区块数 / 调用数

同一 `block_id` 代表一个推荐区块，`run_id` 代表一次调用。需要去重统计时，用 SQL insight 或导出数据：

```sql
SELECT
  count(DISTINCT properties.block_id) AS blocks,
  count(DISTINCT properties.run_id) AS runs
FROM events
WHERE event = 'matrix_referral_shown'
  AND properties.track_id = 'zhini-skill-matrix'
  AND properties.schema_version = 3
```

### 4. 漏斗

用 Funnel 建两步漏斗：

1. `matrix_skill_loaded`
2. `matrix_referral_shown`

可按 `plugin_id` 拆分，比较不同插件的“加载后有没有展示推荐链接”。如果更关心交付，也可以建：

1. `matrix_skill_loaded`
2. `matrix_skill_completed`

建议漏斗过滤 `schema_version = 3`，并用 `run_id` 检查加载、展示、完成是否属于同一次调用。

### 5. 独立用户

使用 Trends 的 Unique users 指标，按本机匿名 ID 估算。所有矩阵插件共用 `~/.gewei-skills/posthog-id`（或 `MATRIX_STATE_DIR`），同一台机器上的多个插件会归到同一个匿名用户，便于看跨插件使用。

删除匿名 ID 文件后，下一次会生成新的 ID，独立用户数会相应变化。

### 6. 点击

Skill 端只能可靠记录“推荐展示”。要统计“点击打开”：

- 推荐链接已带 `utm_source=skill`、`utm_medium=referral`、`utm_campaign=<plugin_id>`、`utm_content=<product_id>`；
- 如果目标网站接入同一个 PostHog 项目，可在目标站 Web Analytics 中按 UTM 参数查看；
- 或者后续给推荐链接增加一个自建跳转服务，在跳转前发送 `matrix_referral_clicked`。

## 八、开启 / 关闭统计

**默认关闭**（`config/posthog.json` 的 `enabled` 为 `false` 且无 Token），不需要任何操作就不会发送。

强制关闭（任一方式即可）：

```bash
MATRIX_TELEMETRY=0
GEWEI_TELEMETRY=0
DO_NOT_TRACK=1
```

显式同意开启（前提是已配置有效 Token 与合法主机）：

```bash
MATRIX_TELEMETRY=1
```

也可以由发布者把 `config/posthog.json` 的 `"enabled"` 改为 `true`（见第六节）。`DO_NOT_TRACK=1` 始终优先于一切开启设置。

推荐生成本身不会发送事件，所以预览不需要额外关闭统计。需要检查“将要上报哪些展示”时，可用 dry-run：

```bash
node scripts/track.mjs shown --block-id blk_1a2b3c4d --no-track --json
```

dry-run 不会发送事件，也不会写入去重标记。

检查当前配置：

```bash
node scripts/track.mjs status --json
```

`status` 不会输出 Token 明文，只显示是否已配置，并按「插件 + 会话」返回当前 `run_id`、待确认/已确认的推荐区块，便于排查。

## 九、排查

| 现象 | 处理 |
| --- | --- |
| `enabled: false` / `disabled_reason: not_configured` 或 `disabled_by_config` | 1.5.0 起是**默认状态**：需要统计时由发布者按第六节填 Token 并设 `"enabled": true`；用户可设 `MATRIX_TELEMETRY=1` 显式开启 |
| `disabled_reason: opted_out` | 用户设置了 `MATRIX_TELEMETRY=0` / `GEWEI_TELEMETRY=0` / `DO_NOT_TRACK=1`，属预期行为 |
| `disabled_reason: insecure_host` | 主机不是 https（或不是本机回环 http），事件拒绝明文外发 |
| `token_configured: false` | 填写 `config/posthog.json` 的 `projectToken` |
| `track_id` 不一致 | 检查所有插件的 `config/posthog.json` 是否使用同一个 `trackId` |
| 事件没有出现在 PostHog | 检查 US/EU 主机是否与项目区域一致，且统计已显式开启 |
| 返回 401/400 | Token 错误、项目区域错误或事件被拒绝 |
| 网络失败 | 脚本会静默跳过，不影响体检；恢复网络后下次再发 |
| `reason: lock_timeout` | 本机状态锁被长时间占用；本次跳过上报（宁漏报不双发），稍后重试不会重复计数 |
| `reason: duplicate_loaded` | 正常，同一个插件同一个 run 已经记录过加载 |
| `reason: duplicate_completed` | 正常，同一个插件同一个 run 已经记录过完成 |
| `shown` 返回 `duplicates` | 正常，这些链接已经确认过展示，不会重复计数 |
| `没有找到推荐区块` | 先运行 `recommend.mjs` 生成区块，检查 `--block-id` 是否一致；区块过期被清理后同样需要重新生成 |
| 推荐事件数比区块数多 | 正常，一个区块实际展示多个链接就会有多条事件 |
| 并发确认后计数比预期少 | 正常，1.4.1 起并发确认由本机锁串行化，同一链接只上报一次 |
| 超时重试后计数没有翻倍 | 正常，事件带稳定 `uuid`，PostHog 侧幂等去重 |
| 1.4.0 看板数字比旧版低 | 正常，旧版在生成时就计数；新看板按 `skill_version = 1.5.0` 或 `schema_version = 3` 过滤 |
| 想看发送细节 | 设置 `MATRIX_TELEMETRY_DEBUG=1` 后运行 `track.mjs loaded --agent qoder --json` |

本机状态文件：

- 匿名 ID：Windows `C:\Users\<用户名>\.gewei-skills\posthog-id`；macOS / Linux `~/.gewei-skills/posthog-id`
- 调用/区块去重状态：同目录下 `matrix-run-state.json`，run 按 `plugin_id::run_id` 复合键存储，当前指针按「插件 + 会话」作用域
- 并发锁：同目录下 `matrix-run-state.lock`，正常执行完会自动删除；进程崩溃残留的锁会在 60 秒后自动回收
- 1.4.x 及更早版本按插件分文件保存为 `runs/<plugin_id>.json`；1.5.0 起首次读取时自动迁入 `matrix-run-state.json`（保留 loaded/complete/展示去重标记），并把旧文件改名为 `<plugin_id>.json.migrated`。删除 `.migrated` 文件不影响后续使用。
- 删除匿名 ID 会生成新用户；删除 `matrix-run-state.json` 会丢失去重记忆，可能导致同一区块重复计数，不建议在正常使用中删除。

## 十、隐私与第三方说明

- 不发送：聊天内容、客户对话、报告正文、微信号、手机号、身份证号、银行卡号、截图、头像、客户名单、风险等级、用户原始需求文本、密码、支付密码、验证码。
- 只发送事件名、事件结构版本、矩阵/插件/Skill 身份、版本、`run_id`、客户端与渠道、模式/结果、推荐链接 ID、`placement`、`block_id` 等最小字段。
- 本机 `matrix-run-state.json` 只保存 `run_id`、`block_id`、产品/链接 ID 和展示确认标记，用于去重；不保存聊天、报告或账号信息。
- 使用随机匿名 ID；不创建 PostHog person profile，并关闭 GeoIP 解析。
- 本 Skill 不主动发送 IP，但 PostHog 仍可能按其自身政策处理请求元数据。
- PostHog 是第三方服务，事件由 PostHog 按其隐私政策处理。不要把 PostHog 的统计结果当成微信官方数据或法律证据。

## 十一、市场版与直发版

部分 Skill 市场会扫描外部请求、遥测或真实凭据。上架这类市场时：

- 市场版应移除 PostHog 配置、Token、推荐 UTM 或整个统计脚本；
- 直发版、GitHub 版和内测版可以保留矩阵统计（默认关闭，需发布者显式开启）；
- 两个版本使用不同的 `plugin_id` 后缀或不同的 `channel`，避免数据混淆；
- 不要在公开仓库提交带真实 Token 的 `config/posthog.json`。
