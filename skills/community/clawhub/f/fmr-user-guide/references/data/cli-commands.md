# CLI 命令与 REST 等价全表

**分发事实（先读）**：`free-model-cli.js` 属 **Skill 形态**分发物——`scripts/` 目录不进 standalone 便携包（打包白名单只有 `core`/`standalone`/`package.json`，3.0.2 实物 zip 同）。standalone 用户的主界面 = **REST（本机回环免密）+ `/admin` 面板**，下表"REST 等价"即 standalone 写法。Skill 形态存量用户（迁移期）机器上仍有该 CLI，可按表用 CLI 列。

**通用行为**：

- CLI 多数命令先 `ensureRouter()`——Router 未运行会自动 spawn **该 CLI 所在包自带的 core** 并最多等 30 秒。此即 **③类陷阱**：拉起的往往是旧版 core（直写共享数据、覆写 `router.pid`、占 5678 旁路服务管理面），且"命令能跑"≠"进程一直在"。**带③标注的命令不能当存活探针**；Router 疑似停止时先走 SKILL.md 探针。
- REST 直调免此陷阱：Router 不在时请求直接拒连，天然是探针。
- 事件三命令（`event-check`/`mark-notified`/`mark-read`）直读 `data/events.json`，不经 Router，无拉起副作用。

分组：**①** 模式无关可依赖；**②** OpenClaw 耦合（写 `openclaw.json`，standalone 不适用）；**③** 带 ensureRouter 自动拉起陷阱（Skill 形态 CLI 上）。

| 命令 | REST 等价 | 用途与副作用 | 分组 |
|---|---|---|---|
| `help` | — | 列命令清单 | ① |
| `setup` | 仅初始化部分 ≈ `POST /api/setup` | 启动 Router + 初始化 + 写 openclaw.json + 输出 cron 注册指令；已装幂等 | ②＋③ |
| `stop` | 平台服务面停止 | 读 `router.pid` → SIGTERM → 删 PID 文件；不拉起 | ① |
| `uninstall` | —（standalone 用卸载脚本，见 upgrade 章） | 停进程 + 删 openclaw.json 的 FMR 条目；数据/cron 保留，主备角色不回滚 | ② |
| `providers` | `GET /api/providers` | 渠道全景（key/启停/健康/主备）；打印层无 `website` 列，注册链接以 REST 为准 | ①＋③ |
| `models [provider]` | `GET /api/models?provider=<id>` | 模型清单（复制准确模型 ID 用） | ①＋③ |
| `providerApiKey <p> <key>` | `POST /api/provider-key` `{provider, apiKey}` | 设 key（单 key **替换**语义）；写后自动拉模型，失败静默 | ①＋③ |
| `switchProviderPrimaryModel <p> <m>` | `POST /api/switch-primary` `{provider, modelId}` | 切主模型；**不校验模型 ID 存在**，写错成功但路由不到——先查 models 复制准确 ID | ①＋③ |
| `disableProvider <p>` | `POST /api/toggle-provider` `{provider, enabled:false}` | 整渠道下线 | ①＋③ |
| `enableProvider <p>` | `POST /api/toggle-provider` `{provider, enabled:true}` | 整渠道恢复 | ①＋③ |
| `disableProviderModel <p> <m>` | `POST /api/toggle-model` `{provider, modelId, enabled:false}` | 禁单模型（若命主池自动提升 fallback） | ①＋③ |
| `enableProviderModel <p> <m>` | `POST /api/toggle-model` `{provider, modelId, enabled:true}` | 恢复单模型 | ①＋③ |
| `configureModelRole <primary\|fallback>` | —（直接改 openclaw.json） | 设 OpenClaw 主/备角色；设主时原主模型自动移入备用列表 | ② |
| `disableReporting` | `POST /api/reporting` `{enabled:false}` | 关健康事件上报；**无对称 enable**，重开走面板 | ①＋③ |
| `event-check` | —（直读 events.json） | 输出待推送事件 Markdown 并自动标已读；排除 dailyStatus | ① |
| `mark-notified <id,...>` | —（直改 events.json） | 事件标已推送（逗号分隔 ID；不存在者静默跳过） | ① |
| `mark-read <id,...>` | —（直改 events.json） | 事件标已读 | ① |

CLI **没有** `status`/`health`/`doctor`/`version` 命令（能力缺口如实标注）：判据一律走 `GET /healthz` + `GET /api/status` + `/admin` 面板 + `data/router.pid`（见 usage 章）。
