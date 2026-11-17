# 故障模式表

21 条起步。症状匹配后按"处置"列执行；写操作守三级写阶梯与 data-map 禁区表。"内部判据"列是全文唯一允许出现形态术语（standalone/Skill）的位置，供 agent 定位根因，非用户话术。key 录入动作统一走 `${CLAUDE_SKILL_DIR}/references/data/provider-registration.md`。探针类判据一律按 SKILL.md 证据层级执行（连接层证据先于 HTTP 层证据）。表内数值常量（重试数/超时/保留版本数等）为 3.x 时点观测，以所装版本实测为准；判据字段缺失时标注"此版本不暴露"，降级到症状级判断。

| # | 故障模式 | 典型症状 | 严重度 | 内部判据 | 处置 |
|---|---|---|---|---|---|
| 1 | 5678 端口被旧进程占用 | "装好了/启动了"但行为怪异；安装器轮询 30 秒后误报成功（假成功高发源） | 高 | 新进程日志"端口已被占用，无法启动服务"后退出；5678 应答方 `version` ≠ 安装版本目录 `package.json`（P4 识破）；`router.pid` 指向者与真实监听者不一致 | 释放端口或停旧进程（Windows `Stop-Process` 过滤 node+server.js；Linux/macOS 按 PID kill），再走平台拉起面 |
| 2 | 旧版 core 被误拉起 | Router"自己起来了"但版本旧；共享数据被旧格式改写；`router.pid` 被覆写 | 高（仅当机器上存在 Skill 形态 CLI 或旧解压包时可达） | CLI 的 `ensureRouter()` spawn 其所在包的 `scripts/router.js`，拉起方版本 = CLI 包根 `package.json` ≠ `current` | 停误拉进程（勿用该 CLI 的 stop——读同一 PID 文件可能停错对象）；核对数据完好后走平台拉起面 |
| 3 | provider key 死亡（上游 401） | 某渠道模型从可路由名单消失；对话自动换模型 | 高 | 事件 `modelDisabled`（high）："已自动禁用（401）"，备模型自动补充 | 换新 key：`POST /api/provider-key`；或 `POST /api/toggle-model` 恢复；多 key 渠道走面板 `/api/provider-keys/*` |
| 4 | 上游模型下架（404/410） | 同 #3 | 中 | 事件 `modelDisabled` | `POST /api/switch-primary` 换在售模型（先 `GET /api/models?provider=` 复制准确 ID） |
| 5 | 429 限流/额度耗尽 | 切换频繁；特定渠道持续失败 | 中 | 事件 `modelFailover`："模型层面限流（额度用尽）"；`rate-limit-state.json` 有冷却记录 | 自动恢复探测每 5 分钟；人工可加 key/加渠道 |
| 6 | 主模型故障自动切换 | 偶发换模型但结果正常 | 中 | 事件 `modelFailover`（主→备）；重试上限 maxRetry=2（共 3 次尝试） | 通常无需操作；频发时按 #3/#4 查根因 |
| 7 | 单渠道整池不可用 | 某渠道全部模型消失 | 高 | 事件 `modelUnavailable`（**critical**）"所有模型均不可用"；兜底救援成功推 `modelRescue` | 查该渠道 key 与官网状态；必要时 `POST /api/toggle-provider` 整渠道下线 |
| 8 | 所有渠道不可用 | 客户端收到 503"所有 Provider 尝试均失败"或 502 | **严重** | `GET /api/status` 的 `activeProviders=0` | 逐渠道补 key（provider-registration.md）；控制服务器可达后 `POST /api/sync-providers` 重同步 |
| 9 | 慢渠道拖垮体验 | 首字延迟高、切换偏多 | 低 | 超时档位 adaptive 自动放宽/收紧；慢渠道判死 = 3 次慢超时嫌疑 + 确认探测 | 可 `POST /api/toggle-model` 禁慢模型 |
| 10 | 粘性路由绑到慢模型 | 同一会话总命中同一慢渠道 | 低 | sticky 按 apiKey+capability 绑定上次成功 provider；选中前有慢车道与上下文窗口校验兜底 | 极端时 `POST /api/toggle-model` 禁该慢模型缓解；改 `routing.strategy` 为 `balanced` 属白名单外配置，如实告知由用户自行决定 |
| 11 | 控制服务器失联 | 渠道列表不再更新 | 中 | `GET /api/status` 的 `lastSync` 过旧 | `POST /api/sync-providers` 手动重同步 |
| 12 | 配置文件损坏 | key"丢失"、行为回默认 | 高 | Router 启动日志配置解析失败；`router-config.json.bak-*` 存在 | 停 Router → 用 `.bak` 回滚 → 平台拉起面重启（research 依据：配置写路径自动留 3 份备份） |
| 13 | Windows 配置热更新失效（OneDrive/杀软/目录改名） | 改配置不生效，"活着但聋了" | 中 | watcher 退避重建连续失败后降级为公告事件 | 收到该公告即重启 Router（平台拉起面） |
| 14 | 自动更新 drain 窗口 | 请求短暂 503"服务正在更新/重启" | 低 | drain 期间 `/v1/*` 返回 503 + `Retry-After: 5` | 等 60 秒自动恢复；勿手动杀进程 |
| 15 | 版本更新后进程未重启 | "升级了还是旧行为" | 中 | P4：`/api/status` 的 `version` ≠ `current/package.json` 版本（端点缺失时无法核实，如实标注） | 平台拉起面重启服务 |
| 16 | 畸形 Anthropic/OpenAI 请求 | 单次请求 400 | 低 | OpenAI 端点扁平 `error`，Anthropic 端点 SDK 兼容嵌套格式 | 修客户端请求；非 Router 配置问题 |
| 17 | 客户端中途断开 | 请求无声中断 | 低 | request-journal 有该请求记录、无错误事件 | 无需处置 |
| 18 | 设备未注册 | `registrationReminder` 事件"尚未注册，请运行 setup" | 低（迁移背景） | `GET /api/status` 的 `apiKeyConfigured=false` | 正常安装会自动注册；持续出现按 install/upgrade 章核对安装完整性 |
| 19 | 状态端点缺失被误判未启动 | 所装版本无 `/healthz`（或端点改名）：探针 404 被当成"未启动"，平台面重复拉起，报端口冲突 | 高 | 连接层证据：5678 对任意路径有 HTTP 应答 = 有进程监听；`/healthz` 404 ≠ 未启动（SKILL.md P2 证据层级） | 按证据层级重判；确需重启先核对 `router.pid` 再走平台拉起面 |
| 20 | 接口面不符（版本与技能知识面差异极大） | 各管理端点全 404，但 5678 有应答 | 高 | P3 替代证据链全部落空（SKILL.md 表后注）；版本号走版本证据链，最坏到"版本未知" | 写操作全部拦截；能力发现走降级；报文件版本号并转 upgrade 章核对；版本新于技能已知面时提议勘误回写 |
| 21 | 切换/请求未到达 Router | "切了没反应/没生效"，但探针全过、Router 健康 | 中 | 事件文件无对应 `switchModel` 等事件，且 request-journal 当日无该时段请求——请求根本没进来，非 Router 故障 | 转查客户端侧：baseURL 是否指向 `127.0.0.1:5678`、配置是否已保存生效（改了没重载高发）；Router 侧无需任何操作 |

高价值条目（#1 假成功、#2 误拉起、#12 明文 key 雷区）在 troubleshoot 章有展开。
