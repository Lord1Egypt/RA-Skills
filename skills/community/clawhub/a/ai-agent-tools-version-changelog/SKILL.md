---
name: ai-agent-tools-version-changelog
description: 查询 AI 工具（Claude Code、OpenClaw、Hermes Agent 等）的版本日志和最新版本信息。当用户要求以下操作时触发：
- "最新版本"、"版本信息"、"有什么新版本"
- "版本日志"、"changelog"、"更新日志"、"更新记录"
- "最近有什么更新"、"最近版本"
- "升级"、"更新到最新版"（涉及 AI 工具版本检查时）
- 提到具体工具的版本查询，如 "Claude Code 最新版"、"OpenClaw 更新"

支持查询：Claude Code、OpenClaw、NousResearch Hermes Agent。
如果用户没有指定工具但上下文明确，自动推断目标工具。
---

# Version Changelog Skill

查询 GitHub 上开发者工具的版本日志和最新版本信息。

## 工具源配置

| 工具 | GitHub 仓库 | Releases 页面 | CHANGELOG |
|------|-------------|---------------|-----------|
| Claude Code | anthropics/claude-code | https://github.com/anthropics/claude-code/releases | 通过 releases 页面获取 |
| OpenClaw | openclaw/openclaw | https://github.com/openclaw/openclaw/releases | https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md |
| Hermes Agent | nousresearch/hermes-agent | https://github.com/nousresearch/hermes-agent/releases | 通过 releases 页面获取 |

## 查询模式

### 模式 1：查询最新版本

**触发**：用户问"最新版"、"当前版本"、"有什么新版本"

**步骤**：
1. 使用 `web_fetch` 抓取对应工具的 releases 页面
2. 提取第一个（最新的）release 信息：
   - 版本号
   - 发布日期
   - 更新摘要（What's changed）
3. 如果本地有当前版本信息，对比并提示是否需要升级

**示例**：
```
web_fetch("https://github.com/anthropics/claude-code/releases")
```

### 模式 2：查询指定时间范围的版本日志

**触发**：用户问"最近一周"、"X月X日到X月X日"、"过去N天"

**步骤**：
1. 计算时间范围（如"最近一周" = 7天前到今天）
2. 使用 `web_fetch` 抓取 releases 页面
3. 筛选该时间范围内的所有 release
4. 按日期倒序整理，提取每个 release 的关键变更
5. 如果 releases 页面信息不够详细，补充抓取 CHANGELOG.md

**示例**：
```
web_fetch("https://github.com/openclaw/openclaw/releases")
web_fetch("https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md")
```

### 模式 3：多工具版本检查

**触发**：用户问"所有工具最新版本"、"检查更新"

**步骤**：
1. 并行抓取所有工具的 releases 页面
2. 汇总对比，生成版本状态表

## 输出格式

### 最新版本查询输出

```markdown
## [工具名] 最新版本

| 项目 | 信息 |
|------|------|
| **最新版本** | vX.X.X（YYYY-MM-DD） |
| **你当前版本** | vX.X.X（如果已知） |
| **主要更新** | 1-2 条关键变更摘要 |
| **发布页** | GitHub Releases 链接 |

### 更新详情
- 变更 1
- 变更 2
- ...
```

### 时间范围查询输出

```markdown
## [工具名] 版本日志（YYYY-MM-DD ~ YYYY-MM-DD）

### vX.X.X - YYYY-MM-DD
**关键变更**：
- 变更 1
- 变更 2

### vX.X.X - YYYY-MM-DD
**关键变更**：
- ...

---
**共 X 个版本**
```

### 多工具版本状态

```markdown
## 工具版本状态

| 工具 | 最新版本 | 发布日期 | 你当前版本 | 状态 |
|------|---------|---------|-----------|------|
| Claude Code | vX.X.X | YYYY-MM-DD | vX.X.X | ✅ 最新 / ⬆️ 可升级 |
| OpenClaw | vX.X.X | YYYY-MM-DD | vX.X.X | ✅ 最新 / ⬆️ 可升级 |
| Hermes Agent | vX.X.X | YYYY-MM-DD | N/A | ℹ️ 未安装 |
```

## 注意事项

1. **web_fetch 限制**：GitHub 页面内容可能较大，使用 `maxChars` 控制抓取长度（默认 5000）
2. **CHANGELOG 补充**：如果 releases 页面信息不够，补充抓取 CHANGELOG.md
3. **版本对比**：如果用户问是否需要升级，先检查本地版本再给出建议
4. **错误处理**：如果某个工具页面无法访问，跳过并告知用户

## 升级命令参考

| 工具 | 升级命令 |
|------|---------|
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| OpenClaw | `openclaw update` 或 `npm update -g openclaw` |
| Hermes Agent | 参考 GitHub 仓库文档 |
