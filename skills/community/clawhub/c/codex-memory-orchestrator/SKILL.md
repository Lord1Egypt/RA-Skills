---
name: memory-orchestrator
slug: codex-memory-orchestrator
displayName: 对话记忆管家 · Memory Orchestrator
description: "长对话检查轮数/token，生成恢复包并交接；不改原文。触发词：上下文压缩、恢复、交接。"
version: 1.9.4
platforms: [macos, windows, linux]
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
locales: [zh-CN, en-US]
---

# memory-orchestrator

长对话记忆管理的中枢。目标是：上下文不失控、新对话 5 行内接续、关键决定不丢失。

## 安装后的接线与限制

- 本 Skill 不能在 Codex 桌面端自行获得每轮回调。实时判断依赖宿主 Skill/Agent 显式调用 `agent_hook.sh`，或由用户明确要求运行；定时扫描只能做事后巡检，不能保证每轮检测、自动生成恢复包或自动开新对话。
- 若宿主支持生命周期 hook，可把同一命令接到每轮事件；当前本机未配置可验证的每轮 hook，相关限制以本机 `$CODEX_HOME/rules/context-and-memory.md` 为准。

### 本机接线样例（可选参考）

作者本人机器上的 Codex/WorkBuddy 具体接线（LaunchAgent、heartbeat、命名空间试点等）见
`references/local-setup-notes.md`。其中 LaunchAgent 只是定时扫描，不是每轮实时钩子；新环境按宿主实际支持的方式接线，不得把定时扫描宣称为实时保护。

## 会话状态（每次会话开始/结束）

- 状态文件：`$CODEX_HOME/memory/state.json`
- 更新命令：
  ```sh
  $CODEX_HOME/skills/memory-orchestrator/scripts/state.py set active_project=<项目名> [agent=<Agent名>]
  $CODEX_HOME/skills/memory-orchestrator/scripts/state.py bump active_project=<项目名> [thread_id=<对话框ID>] [agent=<Agent名>]  # 每轮+1，可带阈值参数
  $CODEX_HOME/skills/memory-orchestrator/scripts/state.py touch agent=<Agent名>                                   # 登记本 Agent 已装 Skill 的存活标记
  $CODEX_HOME/skills/memory-orchestrator/scripts/state.py cross-check [agent=<Agent名>] --json                   # 读共享注册表，交叉提醒其他 Agent
  $CODEX_HOME/skills/memory-orchestrator/scripts/state.py get
  bash $CODEX_HOME/skills/memory-orchestrator/scripts/agent_hook.sh agent=<Agent名> active_project=<项目名> thread_id=<对话框ID>  # 显式调用统一判断
  $CODEX_HOME/skills/memory-orchestrator/scripts/memory_gate.py --thread-id <对话框ID> --active-project <项目名> --dry-run --json
  ```
- 对话轮数监测（仅在宿主显式调用或定时扫描时执行）：以该对话框真实累计轮数为准，不只数本窗口；按 `active_project||thread_id` 在 `state.json` 的 `dialogs` 字典中隔离计数；
  - 硬阈值默认 `turn_count >= 8`（SKILL/AGENTS/state 统一 8 轮，2026-10-19 确认）；可用 `--threshold N / --warn-at N` 或环境变量覆盖；
  - 累计 token 硬阈值默认 `>= 150000`（`TOKEN_THRESHOLD`，取本机实测 input+output），提前线 `>= 130000`（`TOKEN_WARN_AT`）；
  - token-usage 实测硬阈值：单请求 input 峰值 `>= 100000`、请求数 `>= 120`、单会话累计 input `>= 8000000`；
  - 互补触发：五项任一先到即判定需要交接；`memory_gate.py` 把精确轮数和三项 token-usage 指标一起传给 `state.py`，不重复造调度器；
  - 提前 1 轮提醒：当 `turn_count >= 7` 或 `token_count >= 130000` 时输出一次提醒“请准备开新对话”（本提醒只出现一次，不重复刷屏）；
  - 到任一硬阈值时判定需要交接（仅限正在执行任务）：先生成恢复包/记忆摘要，再由当前 Agent 或用户开新对话，本对话框随后归档；停止/已完成/已归档对话框不续接、不开新对话；
  - 单轮内容极大（如图纸批次 >10 张、往返文件多）时，即使未到轮数也要按里程碑先落恢复包，不只看轮数；
  - 触发依据可与 state.json 的 `turn_count` / `dialogs` 核对，缺省按本规则执行。
- 每次 checkpoint 后把 `last_checkpoint` 和 `last_action` 写回 state.json。
- state.json / recovery-index.md 主路径不可写时自动降级到 `$TMPDIR/memory-orchestrator/`（可用 `CODEX_MEMORY_STATE_FALLBACK` / `RECOVERY_INDEX_FALLBACK` 覆盖），并在输出 JSON 的 `storage` 字段标明 `primary/fallback`。
- 并发安全：`state.py` 用文件锁 + 原子写（先写临时文件再 rename），多 Agent 并行 bump 不会互相覆盖。

