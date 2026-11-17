# 跨对话框轮数监测（monitor_dialogs.py）

原 SKILL.md 章节，按需查阅。

## 跨对话框轮数监测（monitor_dialogs.py）

- 脚本：`scripts/monitor_dialogs.py`；纯 stdlib（Python 3.9+ / Windows 兼容），要求 Python 能 read 会话目录。
- **只监测正在执行任务的对话框**（2026-10-20 定）：默认仅统计 `thread_turns.status=inProgress`（App 本地 db `thread_history_1.sqlite`）；停止/已完成/已归档对话框不计数、不提醒、不续接、不开新对话。可用 `--no-active-only` 关闭过滤（不推荐）。
- 跨平台路径（自动探测，可用 CLI 覆盖）：
  - Codex Home：`$CODEX_HOME`/`$OPENAI_CODEX_HOME` 生效，否则 `$CODEX_HOME`（macOS/Linux）或 `%USERPROFILE%\.codex`（Windows，`Path.home()` 自动处理）。
  - 会话目录默认 `<Codex Home>/sessions`；可用 `--sessions-dir` 覆盖（如 Windows 安装到其他位置时显式传入）。
  - 项目/标题元数据默认 `<Codex Home>/sqlite/codex-dev.db`；可用 `--catalog-db` 覆盖。数据库不可用时降级为仅报告 rollout 文件名/目录。
- 数据来源：优先统计 `rollout-*.jsonl` 中 `response_item` 的 `message/user`，兼容 `event_msg/item_completed` 且 `item.type == "UserMessage"`；按消息/turn id 去重。`--thread-id` 可限定只读目标 rollout。
- 默认阈值：轮数 `>=8` 超限、提前 `>=7`；token `>=150000` 超限、提前 `>=130000`；可 `--threshold/--warn-at/--token-threshold/--token-warn-at` 覆盖；`--days` 只扫描最近 N 天。
- token 数据源：rollout 内 `token_usage_record.payload.(thread_)token_usage.total_tokens`（兜底 `event_msg.info.total_token_usage.total_tokens`），取该对话累计最大真实 usage；只读元数据不读正文。
- 运行 `--write-state` 会把扫描快照写入 state.json 的 `index`（兼容原有 active_project/turn_count）。
- 只读会话日志、不自动生成恢复包；发现超限**正在执行**对话框时应按“恢复包”章节为该对话框生成交接包并引导开新对话；停止/已归档对话框不续接、不生成续接对话框。
- 安装后可用的定时巡检接线（只做扫描，不等于每轮实时钩子）：
  - macOS 桌面 Codex：可建 heartbeat/cron 自动化运行 `python3 <skill>/scripts/monitor_dialogs.py --days 3 --write-state --json`，仅在状态变化时汇报。本机 2026-11-05 可核实的是 LaunchAgent `com.lis.memory-orchestrator` RunAtLoad/3600s 定时扫描；它不会自动生成恢复包或开新对话。
  - Windows：任务计划程序创建每日任务（`schtasks /create /tn "MemoryOrchestratorMonitor" /sc daily /st 09:30 /tr "python <skill路径>\scripts\monitor_dialogs.py --days 14 --write-state"`），系统用户登录即开始。
  - Linux/WSL：`crontab -e` 加 `30 9 * * * python3 <skill-path>/scripts/monitor_dialogs.py --days 30 --write-state`。
  - 无法注册系统定时任务的受限环境：把“打开新会话时运行一次 monitor_dialogs.py”写进该环境 AGENTS.md，作为降级触发。
- 存量全量检测（R1）：安装完成即运行一次
  ```sh
  python3 $CODEX_HOME/skills/memory-orchestrator/scripts/monitor_dialogs.py --all --write-state
  # --all 关闭时间过滤全量扫历史，与 --days 互斥；结果写 state.json.index：last_full_scan / scanned_files / 每会话 over_warned
  # 同一对话框提醒后写入 over_warned_ids，二次扫描不重复刷屏
  ```
- 本脚本负责存量/跨对话框巡检；当前对话框的统一判定由 `memory_gate.py` / `agent_hook.sh` 在用户或 Agent 显式调用时执行，不能靠定时扫描冒充实时监测。

