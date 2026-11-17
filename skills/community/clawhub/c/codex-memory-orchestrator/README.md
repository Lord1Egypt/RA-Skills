# memory-orchestrator
**[English](./README.en.md) | [中文](./README.md)**


Codex 长对话记忆管理技能（本机原版 v1.9.4）：在用户或 Agent 显式调用、或定时扫描时统计正在执行任务的对话框轮数与实测用量，按 8 轮、15 万累计 token 等闸门给出交接建议；定时扫描不能替代每轮实时 Hook，也不会自行开新对话。技能负责恢复包、checkpoint、历史压缩（ctxcompress）和会话归档，让新对话 5 行内接续。

## 能力边界

- 只做本地记忆与交接，不上传公司数据。
- cp-memory 不可用时降级写 `$CODEX_HOME/memory/hot.md`；state/recovery 主路径不可写时自动落到 `$TMPDIR/memory-orchestrator/` 并标明 storage.mode。
- ctxcompress 是 CLI，只能 shell 调用，不注册为 MCP 工具。
- 触发词：总结 / 压缩 / 恢复 / 交接 / 开新对话 / checkpoint。
- checkpoint/压缩默认限定当前 active_project，仅处理该项目的 rollout 文件；临时产物用完即删。
- `export_ctx.py` 兼容真实 rollout 的 `payload` 包裹结构，只导出 user/assistant 交换轮（跳过 developer 指令），并按文件名/父目录/session_meta cwd 匹配项目。
- `recovery_prompt.py` 可把恢复包转成 `create_thread` 首条提示词。

## 目录结构

```
memory-orchestrator/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE.md
├── references/
│   ├── templates.md        # 恢复包模板
│   └── agent-gateways.md   # 跨 Agent 能力矩阵（deep_link/manual 降级）
└── scripts/
    ├── export_ctx.py       # rollout jsonl → messages 数组（--project 校验）
    ├── monitor_dialogs.py  # 跨对话框轮数监测（UserMessage 真实计数，默认只监测 inProgress 正在执行）
    ├── agent_hook.sh       # 用户/Agent 显式调用的轮次自检入口（只 bump，不读正文）
    ├── state.py            # 按对话框隔离的轮次计数/阈值/提前提醒/多 Agent 注册表/cross-check（不可写降级）
    ├── recovery.py         # 恢复包索引（不可写降级）
    ├── recovery_prompt.py  # 由恢复包生成 create_thread 提示词
    ├── handoff_gateway.py  # 一键新对话承接（能力矩阵降级）
    └── self_test.py        # 自检
```

## 使用前提

- 可选：本机持久 `cp-memory-mcp`（记忆库）。
- 可选：`agent-ctx-compress` 提供 `ctxcompress`；缺失时用 5-8 行手动摘要降级。
- 全局规则只负责触发路由；Codex 当前没有可验证的每轮生命周期 Hook，`agent_hook.sh` 必须由用户或 Agent 显式调用。
- 跨对话框监测依赖 Codex Home 下 `sessions/` 与 `sqlite/codex-dev.db`（Windows 自动用 `%USERPROFILE%\.codex`，可用 `--sessions-dir`/`--catalog-db` 覆盖）。定时扫描可事后巡检，但不能保证每轮检测或自动换新对话，详见 SKILL.md。

## 授权与发布

本技能源码以 MIT 协议发布。平台专用调整不回写本机原版。


## 显式自检（任意 Agent）

在宿主能可靠执行每轮 Hook 时，可把以下命令接到轮次事件；当前 Codex 没有可验证的每轮 Hook，因此只能由用户或 Agent 显式调用：

```sh
bash $CODEX_HOME/skills/memory-orchestrator/scripts/agent_hook.sh active_project=<项目名> thread_id=<对话框ID>
```

只统计轮数、不记录正文、不上传网络；阈值用 `TURN_THRESHOLD`/`TURN_WARN_AT` 覆盖（默认 8/7），提前 1 轮提醒一次。