## 统一闸门（memory_gate.py，2026-11-05）

- 入口：`scripts/memory_gate.py`。必须由 `agent_hook.sh` 或用户显式调用；只定位文件名含目标 `thread_id` 的 rollout，并调用 `token-usage.sh --session-id <ID> --json`。
- 五项判定：轮数 `>=8`、累计 token `>=150000`、单请求 input 峰值 `>=100000`、请求数 `>=120`、单会话累计 input `>=8000000`。累计 token 口径为实测 `input + output`，`cache_read` 只作明细，不重复相加。
- `--dry-run` 只读本机 usage/state 判定，不写业务文件或 state；正常模式以精确轮数写 state，重复运行同一指标不重复提醒。
- 自测：`python3 scripts/test_memory_gate.py`，固定覆盖五条件、JSON、dry-run、幂等、精确轮数、无关 rollout 隔离和纯本地约束。

## cp-memory 工具调用清单（真实签名，2026-10-18 实测）

- 会话开始检索：`memory_recall(query=项目名或主题, intent=resume, limit=5)`；也可 `memory_search(query=..., limit=5)` / `memory_probe(entity=<项目名>)`。
- 写 checkpoint/归档：`memory_add(entity=<项目名>, property=next_step|decision|checkpoint, value=一句话, tags="checkpoint|archive", content=长文本可选)`。
- 记决策：`memory_decision_add(title, context, decision, rationale)`。
- 记当前任务：`memory_task_set(task_name=...)`；完成：`memory_task_done(result=...)`。
- 恢复上下文：`memory_restore_context(prompt=最近问题, max_chars=...)`。
- 状态核对：`memory_health()` / `memory_stats()`。
- 多项目隔离：`entity` 一律用项目名；tags 带项目名，避免串记。
- 以上工具名均来自本机 `cp-memory-mcp`（v1.30.0）`tools/list` 实测结果。

## 跨对话框轮数监测（monitor_dialogs.py）

- 只统计**正在执行任务**的对话框（`thread_turns.status=inProgress`）；停止/完成/归档的不计数、不提醒、不续接、不开新对话。
- 默认阈值：轮数 ≥8 超限、≥7 提前；token ≥150000 超限、≥130000 提前；`--days` 限定时间窗。
- 存量全量扫描（R1，安装后跑一次）：`python3 scripts/monitor_dialogs.py --all --write-state`，结果写 `state.json` 的 `index`，二次扫描不重复提醒。
- 只读会话日志与 usage 元数据，不读正文、不上网、不自动生成恢复包；发现超限由 Agent 按「恢复包」章节生成交接包。
- 路径探测、token 数据源、各平台定时接线（LaunchAgent / schtasks / crontab）与降级细节见 `references/monitor-dialogs.md`。

## 多 Agent 交叉提醒与一键新对话承接（R2）

- 共享注册表：所有已装本 Skill 的 Agent 读写同一个 `state.json`，`dialogs` 每条带 `agent`/`owner` 字段；
  进程只读他人的行、只写自己 `owner` 的行；非 codex Agent 的对话框键加 `@<agent>` 命名空间防碰撞。
- `state.py bump` 触发提醒时自动读注册表做交叉检查：列出其他 Agent 已超阈值/接近阈值的对话框，
  以及注册表中无存活标记（`agent_alive != true`）的 Agent 并提示“建议在其也安装本 Skill”。
- `state.py touch agent=<Agent名>` 登记本 Agent 的存活标记；`cross-check` 可单独触发交叉提醒。
- 一键承接：`scripts/handoff_gateway.py` 按 `references/agent-gateways.md` 能力矩阵降级——
  Codex = 在当前 Agent 获得 create_thread/fork_thread 权限并显式执行时，可注入续接文本 + `codex://threads/<id>`；否则只生成恢复包和入口提示；
  Claude = deep_link（`claude://new?text=` + 剪贴板）；无注入能力 Agent = 生成恢复包 + 复制剪贴板 + 打开目标应用。
  真实跳转写 `$CODEX_HOME/audit.log`。全程本地，不把会话内容发云端。


## Checkpoint（每 8 轮、里程碑或提前 1 轮提醒后）

1. 导出可压缩源（仅当前项目/会话，禁止默认扫全部日志）：先用 `state.py get` 确认 active_project，再用 `scripts/export_ctx.py` 指定该项目 rollout 文件转成 messages 数组；压缩前向用户说明将读取的范围与用途。

   ```sh
   export ACT="<项目标识>"                              # 必须先经 state.py get 与用户确认
   export OUT="${TMPDIR:-/tmp}/memorch-$$/chat.json"   # 私有临时目录
   mkdir -p "$(dirname "$OUT")"
   python3 $CODEX_HOME/skills/memory-orchestrator/scripts/export_ctx.py --project "$ACT" -i "$HOME/.codex/sessions/**/rollout-*.jsonl" -o "$OUT"
   ctxcompress --input "$OUT" --stats-only
   ```
   仅当前 active_project；export_ctx.py 默认拒绝全目录通配，必须显式 `--project`；兼容真实 rollout 的 `payload` 包裹结构，只导出 user/assistant 交换轮（跳过 developer 指令）；`--project` 会按文件名/父目录/session_meta.payload.cwd 匹配真实项目。临时文件用完即删，原始对话不落入长期记忆。

