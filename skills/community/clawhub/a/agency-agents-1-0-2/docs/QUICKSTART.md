# 🚀 快速开始指南

欢迎使用 **AI Agent 团队**！本指南帮助你在 5 分钟内开始使用。

---

## 📦 安装

### 方式 1: 通过 ClawHub（推荐）

```bash
# 安装完整技能包
openclaw skill install agency-agents

# 验证安装
openclaw skill list
```

### 方式 2: 手动安装

```bash
# Clone 仓库
git clone https://github.com/your-repo/agency-agents-openclaw.git

# 复制到技能目录
cp -r agency-agents-openclaw ~/.openclaw/skills/

# 重启 OpenClaw
openclaw restart
```

---

## 🎯 第一次使用

### 示例 1: 使用单个 Agent

```bash
# 前端开发
/openclaw skill use agency-agents --agent frontend-developer "帮我创建一个 React 登录页面，包含邮箱、密码输入框，需要表单验证和错误提示"

# 增长策略
/openclaw skill use agency-agents --agent growth-hacker "为我的 SaaS 产品制定一个 3 个月增长计划，目标是从 1000 用户到 10000 用户"

# 项目管理
/openclaw skill use agency-agents --agent senior-project-manager "帮我把这个需求分解成具体的开发任务：创建一个电商网站"
```

### 示例 2: 使用 Agent 编排器

```bash
# 完整项目开发
/openclaw skill use agency-agents --agent orchestrator "帮我开发一个完整的博客系统，包括：
- 前端：React + Tailwind CSS
- 后端：Node.js + Express
- 数据库：PostgreSQL
- 功能：用户注册登录、文章发布、评论、标签分类"

# 营销活动
/openclaw skill use agency-agents --agent orchestrator "为我的新产品发布策划一次完整的营销活动，包括社交媒体、内容营销和 PR"
```

### 示例 3: 使用整个部门

```bash
# 工程部门协作
/openclaw skill use agency-agents --department engineering "开发一个完整的 Web 应用，包括前端和后端"

# 市场部门协作
/openclaw skill use agency-agents --department marketing "制定并执行一个季度的营销计划"
```

---

## 💡 常用场景

### 场景 1: 创业公司 MVP

```bash
# 使用编排器自动调度
/openclaw skill use agency-agents --agent orchestrator "帮我快速开发一个 MVP，验证我的创业想法：一个面向自由职业者的时间追踪应用"

# 或手动选择 Agent
# 1. 前端开发
/openclaw skill use agency-agents --agent frontend-developer "创建响应式时间追踪界面"

# 2. 后端架构
/openclaw skill use agency-agents --agent backend-architect "设计用户、项目、时间条目的数据模型和 API"

# 3. 增长策略
/openclaw skill use agency-agents --agent growth-hacker "制定早期用户获取策略"
```

### 场景 2: 网站重构

```bash
/openclaw skill use agency-agents --agent orchestrator "重构我们的公司网站：
- 当前：老式 PHP 网站
- 目标：现代 React + 头 CMS
- 要求：保持 SEO、提升性能、移动优先"
```

### 场景 3: 数据分析报告

```bash
/openclaw skill use agency-agents --agent data-analytics-reporter "分析我们的销售数据，生成月度报告，包括：
- 销售趋势
- 产品线表现
- 地区分析
- 下月预测"
```

---

## 🎭 可用 Agent 快速参考

### 💻 工程部
| Agent | 用途 | 命令 |
|-------|------|------|
| 前端开发 | React/Vue/Angular 开发 | `frontend-developer` |
| 后端架构 | API/数据库设计 | `backend-architect` |
| 移动端 | iOS/Android开发 | `mobile-app-builder` |
| AI 工程 | ML/AI集成 | `ai-engineer` |
| DevOps | CI/CD/基础设施 | `devops-automator` |

### 📢 市场部
| Agent | 用途 | 命令 |
|-------|------|------|
| 增长黑客 | 用户获取/转化 | `growth-hacker` |
| 内容创作 | 多平台内容 | `content-creator` |
| 社交媒体 | 社交策略 | `social-media-strategist` |
| TikTok | 短视频策略 | `tiktok-strategist` |

