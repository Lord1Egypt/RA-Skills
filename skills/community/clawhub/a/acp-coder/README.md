# acp-coder

OpenClaw skill，把代码任务委派给外部 coding agent（Claude Code、Codex 等）执行。简单任务单 agent 直接干，复杂任务自动拆解为多阶段多 agent 协作。

## 安装

```bash
./setup.sh
```

脚本会自动：
- 扫描本地已装的 coding agent，生成白名单
- 安装 codex-acp 平台二进制（如检测到 codex）
- 配置 OpenClaw（acpx 插件、ACP、跨 session 访问）
- 配置 heartbeat（子 agent 完成后自动回调，无需手动轮询）
- 重启 daemon 并验证

编排器行为规范在 `~/.openclaw/workspace/AGENTS.md` 中定义。

## 使用

安装后通过 Web UI / Telegram / QQ Bot 等渠道发消息。

代码任务会自动触发 acp-coder skill，也可以用 `/acp-coder` 手动触发。

### 简单任务

```
帮我看下 ~/project/app.py 有没有 bug
```

```
review 一下 ~/project/auth.py
```

### 指定 agent

```
用 codex 帮我重构 ~/project/handler.py
```

### 复杂任务（自动拆解为多阶段）

```
重构 ~/project/auth/ 模块，完了帮我 review
```

会自动拆解为：claude 分析 → codex 实现 → claude review，确认后按顺序执行。子 agent 完成后自动推进下一阶段，无需手动"继续"。

### 手动触发

```
/acp-coder 帮我看下 ~/project/app.py 有没有 bug
```

## 支持的 Agent

编排规则已定义的 agent：

| agentId | 工具 |
|---------|------|
| `claude` | Claude Code |
| `codex` | Codex CLI |

setup.sh 还会检测 gemini、opencode、kimi、aider 并加入白名单，但 SKILL.md 目前只定义了 claude 和 codex 的编排规则。扩展新 agent 需同时更新 SKILL.md。

手动添加 agent 到白名单：

```bash
openclaw config set acp.allowedAgents '["claude","codex"]'
openclaw daemon restart
```

## 卸载

```bash
# 删除 skill
rm -rf ~/.openclaw/workspace-assistant/skills/acp-coder

openclaw daemon restart
```