2. 无法获得对话转储时，按规则手写压缩摘要（5-8 行，见 `references/templates.md`）。
3. 把 checkpoint 通过 `memory_add(...tags="checkpoint")` 写入 cp-memory，并同步更新 hot.md 与 state.json。

## 压缩（ctxcompress）

- ctxcompress 是 **CLI**，只能经 shell 调用，绝不注册为 MCP 工具。
- 命令形态：

  ```sh
  export ACT="<项目标识>"                                                        # 与 state.py 的 active_project 一致，先征得用户同意
  python3 $CODEX_HOME/skills/memory-orchestrator/scripts/export_ctx.py --project "$ACT" -i "<当前项目 rollout 路径/glob>" -o "$OUT"
  ctxcompress --input "$OUT" --ratio 0.3 --format compact --output "$(dirname "$OUT")/compact.txt"
  ```

- 常用参数：`--stats-only` 看占比；`--ratio 0.3-0.5` 保守压缩；`--no-summarize` 只去重。
- 工具不可用或异常时，降级为 5-8 行手动摘要（同样限定 active_project），降级原因写进交接包，不静默假装压缩。
- 临时压缩产物用完即删（`rm -f "$OUT" "$(dirname "$OUT")/compact.txt"`），原始对话不写入长期记忆。

## 恢复包

- 命名固定：`恢复包-<项目名>-<YYYYMMDD>.md`。
- 生成后登记索引：
  ```sh
  python3 $CODEX_HOME/skills/memory-orchestrator/scripts/recovery.py --add <项目名> <恢复包路径>
  ```
- 索引文件：`$CODEX_HOME/memory/recovery-index.md`，新对话先读它定位最近恢复包。
- 生成 `create_thread` 提示词：`python3 $CODEX_HOME/skills/memory-orchestrator/scripts/recovery_prompt.py --recovery-path <恢复包.md> --project <项目> --thread-id <对话框ID> [--json]`，输出可直接作为本 app `create_thread`/`fork_thread` 的首条 user 消息。
- 模板见 `references/templates.md`；字段：会话信息、目标与已完成、关键决策与依据、下一步、未决/风险、交接对象与验证方式。

## 归档（会话结束或“总结/交接”）

1. 汇总本次目标、决定、下一步 → cp-memory（`memory_add(entity=项目名, tags="archive")` 或 `memory_decision_add`）。
2. 更新 `$CODEX_HOME/memory/hot.md` 顶部（只保留最近 1 个项目的最新状态；切换项目前先把旧项目状态写入 cp-memory 防覆盖丢失）。
3. 若需要人类可读交接文档，同时生成恢复包并登记进 `recovery-index.md`。
4. 结束前把 `turn_count`、`last_checkpoint` 写回 state.json。

## 记忆规则

- 只记结论与决策，不抄过程日志。
- 每条记忆带：主题、时间、状态（进行中/完成/归档）、下一步、责任人（默认用户）。
- 同主题用增量更新（幂等），不重复追加相似条目。
- 多项目并存：cp-memory 按 `entity`+`tags` 隔离；`hot.md` 只做“最近一个任务”的最低保底。
- 公司数据红线不变：本机与公司介质外发仍需遵守项目 AGENTS.md；本技能只做本地记忆，不把内容传云端。

## 禁忌

- 不得把 ctxcompress 当 MCP 服务器注册。
- 不得在 cp-memory 不可用时停摆：至少落到 `$CODEX_HOME/memory/hot.md`。
- 不得默认导出全目录 rollout；必须限定 active_project 并先经用户确认。
- 不得用“换新对话”替代真实交接：必须先生成恢复包/记忆摘要再提醒开新对话。
- 不得在压缩时丢弃未决问题、下一步、关键数字。
- 不得在未切换项目时整份覆盖 hot.md（先归档旧项目）。
- 不读取或替代施工日志/会议纪要等既有项目技能的作用域。

## 项目步骤自动编排（step_orchestrator.py）

- 用途：大项目拆成有序步骤，每步给开工提示词；完成一步自动开新对话框进入下一步，直到完成。
- plan 放 `$CODEX_HOME/memory/plans/`（`CODEX_MEMORY_STATE_FALLBACK` 可覆盖），字段 `project` + `steps[{id,title,prompt,verify}]`。
- 命令：`plan <plan.json> --project 项目`（幂等）→ `render [--json]` → `complete --note ... [--thread-id]` → `status`；中断后重跑 `status`/`render` 即从 `current` 续。
- 默认免逐步确认；`AUTO=0` / `APPROVAL_MODE=manual` 回到逐步确认。红线永不豁免（公司内容外发、删原始资料、未授权系统配置先询）。
- 完整参数、审计写入与接力流程见 `references/step-orchestrator.md`。
