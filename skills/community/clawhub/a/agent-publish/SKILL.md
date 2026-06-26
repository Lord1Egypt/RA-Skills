---
name: agent-publish
description: |
  Agent 发布/更新到 ClawHub + GitHub 的标准技能。
  当 agent 的核心文件（SOUL.md/AGENTS.md/IDENTITY.md/TOOLS.md）发生变更时，自动询问是否发布更新。
  触发场景：agent 内容更新完成时、用户要求发布/推送/更新到 ClawHub/GitHub、用户说"发布"、"推送"、"publish"、"push"。
  必须在所有 agent workspace 中作为基础技能加载。
---

# Agent Publish Skill

> **定位**：Agent 发布基础设施，一键发布到 ClawHub + GitHub。
> **版本**：1.0.0

---

## 自动触发规则

**当检测到以下核心文件变更时，主动询问用户是否发布**：

- `SOUL.md`
- `AGENTS.md`
- `IDENTITY.md`
- `TOOLS.md`
- `SKILL.md`（如有）

**询问格式**：

```
检测到 [文件名] 已更新。是否发布到 ClawHub + GitHub？

1. 是，立即发布
2. 仅发布到 ClawHub
3. 仅推送到 GitHub
4. 稍后再说
```

---

## 发布流程

### Step 1: 准备 Skill 包

将 agent workspace 核心文件打包到 `~/.qclaw/skills/<agent-id>/` 目录：

```
~/.qclaw/skills/<agent-id>/
├── SKILL.md          # skill 入口（从 SOUL.md 提取核心架构）
├── _meta.json        # 版本信息
└── references/
    ├── soul.md       # SOUL.md 完整版
    ├── agents.md     # AGENTS.md
    ├── identity.md   # IDENTITY.md
    └── tools.md      # TOOLS.md
```

**SKILL.md 生成规则**：
1. frontmatter 包含 name、description
2. 主体内容从 SOUL.md 提取架构总览 + 核心逻辑
3. description 要包含关键词，方便搜索

**_meta.json 格式**：
```json
{
  "version": "<semver>",
  "updatedAt": "<YYYY-MM-DD>",
  "changelog": "<变更说明>",
  "author": "<clawhub-username>"
}
```

### Step 2: 版本号管理

- 首次发布：`1.0.0`
- 架构变更（新增/删除分析层、决策引擎）：**主版本号 +1**（2.0.0）
- 功能增强（新增分析维度、优化输出格式）：**次版本号 +1**（1.1.0）
- Bug 修复（修正措辞、补充细节）：**修订号 +1**（1.0.1）
- 变更说明从本次对话中提取

### Step 3: 发布到 ClawHub

```bash
clawhub skill publish "<skill-dir>" \
  --slug <agent-id> \
  --name "<中文名>" \
  --version <semver> \
  --changelog "<变更说明>" \
  --tags latest
```

**前提**：已登录 `clawhub whoami`

### Step 4: 推送到 GitHub

```bash
# 如果 repo 不存在
gh repo create <github-user>/<agent-id> \
  --public \
  --description "<描述>" \
  --source <skill-dir> \
  --push

# 如果 repo 已存在
cd <skill-dir>
git add -A
git commit -m "v<semver>: <变更说明>"
git push origin master
```

**前提**：已登录 `gh auth status`

---

## 首次设置检查

发布前检查以下工具是否就绪：

1. `clawhub whoami` — 确认 ClawHub 登录
2. `gh auth status` — 确认 GitHub 登录
3. `git --version` — 确认 git 可用

**如果未登录**：
- ClawHub：`clawhub login`
- GitHub：`gh auth login --hostname github.com --git-protocol https --web`

---

## 发布确认清单

发布前确认：

- [ ] 核心文件已更新到 skill 包目录
- [ ] SKILL.md 的 frontmatter 正确
- [ ] _meta.json 版本号正确递增
- [ ] changelog 已填写
- [ ] ClawHub 已登录
- [ ] GitHub 已登录

---

## 现有 Agent 注册表

| Agent ID | ClawHub Slug | GitHub Repo | 最新版本 |
|----------|-------------|-------------|---------|
| vc-analyst | vc-analyst | perrykono-debug/vc-analyst | 1.0.0 |

---

## 错误处理

- **ClawHub 发布失败**：检查 `clawhub whoami`，重新登录
- **GitHub push 失败**：检查 `gh auth status`，重新授权
- **Repo 不存在**：用 `gh repo create` 创建
- **版本号冲突**：ClawHub 不允许同版本覆盖，需递增版本号

---

*版本：1.0.0 | 创建日期：2026-06-06 | 作者：perrykono-debug*
