# 🚀 Claude Code Enhancement

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-增强组件-blue?style=for-the-badge&logo=rocket" alt="OpenClaw">
  <img src="https://img.shields.io/badge/版本-1.0.0-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-orange?style=for-the-badge" alt="License">
</p>

> [!TIP]
> 借鉴 Claude Code 顶级架构设计，为 OpenClaw 打造企业级多 Agent 协作系统

---

## ✨ 为什么选择它？

<p align="center">
  <img src="https://streak-stats.demolab.com?user=ntaffffff&theme=dark&hide_border=true" width="400">
</p>

传统的 AI Agent 助手只能**单打独斗**，而这个技能让你拥有**一个指挥官 + N 个执行者**的超级团队！

| 传统模式 | Claude Code Enhancement |
|---------|------------------------|
| ❌ 单线程执行 | ✅ 多 Agent 并行处理 |
| ❌ 工具权限混乱 | ✅ 完整权限控制系统 |
| ❌ 记忆碎片化 | ✅ 结构化记忆体系 |
| ❌ 任务难以追踪 | ✅ 全链路进度监控 |

---

## 🎯 核心功能

### 1. 🧠 Coordinator - 多 Agent 协调器

```
┌─────────────────────────────────────────────────────────────┐
│                        Coordinator                          │
│  🧠 主 Agent (指挥官)                                       │
│     ├── 分析任务                                            │
│     ├── 拆分任务                                            │
│     └── 汇总结果                                            │
│                                                              │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│   │ Worker 1 │   │ Worker 2 │   │ Worker 3 │              │
│   │  🔨 编码  │   │  🔍 测试  │   │  📝 文档  │              │
│   └──────────┘   └──────────┘   └──────────┘              │
│        ↓              ↓              ↓                     │
│   ─────────────────────────────────────────────            │
│                    结果聚合返回                              │
└─────────────────────────────────────────────────────────────┘
```

**一部手机同时让 5 个人帮你干活！**

```bash
# 启动协调者模式
/coord start

# 派生出 3 个 Worker 同时工作
/coord spawn "后端 API" "实现用户注册接口，用 FastAPI"
/coord spawn "前端组件" "实现注册页面，用 React"
/coord spawn "单元测试" "为注册功能编写测试用例"

# 查看所有 Worker 状态
/coord status
```

---

### 2. 🛡️ Tool Permission - 工具权限系统

<p align="center">
  <img src="https://img.shields.io/badge/安全-企业级-red?style=for-the-badge" alt="Security">
</p>

再也不用担心 AI 误删重要文件了！

```python
# 配置文件示例
permission:
  default_mode: "ask"  # 默认每次询问
  
  always_allow:        # 始终允许（安全工具）
    - GlobTool
    - GrepTool
    - FileReadTool
  
  always_deny:         # 始终拒绝（危险操作）
    - FormatDiskTool
    - DeleteProduction
  
  always_ask:          # 始终询问（修改类）
    - BashTool
    - FileWriteTool
    - FileEditTool
```

| 工具类型 | 示例 | 默认行为 |
|---------|------|---------|
| 🔍 只读 | `GlobTool`, `GrepTool` | 自动允许 |
| ⚠️ 修改 | `FileWriteTool`, `BashTool` | 询问确认 |
| ☠️ 危险 | `FormatDiskTool` | 始终拒绝 |

---

### 3. 💾 Memory System - 结构化记忆

<p align="center">
  <img src="https://img.shields.io/badge/记忆-永久保存-blue?style=for-the-badge" alt="Memory">
</p>

再也不用每次都重复告诉 AI 你的偏好！

```
memory/
├── MEMORY.md           ← 入口文件（每次对话自动加载）
├── user/
│   └── preferences.md  ← 你的个人偏好
├── feedback/
│   └── corrections.md  ← 你的每次纠正
├── project/
│   └── context.md      ← 项目上下文
└── reference/
    └── docs.md         ← 参考资料
```

```bash
# 记住我的偏好
/memory add user "我喜欢用 TypeScript + React"

/memory add feedback "上次那个函数写错了，应该是这样..."
/memory search "TypeScript"
```

---

### 4. 📊 Task Workflow - 任务工作流

<p align="center">
  <img src="https://img.shields.io/badge/进度-可视化-green?style=for-the-badge" alt="Progress">
</p>

像项目管理工具一样追踪 AI 任务！

