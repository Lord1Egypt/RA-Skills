# 案例：一次完整的 Agent 瘦身（WorkBuddy，2026-11-17）

这是一份**已验证案例**，不是使用前提。方法本身与 Agent 无关，见 `references/generic-playbook.md`；本文只说明"落到实处时长什么样"：一个真实 Agent 的目录长什么样、动过哪些块、每块省了多少、哪里会卡住。

之所以保留具体宿主名，是因为差异本身就是证据：同一套方法在不同 Agent 上，可自动化的比例不同，但手法和验收口径一致。换一个 Agent 时，把它当参照物，而不是当模板。

阅读顺序：先看第 2 节（动过什么）和第 3 节（省了多少），需要落地时再看第 1 节（结构差异）和第 4 节（哪里做不到）。

## 1. 结构差异

同一套方法，两个 Agent 的落点完全不同。下表是实测对照，可用来判断"某个 Agent 属于哪一类"：

### 1.1 目录布局

| 语义 | Codex | WorkBuddy | 备注 |
|---|---|---|---|
| 常驻身份 | `AGENTS.md` | `SOUL.md` + `IDENTITY.md` + `USER.md` + `BOOTSTRAP.md` | 无 `AGENTS.md`，`AGENTS_MISSING` 是误报 |
| 会话 | `sessions/`、`archived_sessions/` | `workspace/sessions/` | 一级目录名不同，硬编码 `sessions/` 会漏 1.3 GB |
| 日志 | `logs/` | `logs/` + `traces/` | 两者都要进 Cold，否则漏 469 MB |
| 记忆 | `memories/memory_summary.md` | `user-<uid>-personal/MEMORY.md` + `.workbuddy/memory/` | `MEMORY_SUMMARY_MISSING` 是误报 |
| 规则索引 | `rules/index.md` | 无该机制 | `RULES_INDEX_MISSING` 是误报 |
| 备份 | `backups/` | 无根目录；改写前存 `.modify_backup_meta/` 映射 | 决定了 apply 准入差异，见 1.2 |
| 插件 | `plugins/` | `plugins/` + `plugins/cache/` + 4 份注册表 | 注册表分散，见 1.3 |
| 不纳入账本 | — | `projects/`（对话历史）、`binaries/`（运行时）、`blobs/`、`app/` | 在 `limitations` 里写明原因，不静默忽略 |

### 1.2 三个断点（为什么同一份脚本在 WorkBuddy 上会 blocked）

| 断点 | 位置 | Codex | WorkBuddy |
|---|---|---|---|
| ① 宿主探测 | `agent_slim_adapter.py` `probe_codex_home` | 命中 `config.toml`/`sessions/` | 均不符，会误判为 codex |
| ② 冷层账本 | `agent_slim.py` `add_disk_inventory` 硬编码目录名 | 命中 5/6 | 命中 2/6，约 1.7 GB 在账本外 |
| ③ apply 准入 | `agent_slim_workflow.py` `_ready_actions` | 3 个 ready | 0 个 ready |

第 ③ 点是决定性的。Codex 的 ready 全部来自 `quarantine-redundant-backup`——`$CODEX_HOME/backups/` 里字节相同的重复备份，靠哈希自证即可免确认。**WorkBuddy 没有 `backups/` 根，这条通道不存在**，所以永远只出 `pending-confirmation`，必须 `--confirm` 逐项放行。这是宿主事实，不是缺陷；不要为了凑 ready 去放宽准入门槛。

第四个缺陷两边都中：`stable_slug()` 用 `[^a-z0-9]+` 生成 id，中文被整体剔除，同目录中文文件塌成同一 id（WorkBuddy 228→169，丢 59；Codex 278→217，丢 61）。后果是暖层候选 targetId 重复、`--confirm` 传正确路径也匹配不上。修法是正则保留 CJK 区间，纯 ASCII 路径生成的 id 保持逐字不变。

### 1.3 其他宿主事实

