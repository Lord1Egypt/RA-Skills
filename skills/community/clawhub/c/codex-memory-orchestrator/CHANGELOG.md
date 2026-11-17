# Changelog

## 1.9.3 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：16,953 B → 13,673 B（-19.3%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


## 1.9.4 (2026-11-05)

**把记忆闸门收回本 Skill，并停止宣称不存在的能力。**

- 全局 `AGENTS.md`/rules 不再复制 8 轮、15 万 token 等阈值；本 Skill 仍是阈值、恢复包和交接流程的唯一维护处。
- 明确 Codex 当前没有可验证的每轮生命周期 Hook：`agent_hook.sh` 需要用户或 Agent 显式调用，LaunchAgent 每小时扫描只做事后巡检，不会自动生成恢复包或开新对话。
- README/English README 同步改为“显式调用或定时扫描”，删除“自动实时监测/自动换新对话”的误导性表述。

## 1.9.2 (2026-10-28)

**去机器耦合：换一台机器也能跑通自检与编排。**

- `self_test.py` 改三态判定（PASS / FAIL / SKIP）：新增 `SkipTest` 异常与 `check(..., requires=...)`，7 处只在本机才成立的项目（HOT/AGENTS/CONFIG/protect 脚本/CTX/CPM 数值）在环境不满足时记 SKIP 而非 FAIL；输出 `ALL PASS (N 项执行，M 项跳过：…)`。
- `p_config` 可移植化：只断言 `cp-memory` MCP 已注册，`config.toml` 里的具体数值仅在 `STRICT_LOCAL=1` 时校验；未注册时跳过而不是报错。
- `step_orchestrator.py` 默认档位改为 **manual**（手动逐次确认）：仅 `AUTO=1` 或 `APPROVAL_MODE=auto` 显式开启免确认；`render` 在 manual 下输出 `MANUAL_NOTE` 提醒首次授权，auto 下仍输出 PREAPPROVAL。红线不变。
- `handoff_gateway.py` 深链保护：恢复包超过 7500 字符时跳过 deep link，改为提示用剪贴板内容手动粘贴（避免超长 URL 在浏览器/剪贴板被截断）。
- 死代码清理：`state.py` 移除 `if args.json or True:` 恒真分支的不可达 else；`handoff_gateway.py` 移除 `and not args.dry_run: pass` 空分支。
- 新增 Windows 包装器 `scripts/state.cmd`、`scripts/monitor_dialogs.cmd`、`scripts/step_orchestrator.cmd`（CRLF + 纯 ASCII 转发器）。
- `SKILL.md` 214 → 189 行：把「本机已落地接线（Codex）」整块移入 `references/local-setup-notes.md`，原位留 5 行指针；技能正文不再混入单机配置细节。

## 1.9.1 (2026-10-21)
- 三平台对齐（cross-platform + i18n overseas）：README.en.md、`--lang en|zh` 主入口、i18n.py、CFI 三平台 workflow 全绿。
- 不改变业务算法/中文模板；平台专用调整只改发布副本。

## 1.9.0（2026-10-20）

- 监测范围收紧：`monitor_dialogs.py` 默认只监测**正在执行任务**的对话框（读 App 本地 `thread_history_1.sqlite` 的 `thread_turns.status=inProgress`）。
- 停止/已完成/已归档对话框：不计数、不提醒、不自动续接、不开新对话框；仅保留恢复包归档，不再为停止对话批量创建续接线程。
- heartbeat 自动化 `memoryorchestrator` 提示词同步为“只监测正在执行任务”；`--no-active-only` 可显式关闭过滤（不推荐）。
- 文档同步：SKILL.md / README / CHANGELOG 版本与行为说明对齐。

## 1.8.0（2026-10-20）

- 步骤编排默认改为免逐步确认：调用“对话记忆管家做步骤编排”即 auto，新对话框按开工提示词直接执行、不逐次弹授权；`render` 文本/JSON 输出携带“本步已获用户预授权”声明，`complete` 后自动渲染下一步直接接力。
- 保留手动档：`AUTO=0` / `APPROVAL_MODE=manual` 回到逐次确认；红线（公司数据上云/Git远端、删除原始资料、未授权系统配置改动）即使 auto 也不豁免。
- 修复 `render --json` 被 auto 提示行污染导致无法解析的问题，改为纯 JSON 输出。
- 发布脱敏：移除 self_test.py 中的私有本机路径（/System/Volumes/Data），改为通用不可写演示路径。

## 1.7.0（2026-10-20）

- 新增自动换新对话：与轮数阈值 8/7 互补，token 硬阈值 `>=150000`（提前线 `>=130000`）哪个先到先触发；达到即本对话框先生成恢复包/记忆摘要，再 `create_thread`/`fork_thread` 开新对话，本对话框随后归档；无 create_thread 能力时经 handoff_gateway 降级。
- `state.py bump` 支持 `token_count=` 一并判定并输出 over_tokens/warn_tokens；`monitor_dialogs.py` 扫描 token 与轮数互补；SKILL.md 与全局 AGENTS.md 同步写入同一规则。

## 1.6.0（2026-10-19）

- 接线落地：实时钩子固化进 Codex 全局 `$CODEX_HOME/AGENTS.md`「长对话记忆管理」第 8 条（每轮 `agent_hook.sh`），新对话自动生效；新增 heartbeat 自动化 `memoryorchestrator` 作为兜底监测（每小时 `monitor_dialogs.py --write-state`，新超阈值才通知）。
- 本机实测通过：阈值 7 轮提前提醒、8 轮强制提醒、state 按 `active_project||thread_id` 隔离、monitor 检测、export_ctx→ctxcompress、recovery 登记全链路跑通；self_test 22 项 PASS。
## 1.5.0（2026-10-19）

