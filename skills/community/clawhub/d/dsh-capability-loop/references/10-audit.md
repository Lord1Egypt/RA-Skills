# 10 · 审计口径（Audit）

> 原则：**只读、可复现、带证据**。审计不改任何配置、不启停服务、不安装软件；每条结论必须能指向 `文件:行号`、命令输出或目录清单。
> 工具：`scripts/capability-audit.ps1`（自动跑九组指标 + 与上次的漂移对比）；本文件定义「看什么、怎么判、报告怎么写」。

> **动态健康检测**：脚本每次把关键指标快照写到 `<工作区>\.tmp\capability-loop\audit-state.json`；下次体检自动对比（skills 增减、catalog 字符、索引大小、桌面壳补丁、检索开关、Trae 可用性、会话数），变化以 `[WARN] 变化：xxx 上次=… → 本次=…` 输出。需要周期性检查时，用 `schedule_create` 或任务计划器定时跑 `capability-audit.ps1 -Strict`（脚本本身不常驻）。

## 1. 九组指标与判定阈值

| 组 | 看什么 | 通过标准 | 常见问题 |
|---|---|---|---|
| **A 运行时** | PS 版本、Node/Python/pnpm、DSH_HOME 可读性、CLI 可用 | 与环境基线一致或已记录差异 | 裸 `npx` 命中坏 shim（用 `npx.cmd`）；`~/.dsh` 在沙箱内不可写（需审批/用户终端） |
| **B Skills** | 活动/停用数量、`SKILL.md` 缺失、description 字符数与触发词、依赖 CLI 是否可用 | 每条 description ≤200 字符（硬上限 500，超出被截断）；总字符 ≤5000；每个 skill 有显式触发词 | 「装了必阻塞」（依赖缺失）、超长 description、无触发限定抢触发、功能重复但都留着 |
| **C 角色** | `~/.dsh/agents/*.md` 角色 prompt 数量 | 至少有设计/需求/测试类角色（团队评审依赖） | 只有 skill 没角色 → spawn 时无 prompt |
| **D profile** | `cordis.patch.yml` 行数、检索三件套、token-insights/dshmarket 残留、市场数量、依赖数 | 检索为持久化+first-search+wal；已清理插件在 patch/package/storage 三处均无残留；市场只留一个 | 插入了却 `disabled: true`（装了没跑还占工具前缀）；两三个市场互相抢入口；`uninstall-blocked` |
| **E 会话记忆** | 会话数/总大小、`session-index.sqlite*` 大小与时间、`session_search` 实测 | 索引存在且 >100MB；搜索返回真实结果、无错误码 | 索引半成品（超时中断）→ 删 3 个文件重搜；`openAt: never` 说明检索被关 |
| **F 桌面壳** | `main.js` 锚点、`desktop.log` 尾部（`3/3` 判死、`EADDRINUSE`、`已启动内置服务器`） | 补丁锚点齐全；重启后 0 次 `3/3`；无失败启动日志 | 旧版 ≈23s 误杀长任务；dshmarket 自重启抢端口 |
| **G 资产与门禁** | `AGENTS.md`/`memory`/`standards`/`tools`/`upgrade` 门禁/示例项目/交接包/用户偏好 | 存在且可执行；门禁有正例+反例记录；偏好账未过期（>120 天 WARN） | 只有文档没有可执行门禁；门禁脚本没跑过；偏好记了不读 |
| **H 版本/更新** | 安装版 `version.json`、源目录版本、CHANGELOG | 安装版=源；或明确记录差异 | 源已更新但安装版未同步（用 `skill-status.ps1` 看 diff） |
| **I 漂移** | 与上次快照的指标变化 | 无未解释变化 | 死技能悄悄回来、catalog 变大、索引被删、补丁被覆盖 |

## 2. 度量口径（能算就算，不能算就说明）

- **catalog 成本**：所有活动 skill 的 `description` 字符数合计（CJK≈1 token/字，英文≈4 字符/token）。源环境：磁盘 description 合计 6,419 → 3,673 字符（−43%）；按 catalog 注入估算 21 条约 14,950 字符 → 12 条约 6k 字符（条目 −43%，字符降幅更大）。
- **固定前缀**：工具 schema + 系统提示（源环境 ≈12.2k tokens/请求，其中工具 ≈10.1k、系统 ≈2.1k）；插件/工具增减会直接改变它。
- **费用结构**：先看 `dsh-cost-meter` 账本（模型 × 缓存读写 × 输出）；诊断顺序 = 长会话重发 > 贵模型路由 > 前缀体积。
- **缓存命中**：源环境 95.96%；工具集/skill 清单变更会击穿缓存，所以**批量改**。
- **索引规模**：源环境 256 会话 ≈194MB → 索引 ≈213MB→250MB（首次建库 2–3 分钟）。

## 3. 审计技巧（避免被工具本身误导）

1. **中文乱码 ≠ 文件坏**：PS 5.1 `Get-Content` 默认按 ANSI 解码，UTF-8 中文会花屏；用 `-Encoding UTF8` 或 `[System.IO.File]::ReadAllText($p,[Text.Encoding]::UTF8)` 复核原始字节。
2. **`ConvertFrom-Json` 深度**：大配置文件/会话投影可能超默认深度，用 Node/Python 解析更稳。
3. **会话文件是多帧 zstd**：`zstdDecompressSync` 只解第一帧；按 magic `28 B5 2F FD` 逐帧解压再拼接（见 `70-playbook.md`）。
4. **日志时间戳是 UTC**：`desktop.log` 里 `[...Z]`，与本地 +8 差 8 小时，判断「重启前后」要换算。
5. **进程归属校验**：用 `Get-CimInstance Win32_Process` 的 `CommandLine` 确认是 `dsh-local` 服务器，别误杀用户其它 node 进程。
6. **只读也不等于零风险**：`--dump-config` 等命令可能写 `~/.dsh`（沙箱 EPERM），先查文档再跑。

## 4. 报告结构（落盘 `<ws>/.tmp/capability-audit-<时间>.md`）

```markdown
# DSH 能力体检 — <日期>
## 0. 结论（3–5 条，按收益/风险排序）
## 1. 指标总览（A–I 九组，PASS/WARN/FAIL 计数 + 漂移摘要）
## 2. 明细（每组：项 / 实测值 / 判定 / 证据）
## 3. 风险清单（P0/P1/P2 + 影响 + 建议动作 + 回滚点）
## 4. 不建议做的事（只读结论，避免过度优化）
## 5. 下一步（一次只选 1–3 项，写明验证方式）
```

## 5. 审计完成的判定

- 九组都有实测值（不能是「应该是/大概」）；
- 每个 FAIL/WARN 都有证据与建议动作；漂移变化都有解释或进待办；
- 明确指出「本次审计未修改任何配置」（或如果修改了，另开 `20-runtime-fix.md` 流程并记录备份路径）；
- 报告可被第二个人按同样命令复现（命令 + 参数 + 环境差异写清）。
