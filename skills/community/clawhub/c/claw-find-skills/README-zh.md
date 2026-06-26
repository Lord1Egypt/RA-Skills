# Find-Skills Skill 中文文档

## 概述

**Find-Skills** 是一个帮助用户发现和安装 Agent Skills 的技能。当用户询问"如何做 X"、"找一个 X 的 skill"、"有没有能...的 skill"时，此 skill 会被触发。

**技能市场**: https://skills.sh/

---

## 触发条件

当用户出现以下行为时使用此 skill：

| 触发场景 | 示例 |
|----------|------|
| 询问"如何做 X" | "如何让 React 应用更快？" |
| 请求查找 skill | "找一个 PR review 的 skill" |
| 询问能力 | "你能做 X 吗？" |
| 表达扩展意愿 | "希望能扩展 agent 能力" |
| 搜索工具/模板 | "有没有测试模板？" |
| 提及特定领域 | "希望有设计方面的帮助" |

---

## Skills CLI 介绍

Skills CLI (`npx skills`) 是开放 Agent Skills 生态系统的包管理器。Skills 是模块化包，通过专业知识、工作流和工具扩展 Agent 能力。

### 核心命令

| 命令 | 功能 |
|------|------|
| `npx skills find [query]` | 按关键词交互式搜索 skills |
| `npx skills add <package>` | 从 GitHub 等来源安装 skill |
| `npx skills check` | 检查 skill 更新 |
| `npx skills update` | 更新所有已安装 skills |

---

## 工作流程

### Step 1: 理解用户需求

当用户请求帮助时，识别：

1. **领域** - 如 React、测试、设计、部署
2. **具体任务** - 如编写测试、创建动画、审查 PR
3. **常见程度** - 是否足够常见以至于可能有现成 skill

### Step 2: 搜索 Skills

运行搜索命令：

```bash
npx skills find [query]
```

**示例映射**：

| 用户问题 | 搜索命令 |
|----------|----------|
| "如何让 React 应用更快？" | `npx skills find react performance` |
| "能帮我做 PR review 吗？" | `npx skills find pr review` |
| "我需要创建 changelog" | `npx skills find changelog` |

**搜索结果格式**：

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 3: 向用户展示选项

找到相关 skills 后，展示：

1. Skill 名称和功能说明
2. 安装命令
3. 详细信息链接

**回复示例**：

```
我找到了一个可能有帮助的 skill！"vercel-react-best-practices" skill
提供了来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。

安装命令：
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 4: 提供安装服务

如果用户同意，可以代为安装：

```bash
npx skills add <owner/repo@skill> -g -y
```

**参数说明**：
- `-g` - 全局安装（用户级别）
- `-y` - 跳过确认提示

---

## 常见 Skill 分类

| 类别 | 搜索关键词示例 |
|------|----------------|
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| 文档 | docs, readme, changelog, api-docs |
| 代码质量 | review, lint, refactor, best-practices |
| 设计 | ui, ux, design-system, accessibility |
| 生产力 | workflow, automation, git |

---

## 搜索技巧

### 1. 使用具体关键词

```
❌ testing          # 太宽泛
✅ react testing    # 更具体
```

### 2. 尝试替代术语

```
deploy → deployment → ci-cd
```

### 3. 检查热门来源

许多 skills 来自：
- `vercel-labs/agent-skills`
- `ComposioHQ/awesome-claude-skills`

---

## 未找到 Skills 时的处理

如果搜索无结果：

1. **告知用户** - 没有找到相关 skill
2. **提供替代** - 用通用能力直接帮助
3. **建议创建** - 用户可以自己创建 skill

**回复示例**：

```
我搜索了 "xyz" 相关的 skills 但没有找到匹配项。
我仍然可以直接帮你完成这个任务！要继续吗？

如果这是你经常做的事情，可以创建自己的 skill：
npx skills init my-xyz-skill
```

---

## Skill 包命名规范

```
<owner>/<repo>@<skill-name>
```

**示例**：
- `vercel-labs/agent-skills@vercel-react-best-practices`
- `ComposioHQ/awesome-claude-skills@playwright-testing`

---

## 文件结构

```
skills/find-skills/
├── SKILL.md      # 使用文档
└── _meta.json    # 元数据
```

---

## 特点总结

| 特点 | 说明 |
|------|------|
| **无外部依赖** | 仅依赖 npx skills CLI |
| **交互式搜索** | 支持关键词搜索 |
| **自动安装** | 可代用户执行安装 |
| **友好引导** | 未找到时提供替代方案 |
| **生态开放** | 支持 GitHub 等多来源 |

---

## 相关资源

- **Skills 市场**: https://skills.sh/
- **Vercel Labs Skills**: https://github.com/vercel-labs/agent-skills
- **ComposioHQ Skills**: https://github.com/ComposioHQ/awesome-claude-skills