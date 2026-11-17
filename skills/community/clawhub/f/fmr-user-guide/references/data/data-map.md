# 数据文件地图与写权限阶梯

路径根：`~/.free-model-router/`（Windows `%USERPROFILE%\.free-model-router\`；环境变量 `FMR_DATA_DIR`/`FMR_ROOT_DIR` 可覆盖）。Skill 与 standalone 两种形态**共享同一数据目录**。

## 目录布局

```
~/.free-model-router/
├── data/                        # 运行数据
│   ├── router-config.json       # 主配置：server host/port/设备Key、providers（明文渠道 key）、
│   │                            #   routing、autoUpdate、moa、groups、disabledModels
│   ├── events.json              # 事件流（最近 200 条；改状态只用 mark-* 命令）
│   ├── stats.json               # 每模型调用统计（延迟/成功率/评分依据）
│   ├── model-states.json        # 每模型可用性（"模型为何不进热池"看这里）
│   ├── rate-limit-state.json    # 副本级限流冷却
│   ├── announcements.json / announcements-notified.json   # 公告缓存/已推送记录
│   ├── flush-state.json         # 遥测批量上报游标
│   ├── update-state.json        # 自动更新状态机内部文件
│   ├── install-info.json / migration-state.json / install-divergence.json
│   ├── router.pid               # Router 进程号（判活依据）
│   ├── device-id.json / fingerprints-<date>.json / error-queue.json
│   └── feedback.json            # 用户反馈本地副本
├── logs/
│   ├── monitor-error-<date>.log         # 监控错误日志
│   ├── request-journal-<date>.jsonl     # 请求明细流水（7 天/100MB 上限）——排"哪次请求走了哪个 provider、为何失败"的主战场
│   └── reasoning-content-errors.jsonl   # 默认关闭（配置 reasoningDiagnosticLogEnabled 或 FMR_REASONING_DIAG_LOG=1 才写）
├── versions/<ver>/              # 版本目录（自动更新独占管理）
├── staging/                     # 更新下载暂存（自动更新独占）
└── current                      # → versions/<ver> 指针（Windows 旧装为目录复制）
```

旧布局安装（无 `versions/`/`current`，应用目录自定）同样成立：禁区对应其应用目录整体。

## 写权限三级

**只读**：上表全部文件只读查看一律安全。排障三件套 = `data/router.pid` + `logs/request-journal-*.jsonl` + `data/events.json`。

**白名单可改**（仅这些项允许手改 `data/router-config.json`，改前必备份）：

| 字段 | 场景 | 生效方式 |
|---|---|---|
| `server.host` / `server.port` | 跨机接入（access 章） | 重启 Router（监听地址只在启动时读取） |
| `debugLog` | 调试日志开关（troubleshoot 章） | 热更新 |
| `autoUpdate.mode` | `auto`/`notify`/`disabled`（upgrade 章） | 热更新 |

改法：先回读目标字段在所装版本的配置里确实存在（解析实测确认，不以技能记载为准）——不存在或形状不符 = 知识面落后信号：停手、如实报告、提议勘误（须用户确认，维护层落账）；确认存在再 `cp router-config.json router-config.json.bak-<时间戳>` → 修改 → JSON 校验通过才算改完。Router 运行期手改出格式错误会**回落默认配置**（key"看似丢失"，实际在自动备份 `router-config.json.bak-*` 里）。**白名单之外的字段一律不代改**：有 REST/面板入口的走 REST/面板；两者都没有的如实告知用户由其自行处理。

**调整记录（2026-09-17）**：白名单原含 `routing.strategy`、`autoUpdate.mode`、`reasoningDiagnosticLogEnabled`，因配置 schema 随版本漂移、手改误伤面大（回落默认配置风险）一度全部移出；后经用户裁定 `autoUpdate.mode` 挪回（自动更新模式为用户高频诉求）。现仍移出：`routing.strategy`、`reasoningDiagnosticLogEnabled`——技能不代改，用户诉求如实转告自行处理。

**禁区**（手改即雷区）：

- `versions/`、`staging/`、`current`、`current.old`——自动更新与切换进程独占；
- `data/update-state.json`、`data/install-info.json`、`data/migration-state.json`、`data/flush-state.json`——更新/遥测内部状态，手改可卡死更新链路；
- `data/router.pid`——进程判活依据；
- `data/events.json`——并发写无锁，改事件状态只用 `mark-notified`/`mark-read`。
