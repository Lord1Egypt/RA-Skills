# OpenClaw 集成指南

将 ai-self-evolution skill 集成到 OpenClaw 的完整配置与使用说明。

## 概览

OpenClaw 通过“工作区注入 + 事件驱动 Hook”提供上下文能力：  
会话启动时注入工作区文件，Hook 可在生命周期事件上触发提醒。

## 工作区结构

```
~/.openclaw/
├── workspace/                   # 工作目录
│   ├── AGENTS.md               # 多代理协作模式
│   ├── SOUL.md                 # 行为准则与风格
│   ├── TOOLS.md                # 工具能力与使用坑点
│   ├── MEMORY.md               # 长期记忆（仅主会话）
│   └── memory/                 # 每日记忆文件
│       └── YYYY-MM-DD.md
├── skills/                      # 已安装 skills
│   └── <skill-name>/
│       └── SKILL.md
└── hooks/                       # 自定义 hooks
    └── <hook-name>/
        ├── HOOK.md
        └── handler.ts
```

## 快速配置

### 1. 安装 Skill

```bash
clawdhub install ai-self-evolution
```

或手动复制：

```bash
cp -r ai-self-evolution ~/.openclaw/skills/
```

### 2. 安装 Hook（可选）

将 hook 复制到 OpenClaw hooks 目录：

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/ai-self-evolution
```

启用 hook：

```bash
openclaw hooks enable ai-self-evolution
```

### 3. 创建 Learning 文件

在工作区创建 `.learnings/`：

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

或在 skill 目录下创建：

```bash
mkdir -p ~/.openclaw/skills/ai-self-evolution/.learnings
```

## 注入的提示文件

### AGENTS.md

用途：多代理工作流与委派模式。

```markdown
# Agent Coordination

## Delegation Rules
- Use explore agent for open-ended codebase questions
- Spawn sub-agents for long-running tasks
- Use sessions_send for cross-session communication

## Session Handoff
When delegating to another session:
1. Provide full context in the handoff message
2. Include relevant file paths
3. Specify expected output format
```

### SOUL.md

用途：行为规范与沟通风格。

```markdown
# Behavioral Guidelines

## Communication Style
- Be direct and concise
- Avoid unnecessary caveats and disclaimers
- Use technical language appropriate to context

## Error Handling
- Admit mistakes promptly
- Provide corrected information immediately
- Log significant errors to learnings
```

### TOOLS.md

用途：工具能力、集成注意事项、本地配置信息。

```markdown
# Tool Knowledge

## ai-self-evolution Skill
Log learnings to `.learnings/` for continuous improvement.

## Local Tools
- Document tool-specific gotchas here
- Note authentication requirements
- Track integration quirks
```

## Learning 工作流

### 记录 Learnings

1. **会话内**：按常规写入 `.learnings/`
2. **跨会话**：将可复用内容提升到工作区文件

### 提升决策树

```
该 learning 是否项目特定？
├── 是 → 保留在 .learnings/
└── 否 → 是否属于行为/风格？
    ├── 是 → 提升到 SOUL.md
    └── 否 → 是否属于工具使用？
        ├── 是 → 提升到 TOOLS.md
        └── 否 → 提升到 AGENTS.md（工作流）
```

### 提升格式示例

**From learning:**
> Git push to GitHub fails without auth configured - triggers desktop prompt

**To TOOLS.md:**
```markdown
## Git
- Don't push without confirming auth is configured
- Use `gh auth status` to check GitHub CLI auth
```

## 代理间通信

OpenClaw 提供跨会话通信工具：

### sessions_list

查看活跃与近期会话：
```
sessions_list(activeMinutes=30, messageLimit=3)
```

### sessions_history

读取其他会话记录：
```
sessions_history(sessionKey="session-id", limit=50)
```

### sessions_send

向其他会话发送消息：
```
sessions_send(sessionKey="session-id", message="Learning: API requires X-Custom-Header")
```

### sessions_spawn

启动后台子代理：
```
sessions_spawn(task="Research X and report back", label="research")
```

## 可用 Hook 事件

| 事件 | 触发时机 |
|-------|---------------|
| `agent:bootstrap` | 工作区文件注入之前 |
| `command:new` | 执行 `/new` 命令时 |
| `command:reset` | 执行 `/reset` 命令时 |
| `command:stop` | 执行 `/stop` 命令时 |
| `gateway:startup` | gateway 启动时 |

## 检测触发器

### 标准触发器
- 用户纠正（如 “No, that's wrong...”）
- 命令失败（非零退出码）
- API 错误
- 知识缺口

### OpenClaw 特定触发器

| 触发器 | 动作 |
|---------|--------|
| 工具调用错误 | 记录到 TOOLS.md，并标注工具名 |
| 会话交接混乱 | 记录到 AGENTS.md，并补充委派模式 |
| 模型行为异常 | 记录到 SOUL.md，并标注预期与实际 |
| Skill 问题 | 记录到 .learnings/ 或向上游反馈 |

## 验证

检查 hook 是否已注册：

```bash
openclaw hooks list
```

检查 skill 是否已加载：

```bash
openclaw status
```

## 故障排查

### Hook 不触发

1. 确认配置中已启用 hooks
2. 修改配置后重启 gateway
3. 查看 gateway 日志排查错误

### Learnings 未持久化

1. 确认 `.learnings/` 目录存在
2. 检查文件权限
3. 确认 workspace 路径配置正确

### Skill 未加载

1. 确认 skill 位于 skills 目录
2. 检查 SKILL.md frontmatter 是否正确
3. 运行 `openclaw status` 查看加载状态