```
任务: 用户头像上传功能
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 阶段 1: 分析 ████████████ 100%
🎯 阶段 2: 规划 ████████░░░░ 80%
▶️ 阶段 3: 执行 ████░░░░░░░░ 40%
⏳ 阶段 4: 验证 ░░░░░░░░░░░ 0%
⏳ 阶段 5: 总结 ░░░░░░░░░░░ 0%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```bash
/task create "实现用户头像上传"
/task status      # 查看当前状态
/task progress    # 查看详细进度
/task complete    # 标记完成
```

---

### 5. 🤖 Enhanced Agent - 增强版 Agent

| Agent 类型 | 描述 | 超能力 |
|-----------|------|--------|
| 🧑‍💻 `coder` | 编码专家 | 写代码、debug、重构 |
| 🔍 `reviewer` | 审查专家 | 代码审查、安全扫描 |
| 📚 `researcher` | 研究专家 | 信息收集、分析整理 |
| 👷 `worker` | 多面手 | 通用任务执行 |
| 🧠 `general` | 全能型 | 日常对话任务 |

```python
# 调用专门的 Coding Agent
agent = await spawn_agent(
    type="coder",
    description="修复登录 bug",
    prompt="用户反馈登录后 token 过期时间不对，请检查并修复",
    isolation="worktree"  # 隔离环境，安全！
)
```

---

## 🚀 快速开始

### 安装

```bash
# 方式一：ClawHub 安装（推荐）
clawhub install claude-code-enhancement

# 方式二：GitHub 手动安装
git clone https://github.com/ntaffffff/openclaw-claude-code-enhancement.git
cd openclaw-claude-code-enhancement
```

### 使用

```bash
# 启动多 Agent 协作
/coord start

# 添加记忆
/memory add user "我喜欢用 Python + FastAPI"

# 创建任务
/task create "实现支付功能"
```

---

## 📖 文档导航

| 文档 | 说明 |
|------|------|
| [功能详解](./docs/features.md) | 所有功能的详细介绍 |
| [配置指南](./docs/config.md) | 如何自定义配置 |
| [API 参考](./docs/api.md) | 开发者 API |
| [常见问题](./docs/faq.md) | 常见问题解答 |

---

## 🆚 对比其他方案

| 特性 | 本技能 | 传统单 Agent | 其他多 Agent 方案 |
|------|--------|-------------|------------------|
| 多 Worker 并行 | ✅ | ❌ | ✅ |
| 工具权限控制 | ✅ 企业级 | ❌ | ⚠️ 基础 |
| 结构化记忆 | ✅ | ❌ | ❌ |
| 任务进度追踪 | ✅ | ❌ | ⚠️ 基础 |
| 隔离执行模式 | ✅ Git Worktree | ❌ | ⚠️ 有限 |
| 零侵入 | ✅ | - | ❌ |

---

## 🧪 示例展示

### 示例 1：同时实现一个完整功能

```
用户: 帮我实现一个用户认证系统

> /coord start

[Coordinator] 分析任务中...
[Coordinator] 任务已拆分为 4 个子任务

> /coord spawn "用户模型" "实现 User 模型，包含 id, email, password, createdAt"
> /coord spawn "注册 API" "实现 POST /register 接口"
> /coord spawn "登录 API" "实现 POST /login 接口，返回 JWT"
> /coord spawn "中间件" "实现 JWT 验证中间件"

[Worker 1] ✅ 完成
[Worker 2] ✅ 完成
[Worker 3] ✅ 完成  
[Worker 4] ✅ 完成

[Coordinator] 结果聚合中...
[Coordinator] ✅ 任务完成！
```

### 示例 2：记住你的偏好

```
用户: 记住我喜欢用 Vitest 做测试

> /memory add user "测试框架: Vitest"
> /memory add user "代码风格: 函数式编程"
> /memory add user "喜欢用 async/await"

[Memory] ✅ 已记住！

用户: 帮我写个工具函数

[Agent] 好的！我会用 Vitest + 函数式风格来写～
```

---

## 🤝 贡献者

<p align="center">
  <img src="https://contributors-img.web.app/image?repo=ntaffffff/openclaw-claude-code-enhancement" width="400">
</p>

---

## 📝 更新日志

### v1.0.0 (2026-04-03)
- 🎉 初始版本发布
- ✅ Coordinator 多 Agent 协调
- ✅ Tool Permission 权限系统
- ✅ Memory System 记忆系统
- ✅ Task Workflow 任务工作流
- ✅ Enhanced Agent 增强代理

---

## 📄 许可证

<p align="center">
  <img src="https://img.shields.io/badge/许可证-MIT-blue?style=for-the-badge" alt="License">
</p>

MIT License - 自由使用，保留署名即可。

---

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请点个 Star！</strong>
</p>

<p align="center">
  <a href="https://github.com/ntaffffff/openclaw-claude-code-enhancement">
    <img src="https://img.shields.io/github/stars/ntaffffff/openclaw-claude-code-enhancement?style=social" alt="Star">
  </a>
  <a href="https://github.com/ntaffffff/openclaw-claude-code-enhancement/fork">
    <img src="https://img.shields.io/github/forks/ntaffffff/openclaw-claude-code-enhancement?style=social" alt="Fork">
  </a>
</p>

---

<p align="center">
  <sub>Made with ❤️ by dxx</sub>
</p>