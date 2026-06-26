# settings.local.json 权限配置模板

> 创建自我进化智能体时，将此模板复制到 `~/.claude/skills/<skill-name>/.claude/settings.local.json`
> 并替换 `{{SKILL_NAME}}` 为实际技能名称

## 基础版（自我进化智能体必备）

适用于大多数自我进化智能体，提供对自己 skill 目录的完整读写权限。

```json
{
  "permissions": {
    "allow": [
      "Read(/~/.claude/skills/{{SKILL_NAME}}/**)",
      "Write(/~/.claude/skills/{{SKILL_NAME}}/**)",
      "Edit(/~/.claude/skills/{{SKILL_NAME}}/**)",
      "Glob(/~/.claude/skills/{{SKILL_NAME}}/**)",
      "Grep(/~/.claude/skills/{{SKILL_NAME}}/**)",
      "WebSearch(*)",
      "Bash(echo:*)",
      "Bash(ls:*)",
      "Bash(mkdir:*)",
      "Bash(cat:*)"
    ]
  }
}
```

## WebFetch 版（需要网页抓取）

适用于需要访问网页内容的智能体（如家庭医生、操盘手等）。

在基础版基础上增加：
```json
      "WebFetch(*)",
```

## Python 版（需要运行 Python 脚本）

适用于需要运行 Python 工具的智能体（如操盘手等）。

在基础版基础上增加：
```json
      "Bash(python3:*)",
```

## 技术达人版（需要安装工具）

适用于需要安装/管理软件包的技术类智能体。

在基础版基础上增加：
```json
      "Bash(python3:*)",
      "Bash(brew:*)"
```

## 完整版（bypassPermissions）

适用于需要访问用户目录大部分内容的智能体（如管家、项目维护者）。

```json
{
  "permissions": {
    "allow": [
      "Read(~/**)",
      "Write(~/**)",
      "Edit(~/**)",
      "Glob(~/**)",
      "Grep(~/**)",
      "WebSearch(*)",
      "WebFetch(*)",
      "Bash(*)"
    ]
  }
}
```

---

## 使用说明

1. 创建新角色时，根据角色需求选择合适的模板版本
2. 将 `{{SKILL_NAME}}` 替换为实际的技能名称
3. 将文件保存到 `~/.claude/skills/<skill-name>/.claude/settings.local.json`
4. 确保已创建 `.claude` 目录：`mkdir -p ~/.claude/skills/<skill-name>/.claude`

## 权限字段说明

| 字段 | 用途 |
|------|------|
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件（替换内容） |
| `Glob` | 文件模式匹配（列出文件） |
| `Grep` | 文件内容搜索 |
| `WebSearch` | 网络搜索 |
| `WebFetch` | 抓取网页内容 |
| `Bash` | 执行 Shell 命令 |

## 关键原则

1. **最小权限原则** — 只授予角色必需的权限
2. **自我进化必需** — 所有自我进化智能体必须对自己 skill 目录有完整读写权限
3. **渐进式扩展** — 基础版优先，根据需要逐步增加权限