### 🎬 项目管理
| Agent | 用途 | 命令 |
|-------|------|------|
| 高级 PM | 任务分解/规划 | `senior-project-manager` |
| 项目协调 | 跨职能协调 | `project-shepherd` |
| 实验追踪 | A/B 测试 | `experiment-tracker` |

### 🧪 测试部
| Agent | 用途 | 命令 |
|-------|------|------|
| 现实检查 | 质量认证 | `reality-checker` |
| 证据收集 | 截图 QA | `evidence-collector` |
| 性能测试 | 性能基准 | `performance-benchmarker` |

---

## 📊 最佳实践

### 1. 清晰的任务描述

❌ **模糊**:
```
"帮我做个网站"
```

✅ **清晰**:
```
"帮我创建一个电商网站的前端，使用 React + Tailwind CSS，需要包含：
- 首页（展示热门商品）
- 商品列表页（带筛选和排序）
- 商品详情页
- 购物车页面
- 结账流程
要求：响应式设计，支持移动端，无障碍合规"
```

### 2. 提供上下文

```
"我的产品是一个面向小企业的 SaaS 记账工具，目标用户是没有会计背景的店主。
请帮我设计一个 onboarding 流程，让他们能在 5 分钟内完成初始设置并开始使用。"
```

### 3. 迭代优化

```
# 第一轮
"帮我写一个登录页面"

# 第二轮（基于输出反馈）
"很好！现在添加以下功能：
1. 社交登录（Google、微信）
2. 记住我功能
3. 密码强度指示器"

# 第三轮
"再优化一下移动端体验，按钮太小了"
```

### 4. 多 Agent 验证

```
# 开发完成后，让测试 Agent 验证
/openclaw skill use agency-agents --agent reality-checker "审查这个登录页面的实现质量"

# 让 UX Agent 提供建议
/openclaw skill use agency-agents --agent ux-researcher "从 UX 角度审查这个登录流程"
```

---

## ⚙️ 配置选项

### 环境变量

```bash
# 设置默认部门（可选）
export AGENCY_AGENTS_DEFAULT_DEPARTMENT=engineering

# 设置质量检查严格度 1-5（默认 3）
export AGENCY_AGENTS_QA_LEVEL=4

# 启用详细日志（可选）
export AGENCY_AGENTS_VERBOSE=true
```

### 技能配置

在 `~/.openclaw/skills/agency-agents-openclaw/config.json` 中：

```json
{
  "defaultAgent": "frontend-developer",
  "qaLevel": 3,
  "maxRetries": 3,
  "timeout": 3600,
  "verbose": false
}
```

---

## 🆘 常见问题

### Q: 安装后找不到技能？
A: 运行 `openclaw skill list` 确认安装成功，然后重启 OpenClaw。

### Q: Agent 输出不符合预期？
A: 
1. 提供更详细的任务描述
2. 提供示例和参考
3. 明确技术栈和要求
4. 使用迭代方式优化

### Q: 如何切换 Agent？
A: 直接在新命令中指定不同 Agent 即可：
```bash
/openclaw skill use agency-agents --agent growth-hacker "..."
```

### Q: 多 Agent 如何协作？
A: 使用编排器自动调度，或手动依次调用不同 Agent。

### Q: 如何保存 Agent 输出？
A: Agent 会自动保存输出到工作区，路径：`~/clawd/agency-agents/[日期]/[项目名]/`

---

## 📚 进阶资源

- [完整 Agent 列表](./agents-list.md)
- [使用指南](./usage-guide.md)
- [最佳实践](./best-practices.md)
- [API 参考](./api-reference.md)
- [示例项目](../examples/)

---

## 💬 获取帮助

- 📧 Email: support@your-company.com
- 💬 Discord: 加入社区
- 📚 文档：https://docs.your-company.com

---

**准备好开始了吗？** 试试第一个命令：

```bash
/openclaw skill use agency-agents --agent frontend-developer "帮我创建一个简单的 React 计数器组件"
```

🎉 祝你使用愉快！
