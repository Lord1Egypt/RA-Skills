# Claude Code Hooks 配置笔记

- 文档：https://docs.claude.com/en/docs/claude-code/hooks
- 配置位置：`.claude/settings.json`（项目级）或 `~/.claude/settings.json`（用户级）
- 事件名（PascalCase）：`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStart`, `SubagentStop`
- Hook 脚本接收 camelCase JSON via stdin：`session_id`, `transcript_path`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`
- **阻断决策**：stdout 输出 `{"decision": "block", "reason": "..."}`（PreToolUse / Stop）
- **上下文注入**：
  - SessionStart：stdout 纯文本即可
  - PreToolUse：`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "..."}, "decision": "approve"}`
- 退出码：正常 0；不要用 `process.exit(2)`（会触发 unrecoverable error）

## Windows 环境

- bash.exe 在某些终端下会弹控制台窗口 → 用 Node.js 脚本 + `child_process.spawnSync` / `execSync` 时传 `windowsHide: true`
- 路径用 `path.resolve(__dirname, ...)` 不用相对路径
- `~` 用 `os.homedir()` 解析

## `stop_hook_active` 守卫

- Stop hook 在阻断后会重试，可能进入死循环
- 所有 Stop / SubagentStop hook 必须检查 `data.stop_hook_active`，若为 true 则直接 exit 0 不输出
