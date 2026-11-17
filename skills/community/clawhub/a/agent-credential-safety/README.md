# Agent Credential Safety

一个面向 AI Coding Agent 的凭据安全技能（Skill）——不是把密码藏进文件，而是限制谁能取、何时能取、取到后能做什么。

## 解决什么问题

当你让 Claude Code、Codex、Cursor 等 Agent 帮你写代码时，它们经常需要调用 API、访问服务器。常见的做法是在每个项目里放 `.env`，或者让 Agent 自己找密钥——这带来了几个问题：

- 凭据散落在多个项目里，轮换时容易遗漏
- Agent 可能遍历配置文件、把密钥写进日志或补丁
- `.gitignore` 只能防手滑，挡不住有终端权限的 Agent
- 没有统一的取用规则，每次都靠 Agent "自觉"

这个 Skill 提供一套可执行的凭据使用政策，覆盖**存储、取用、行动、追责**四层。

## 快速开始

### 1. 创建凭据文件

```bash
mkdir -p ~/.localcfg
```

创建 `~/.localcfg/base.env`：

```env
# 按需添加你需要的变量
OPENROUTER_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
# ...
```

### 2. 配置 SSH 别名

编辑 `~/.ssh/config`：

```
Host myserver
    HostName 192.0.2.1
    Port 22
    User deploy
    IdentityFile ~/.ssh/myserver.pem
    IdentitiesOnly yes
```

### 3. 在 Agent 中安装本 Skill

**Claude Code：** 将 `SKILL.md` 放入 `~/.claude/skills/ps/SKILL.md`（或创建软链接）。

**Codex：** 将 `SKILL.md` 放入全局 agents 目录，并参考 `agents/openai.yaml` 配置触发策略。

### 4. 在项目代码中加载

```python
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.home() / ".localcfg" / "base.env")
```

## 设计原则

这不是一个企业级安全管理方案，而是一套**个人工作流中的可执行政策**：

| 层级 | 做什么 | 防什么 |
|------|--------|--------|
| **存储层** | 集中保存，统一命名，不进仓库 | 散布、漏改、误提交 |
| **取用层** | 每次只给任务必需的那一把 | 权限蔓延、不必要的暴露 |
| **行动层** | 高风险动作由系统拦截 | Agent 越权执行 |
| **追责层** | 知道哪次任务用了什么权限 | 出问题无法定位和撤销 |

## 不是什么

- ❌ 不是 Vault / KMS 的替代品
- ❌ 不是防恶意代码的安全边界（Agent 有终端权限时理论上仍可读取）
- ✅ 是减少误操作、建立可执行规则、降低暴露面的实用方案

## License

MIT