- R3 export_ctx 真实 rollout 兼容：兼容 `response_item.payload.type == "message"` 的 App 真实结构，只导出 user/assistant 交换轮（跳过 developer 指令）；`--project` 除文件名/父目录外，还会按 `session_meta.payload.cwd` 匹配真实项目，避免“文件名只有 thread id 导致导出为空”。
- R3 recovery_prompt：新增 `scripts/recovery_prompt.py`，由恢复包生成 create_thread 提示词（可直接作为本 app `create_thread`/`fork_thread` 首条 user 消息），支持 `--json`。
- R3 不可写降级：state.py / recovery.py 主路径不可写时自动落到 `$TMPDIR/memory-orchestrator/`，输出 JSON 的 `storage` 字段标明 primary/fallback；可用 `CODEX_MEMORY_STATE_FALLBACK` / `RECOVERY_INDEX_FALLBACK` 覆盖。
- 阈值统一：SKILL.md 与 AGENTS.md 全局阈值统一为 8 轮（移除“12 轮”旧文案）；写权限按项目规则走审批。
- config：`$CODEX_HOME/config.toml` 补 `[mcp_servers.cp-memory]`（指向本机 cp-memory-mcp），自检保留严格检查。
- self_test 新增：真实 rollout export、recovery_prompt、state/recovery 不可写降级；AGENTS 检查改为 8 轮。

## 1.4.0（2026-10-19）

- R1 存量全量检测：`monitor_dialogs.py` 新增 `--all`（与 `--days` 互斥），全量扫历史；`--write-state` 写入 `index.last_full_scan / scanned_files / over_warned_ids / 每会话 over_warned`，同一对话框提醒后二次扫描不再重复刷屏。
- R2 多 Agent 共享注册表：`state.py` 每条 dialog 记录增加 `agent/owner`，非 codex Agent 用 `@<agent>` 键命名空间；新增 `touch`（登记存活标记）与 `cross-check`（读共享注册表，列出其他 Agent 超阈值/接近阈值对话框并建议在无存活标记的 Agent 安装本 Skill）；`bump` 触发提醒时自动带交叉检查。
- R2 一键承接：新增 `scripts/handoff_gateway.py`（按 `references/agent-gateways.md` 能力矩阵：Codex=full_auto、Claude=deep_link、其他=生成恢复包+剪贴板+打开目标应用；真实跨 Agent 跳转写 `$CODEX_HOME/audit.log`；全程本地不联网）。
- `agent_hook.sh` 支持 `MEMORY_AGENT`/`agent=` 传 Agent 名。
- `self_test.py` 新增 R1/R2/handoff 自检；SKILL.md/README/CHANGELOG 同步说明。

## 1.3.0（2026-10-19）

- 新增 `agent_hook.sh`：任意 Agent 每轮实时自检钩子，只 bump 轮数，不读取/不记录正文。
- `state.py` 按 `active_project||thread_id` 隔离多对话框计数；支持 `--threshold/--warn-at` 与环境变量；提前 1 轮提醒且每对话框只提醒一次；文件锁 + 原子写防并发覆盖。
- SKILL.md 增加「安装后自动检测」章节与隐私/联网红线说明；README 同步。

# Changelog

## v1.2.0 (2026-10-18)

- 跨平台化：monitor_dialogs.py 自动探测 Codex Home（$CODEX_HOME / $CODEX_HOME / %USERPROFILE%\.codex），新增 `--sessions-dir`/`--catalog-db`；SKILL 记录 macOS 自动化、Windows 任务计划程序、Linux crontab 三种“安装后自动开始”方式。

- 新增 `scripts/monitor_dialogs.py`：跨对话框自动监测，按 rollout 中 `UserMessage` 真实计数，映射 `local_thread_catalog` 的项目与标题；`--write-state` 写入 state.json.index。
- 修复 `self_test.py` 在 Python 3.9（无 tomllib）崩溃：增加 TOML 降级解析；新增 monitor_dialogs 自检（13 项）。
- 修复 `_mcp_lines` 文本模式缓冲导致 cp-memory 自检挂起：改为二进制无缓冲。
- SKILL.md 增加“跨对话框轮数监测”章节，README 更新结构性说明。

## v1.1.4 (2026-10-18)

- 对话轮数监测改为自动执行：按真实累计轮数，默认硬阈值 8 轮；提前 1 轮（>=7）提醒一次；>=8 强制生成恢复包并引导开新对话；单轮内容极大（如图纸批次>10 张或往返文件多）时按里程碑先落恢复包。
- README / references/templates 阈值同步到 8/7 轮；平台与 GitHub 版本统一到 1.1.4。

## v1.1.3 (2026-10-18)
- SKillHub 平台展示：中文名「对话记忆管家 / Memory Orchestrator」+ 第一版蓝图风系列图标（平台专用，不回写本机）。
- 本机原版与平台版本号统一到 1.1.3；功能保持一致。

## v1.1.2 (2026-10-18)

- export_ctx.py 增加 `--project` 校验，默认拒绝 `**/*.jsonl` 全目录通配；示例改为项目限定 + 私有临时目录 + 用后清理。

## v1.1.1 (2026-10-18)

- 限制 checkpoint/压缩默认范围到当前 active_project，仅导出当前项目 rollout；压缩前需用户确认读取范围。
- 明确不持久化对话原文，/tmp 临时产物用完即删，避免跨项目隐私风险。

## v1.1.0 (2026-10-18)

- 新增自检 `scripts/self_test.py`，12 项全覆盖：结构、模板、降级线、AGENTS 注入、config 数值、protect 对齐、ctxcompress 真实运行、cp-memory 初始化与写读清闭环、export_ctx、state、recovery index。
- README / CHANGELOG / LICENSE 补齐。
