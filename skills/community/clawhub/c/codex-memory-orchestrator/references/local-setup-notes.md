# 作者本机接线记录（非通用安装内容）

> 本文件是 v1.9.1 及以前写在 SKILL.md 正文里的本机运维笔记，v1.9.2 起移到 references/，避免主 SKILL 每次加载都带无关的机器细节。新装用户无需照做，按 SKILL.md 的通用接线说明即可。

### 本机接线现状（Codex）
- 现状：全局常驻规则只保留触发路由，不再复制 8 轮/15 万 token 阈值；`agent_hook.sh` 需用户或 Agent 显式调用，不能把“写进 AGENTS”当作自动执行。
- Codex 实参示例：`bash $CODEX_HOME/skills/memory-orchestrator/scripts/agent_hook.sh agent=codex active_project=<项目标识> thread_id=<对话框ID>`。
- 兜底现状（2026-11-05 复核）：LaunchAgent `com.lis.memory-orchestrator` 每小时运行一次 `monitor_dialogs.py --all --write-state`，只做扫描和提醒；它不是每轮实时 Hook，也不会自行生成恢复包或开新对话。日志写 `~/Library/Logs/memory-orchestrator.out.log` / `.err.log`。
- 显式自检钩子（纯本地、哑调用；不是自动每轮 Hook）：
  ```sh
  bash $CODEX_HOME/skills/memory-orchestrator/scripts/agent_hook.sh agent=<Agent名> active_project=<项目名> thread_id=<对话框ID>
  # 或 MEMORY_AGENT=<Agent名>。阈值可用环境变量覆盖：TURN_THRESHOLD / TURN_WARN_AT（默认 8 / 7）；
  # TOKEN_THRESHOLD / TOKEN_WARN_AT（默认 150000 / 130000）。
  ```
- 钩子做的事情 = 一次 `state.py bump`：只把“项目名 + 对话框标识 + 轮数 + 是否已提醒”写进 `state.json`，**绝不写入任何对话文本/摘要/正文**。
- state.json 是唯一本地计数文件；脚本没有 socket/requests/urllib/http 调用，不连网络、不上云、不推远端 git。发布版同样不包含任何上报逻辑。
- 每个对话框按 `active_project||thread_id` 独立计数、独立提醒，多 Agent/多对话框互不串号。
- 阈值与提前提醒（默认可覆盖）：
  - 轮数硬阈值默认 `>= 8`（SKILL/state 统一 8 轮，2026-10-19 确认；全局 AGENTS 不再复制阈值）；提前 1 轮 `>= 7`；
  - token 硬阈值默认 `>= 150000`（2026-10-20 加，`TOKEN_THRESHOLD`），提前线 `>= 130000`（`TOKEN_WARN_AT`）；
  - 互补触发：轮数或 token 哪个先到就先触发（warning/over 只按先到者报，另一维度达到时再报）；
  - 提前提醒：达到提前线（7 轮或 13 万 token）时输出一次提醒（每对话框只出现一次，不刷屏）；
  - 到 `>= 8` 强制提醒：先生成恢复包，再引导开新对话；
  - **交接建议（互补，先到先判定，仅限正在执行任务）**：轮数 `>= 8` 或 token `>= 150000` 哪个先达到，显式调用或 Agent 主动执行时先落恢复包/记忆摘要（checkpoint），再用 `create_thread`/`fork_thread` 开新对话（用 `recovery_prompt.py` 生成首条 user 消息）完成接力，本对话框随后归档收尾；不能 `create_thread` 时降级为 `handoff_gateway.py` 深层链接/复制剪贴板并提醒用户。定时扫描本身不会自动开新对话；停止/已完成/已归档对话框不做续接。
- 兜底（显式钩子遗漏时）：`monitor_dialogs.py` 定时扫描会话目录做真实轮数复核；两者互补，但定时扫描仍不是实时保护。

### WorkBuddy 跨 Agent 接线（本机试点，2026-10-20）
- 试点对象：本机 WorkBuddy（`~/.workbuddy/workbuddy.db`，`mode=ro` 只读 `sessions`/`session_usage` 轮次与用量元数据，不读任何会话正文；实测当前含 3 个 session 的 token 用量，无独立轮数字段）。
- 共享计数：Codex/WorkBuddy 跨 Agent 状态统一写 `$CODEX_HOME/memory/state.json` 的 `dialogs`；WorkBuddy 侧使用 `@workbuddy` 命名空间（即 `agent=workbuddy`）登记，只写对话框标识/项目名/轮次/提醒标记，不写正文。
- 交叉核对：codex 侧 `state.py cross-check [agent=codex|workbuddy...] --json` 可列示其他 Agent 的超阈值/接近阈值对话框；临时模拟验证 workbuddy `turn_count=9 → over` 链路通过（真实 state 未伪造轮数）。
- 真实轮数边界：当前 db 无轮数列，真实轮数须由 WorkBuddy 发出端每轮调用 `agent_hook.sh agent=workbuddy active_project=<项目> thread_id=<会话ID>` 登记后才可得；未登记前不得伪造轮数数据。
