# AI工作日记 · 飞书知识库 Skill

将「今天用 AI 完成的事」写成第一人称 **AI工作日记**，并发布到**你指定的**飞书 Wiki / 云文档父节点。

Skill 标识（frontmatter `name`）：`ai-work-journal-feishu`

本仓库**不含**任何私有 Wiki 链接或 token；首次使用由 Agent 询问落库位置，可征得你同意后写入本机 `config.local.json`（已 gitignore）。

## 安装

```bash
git clone https://github.com/testman2025/ai-practice-journal-feishu.git
```

### WorkBuddy

指向本目录安装后，说：「记到飞书知识库 / 写今天的 AI工作日记」。

### Cursor

Clone 后在对话中 `@SKILL.md`，或把本目录加入你的 skills / rules 加载路径。

## 使用前：飞书准备

1. **登录态**：启用 Feishu Docs MCP 并完成认证，或本机 `lark-cli` 已登录
2. **父节点**：准备要挂载日记的 Wiki 页面链接（或直接提供 node token）
3. **首次对话**：Agent 会问「上传到飞书哪里」；确认「记住」后写入 `config.local.json`

详细字段说明见 `SKILL.md`「飞书接入」「飞书落库配置」。

**切勿**把 App Secret、密码、真实 `config.local.json` 提交到 git。

## 要点

- 标题必填分类：`YYYY-MM-DD｜[类型·场景] 主题`
- 正文结构不固定，按当天内容灵活删节、合并、加节
- 排障类：先因果链流程图，再展开
- 缺截图会向你要，不会空占位

## 文件

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | Agent 执行规范 |
| `README.md` | 本说明 |
| `config.local.json` | 本机落库配置（不提交，可选） |
| `config.local.example.json` | 配置字段示例 |

## 许可与隐私

分享本 skill 前请确认文档中无个人 Wiki URL、token、知识库层级名或本机绝对路径。日常私有配置只放在 `config.local.json`。
