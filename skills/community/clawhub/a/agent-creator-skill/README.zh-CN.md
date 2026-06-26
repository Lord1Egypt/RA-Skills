# OpenClaw Agent Creator Skill

一个轻量级的 OpenClaw 技能。安装后，你可以通过口语化的方式，让主 Agent（龙虾）自动帮你创建、配置并初始化其他的 **独立 Agent（非子代理）**。

## 💡 工作原理
1. 主 Agent 接收到自然语言指令（例："使用 agent-creator 创建一个精通Python爬虫的代理"）。
2. 主 Agent 查阅 `SKILL.md` 的规范，自动将 Agent ID 翻译为 `python_spider_expert`，生成友好的显示名称，并根据用户请求的语言撰写详细的专属身份提示词；除非用户明确指定其他语言。
3. 主 Agent 会根据当前系统自动调用对应脚本。例如 Linux/macOS/WSL/Git Bash 使用：`bash create_agent.sh "python_spider_expert" "Python爬虫专家" "你是一个资深..."`；原生 Windows PowerShell 使用：`powershell -ExecutionPolicy Bypass -File create_agent.ps1 -AgentId "python_spider_expert" -DisplayName "Python爬虫专家" -IdentityPrompt "你是一个资深..."`。
4. 选中的系统脚本会自动执行 `openclaw agents add` 和 `openclaw agent --message`，瞬间完成新 Agent 的环境创建和记忆注入。

## 🚀 安装方式

### 方式一：口语化在线安装（推荐）
只要这个项目托管在 GitHub 上，你可以直接对你的 OpenClaw 主 Agent 发送指令：
> "帮我安装这个 skill：https://github.com/freesaber/agent-creator-skill。"
主 Agent 会自己拉取代码、配置并使其生效。

### 方式二：手动离线安装
如果你在本地开发调试：
1. 将此文件夹放入 `~/.openclaw/workspace/skills/` 目录下。原生 Windows 通常对应 `%USERPROFILE%\.openclaw\workspace\skills\`。
2. 如果是 Linux/macOS/WSL/Git Bash，在终端进入该目录，确保 shell 脚本有执行权限：`chmod +x create_agent.sh`。如果是原生 Windows PowerShell，使用 `create_agent.ps1`，不需要执行 chmod。
3. 重启 OpenClaw 或等待主 Agent 重新加载技能。

## 💬 使用示例与注意事项

由于大模型的理解惯性，它有时会误以为自己在创建“从属子代理”。为了确保命令精准执行，建议在对话时明确指出：

✅ **推荐话术：**
> "使用 agent-creator 技能创建一个精通 Java 高级开发的代理。注意，是创建一个独立的平级 agent，不要创建 subagent。"
> "帮我建一个产品经理 agent。要求是独立的 agent，不是你的子代理。"

一旦执行成功，主 Agent 会向你报告新 Agent 的名字和工作区路径，你就可以直接与这个新 Agent 开始工作了！