- `token_usage_read` 恒为 `unknown`：没有 `token-usage.sh`，也没有计费读数。任何 Token 数字只能是静态字符估算（字符数 × 0.6），必须标注非实测。
- `skill_usage_index` 恒为 `unknown`：没有 `skills/.usage.json`。要判断"低频"，只能用会话 jsonl 里的 `DeferExecuteTool` / `Skill` 调用做代理统计，并在报告里写明是代理口径。
- 插件注册表有 4 处，删目录必须同步：`plugins/known_marketplaces.json`、`plugins/installed_plugins.json`、`plugins/configured-plugins.json`、`settings.json` 的 `enabledPlugins`。市场 `autoUpdate: true` 时只删目录会被自动拉回。
- 平台内置连接器（`agent-mail`、`genie-baas`、`ima-mcp`、`sheetagent` 等）不在 `enabledPlugins` 里，改配置文件不生效，只能在「设置 > 连接器」关闭。
- 服务端注入的 `<memory>` 块本地没有对应文件，不可编辑；其中的空 `[unknown]` 条目只能去 App 记忆设置清。
- 技能里可能有 `vendor` 软链指向 `$CODEX_HOME/skills/...`（跨宿主依赖）。移动或打包前先 `du`/`readlink` 确认真实占用，别把软链当成内容，也别让 WorkBuddy 侧删掉 Codex 侧的数据。
- 重名技能（同 `name`，如 `xxx` 与 `xxx__skillhub`）会重复注入清单、扰乱候选 targetId，是 Hot 层最值得先清的一项。

## 2. 七个阶段（通用流程的落地版本）

### W0 宿主确认

```sh
python3 scripts/agent_slim.py host --home ~/.workbuddy --output host.json
```

确认 `host=workbuddy`。若报成别的宿主，有两条路：修适配器分支，或者直接写一份 `layout.json` 声明（推荐后者——这是通用做法）：

```json
{
  "host": "workbuddy",
  "hot": [
    {"path": "<user-profile>/SOUL.md", "category": "instructions"},
    {"path": "<user-profile>/IDENTITY.md", "category": "instructions"},
    {"path": "<user-profile>/USER.md", "category": "instructions"},
    {"path": "<user-profile>/BOOTSTRAP.md", "category": "instructions"},
    {"path": "<user-profile>/MEMORY.md", "category": "memory", "loadedWhen": "startup-memory-summary"}
  ],
  "skillRoots": ["skills"],
  "sessionRoots": ["workspace/sessions"],
  "logRoots": ["logs", "traces"]
}
```

```sh
python3 scripts/agent_slim.py audit --home ~/.workbuddy --layout ~/.workbuddy.layout.json --json --output audit.json
```

实测差别显著：不写 layout 时 Hot 只有 23 条、估算 2,971 tok，因为 `SOUL/MEMORY` 那类文件不在任何厂商默认路径里；写了对的 layout 后 Hot 28 条、5,483 tok，才第一次看见真实的每轮常驻。**基线不准，后面所有百分比都是错的。**

同时 `du -sh ~/.workbuddy/*` 留一份真实占用，用来核对账本覆盖率。

### W1 基线

- 整包备份待改技能目录与配置（`tar.gz` + SHA-256）。
- 技能清单快照 + 全量文件 SHA-256，作为"没改内容"的证据。
- 用量代理统计：扫会话 jsonl，统计每个技能/MCP 工具的调用次数与时间窗，明确标注是代理口径。

### W2 分级

按 `audit` 结果把候选分到 Hot / Warm / Cold，标注 R1/R2、证据标签、加载条件。WorkBuddy 的典型分布：Hot 二十余条、Warm 两百余条（其中大量是 `packs` 子项与 `references`）、Cold 三到五类目录。

### W3 Hot 层（每轮常驻）

顺序按收益从大到小，每项改完单独记账：

1. **记忆文件**：原文逐字存到不注入的归档目录（`memory-library/` 之类），常驻文件只留结论 + 一行指针。事实不能丢，丢的是重复叙述。
2. **重名技能**：移出并打包隔离，消除清单重复与 targetId 冲突。
3. **`SOUL.md`**：删模板说教与重复段落，保留核心原则、边界、语气。
4. **`IDENTITY.md` / `USER.md`**：只删括号里的引导句与结尾说教，字段结构保留。
5. **技能 `description`**：只压最长的前几个，**触发词必须全留**——描述是路由依据，压掉触发词等于改能力。
6. **清单子项**：同一技能下重复的 `packs` 条目去重。

`BOOTSTRAP.md` 若无替代流程不要删；命名流程没走完时它仍承担引导职责。

### W4 Warm 层

- 单个大文件改路由拆分（正文 → 按需参考），只有"确实不再被加载"的部分才计 Token 收益。
- 同源重复目录（`xxx` 与 `xxx__skillhub`）只保留一份，另一份进隔离区。
- `unreferenced` 判定偏严是常态：目录树里罗列文件名不算读取边。别为了降低候选数去放宽引用图。

### W5 MCP 与插件层

这是 WorkBuddy 上 Hot 层的最大单项，Codex 首版流程里没有。

1. **先分清真注入与缓存**：`mcp-tool-list.json` 里可能几百个工具，其中大半属于未连接的 server，不进上下文。只统计真正注入的部分。
2. **按调用频次裁剪工具集**：GitHub 远程 MCP 支持 `X-MCP-Toolsets` / `X-MCP-Tools` header 限制暴露面，实测 46→21 工具。裁剪后必须对端点做一次 `initialize` + `tools/list` 验证，不能只看配置文件。
3. **插件缓存**：被新版本替代的旧版本、已 `enabled=false` 的市场包可以清；清之前先读注册表确认无引用，清之后同步 4 处注册记录。
4. **凭据**：`mcp.json` 权限收到 `600`。任何排查都不要把含 token 的文件整份打印到输出里。

### W6 验证与回滚

五类证据全过才算完成：frontmatter 闭合、引用完整、SHA 未变、审计复跑状态不退化、`apply → verify → restore` 闭环哈希一致。

复跑 `audit` 时若 warning 属于布局误报（`AGENTS_MISSING` / `MEMORY_SUMMARY_MISSING` / `RULES_INDEX_MISSING`），在报告里逐条写明是误报及原因，不要静默忽略，也不要为了消 warning 去造假文件。

## 3. 收益口径（2026-11-17 实测）

| 维度 | 前 | 后 | 变化 |
|---|---|---|---|
| Hot 常驻（静态估算） | 11,699 tok/轮 | 5,875 tok/轮 | -50% |
| MCP 注入工具 | 132 个 / 2,741 tok | 107 个 / 2,255 tok | -486 tok |
| 磁盘总量 | 6,063 MB | 4,095 MB | -32.5% |
| 其中 logs | 676 MB | 35 MB | -95% |
| 其中 traces | 473 MB | 115 MB | -76% |
| 其中 workspace | 1,331 MB | 351 MB | -74% |
| 插件缓存 | 233 MB | 80 MB | -153 MB |

磁盘与 Token 分栏记账，不互相冒充。静态估算不得写成账单实测。

## 4. 宿主做不到的事

- 没有 `backups/` 根 → 无免确认自动通道，全部逐项 `--confirm`。接受它，或另建等价备份根后再说。
- 无计费读数、无技能使用索引 → 两个能力恒 `unknown`，所有"低频"结论只能是代理证据。
- 服务端记忆块本地不可改 → 空条目只能去 App 设置清。
- 内置连接器工具只能 UI 关闭 → 报告里标"待人工"，不要写"已优化"。
- 插件市场 `autoUpdate` → 只删目录等于没删。

## 5. 回滚清单

按这个顺序留，缺一项就别动：

1. 待改技能/配置的整包 `tar.gz` + SHA-256。
2. 单文件级 `.bak`（记忆文件、`mcp.json`）。
3. 4 份插件注册表原文（`registry-backup/`）。
4. 被移动内容的原始路径映射表（`原始路径映射.tsv`），隔离区包内保留相对路径。
5. 删除清单（`deleted-manifest.tsv`），逐行写路径、字节、依据。

## 6. 复用检查表

- [ ] `host` 报 `workbuddy`，账本覆盖率与 `du` 对得上
- [ ] 中文路径的 targetId 唯一，`--confirm` 能匹配
- [ ] Hot 每一项改动都有 before/after 字符数与回滚位置
- [ ] 技能 `description` 压缩后触发词逐个核对未丢
- [ ] MCP 裁剪后对端点做过 `tools/list` 实测
- [ ] 插件目录与 4 处注册表状态一致
- [ ] `apply → verify → restore` SHA 闭环通过
- [ ] 报告里区分"实测"与"估算"，磁盘与 Token 分栏
