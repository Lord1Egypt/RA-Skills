# 🚀 Claude Code Enhancement

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-增强组件-blue?style=for-the-badge&logo=rocket" alt="OpenClaw">
  <img src="https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge" alt="Python">
</p>

> [!TIP]
> 借鉴 Claude Code 顶级架构设计，为 OpenClaw 打造企业级多 Agent 协作系统

---

## ✨ 一句话介绍

**让你的 AI 助手拥有"一个指挥官 + N 个执行者"的超级团队！**

传统 AI 只能单打独斗，这个技能让你同时指挥多个 AI 并行工作，效率翻 10 倍！

---

## 🎯 能做什么？

### 1️⃣ 多 Agent 协作 - 一人干活，十人围观变成历史

```bash
# 传统方式：AI 一个个任务做，累死个人
用户: 帮我实现登录功能
AI: 好的，我来写后端 API...
(1小时后...)
AI: 好了，我再写前端页面...
(2小时后...)
AI: 完成了！

# 使用本技能：5 个 AI 同时帮你干！
用户: 帮我实现登录功能
> /coord start
> /coord spawn "后端API" "实现登录接口"
> /coord spawn "前端页面" "实现登录页面"  
> /coord spawn "单元测试" "写登录测试"
> /coord spawn "文档" "写 API 文档"

[Coordinator] ✅ 4 个任务同时完成，总耗时 15 分钟！
```

### 2️⃣ 工具权限管理 - 再也不怕 AI 删错文件

```
场景: AI 帮你整理文件，一不小心删错了...

❌ 没有权限系统:
AI: 好的，我帮你删除这个文件夹
(啪！重要文件没了！哭都来不及)

✅ 有权限系统:
AI: 我想删除这个文件夹
🛡️ [拦截] 这看起来是个重要文件夹，确认删除吗？
用户: 确认
AI: 已删除
```

### 3️⃣ 永久记忆 - 不用每次都重复交代

```
❌ 每次都要说:
用户: 记住我用 TypeScript
用户: 记得我用 React
用户: 我喜欢 Vitest
用户: 我用 FastAPI
用户: 我...

✅ 一次记住，终身不忘:
用户: /memory add user "我喜欢 TypeScript + React + FastAPI + Vitest"
[Memory] ✅ 已记住！

用户: 帮我写个后端接口
AI: 好的！我用 TypeScript + FastAPI 来写，再配上 Vitest 测试～
```

### 4️⃣ 任务进度可视化 - 看得见的进度

```
任务: 电商项目重构
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 分析   ████████████ 100% ✅
🎯 规划   ██████████░░ 80% ✅
▶️ 执行   ████░░░░░░░░ 40% 🔄
⏳ 验证   ░░░░░░░░░░░░ 0% ⏳
⏳ 总结   ░░░░░░░░░░░░ 0% ⏳
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 正在执行: "实现用户模块"
```

---

## 🚀 5 分钟快速入门

### 步骤 1: 安装

```bash
# 方式一：ClawHub 一键安装（推荐）
clawhub install claude-code-enhancement

# 方式二：GitHub 手动安装
git clone https://github.com/ntaffffff/openclaw-claude-code-enhancement.git
cd openclaw-claude-code-enhancement
```

### 步骤 2: 启动多 Agent 模式

```bash
# 告诉 AI: 我要用多 Agent 模式
/coord start

# 或者自然语言触发
"帮我实现一个用户认证系统，要包含注册、登录、token 验证"
```

### 步骤 3: 派发任务

```bash
# 派发多个并行任务
/coord spawn "后端" "用 FastAPI 实现注册和登录接口"
/coord spawn "前端" "用 React 实现登录页面"
/coord spawn "测试" "用 Vitest 写测试用例"

# 查看状态
/coord status
```

### 步骤 4: 验收结果

```
[Worker 1] ✅ 后端完成
[Worker 2] ✅ 前端完成  
[Worker 3] ✅ 测试完成

/coord stop  # 退出协调模式
```

---

## 📖 进阶用法

### 记住你的偏好

```bash
# 记住技术栈
/memory add user "后端: Python + FastAPI"
/memory add user "前端: React + TypeScript"
/memory add user "测试: Vitest"
/emory add user "数据库: PostgreSQL"

/memory list  # 查看所有记忆
```

### 使用专门的 Agent

```python
# 召唤一个 Coding Agent
await spawn_agent(
    type="coder",
    description="修复登录 bug",
    prompt="用户登录后 token 过期时间不对，请检查 JWT 生成逻辑"
)

# 召唤一个 Reviewer Agent  
await spawn_agent(
    type="reviewer", 
    description="安全审计",
    prompt="请检查整个项目的安全问题"
)
```

### 配置权限规则

```yaml
# 在配置文件中设置
permission:
  default_mode: "ask"
  
  # 永远信任这些工具
  always_allow:
    - GlobTool        # 查找文件
    - GrepTool        # 搜索内容
    - FileReadTool    # 读取文件
  
  # 永远拒绝这些
  always_deny:
    - FormatDiskTool  # 格式化磁盘
    - DropDatabase    # 删除数据库
  
  # 每次确认
  always_ask:
    - BashTool        # 执行命令
    - FileWriteTool   # 写入文件
    - FileDeleteTool  # 删除文件
```

---

## 🆚 对比传统方案

| 功能 | 本技能 | 其他方案 |
|------|--------|---------|
| 多 Worker 并行 | ✅ 最多 5 个 | ❌ 没有 |
| 工具权限控制 | ✅ 企业级安全 | ❌ 没有 |
| 永久记忆 | ✅ 结构化 | ❌ 没有 |
| 任务追踪 | ✅ 可视化 | ❌ 没有 |
| 隔离执行 | ✅ Git Worktree | ❌ 没有 |

---

## 📦 包含模块

```
claude-code-enhancement/
├── SKILL.md              # 本文件
├── coordinator/          # 多 Agent 协调器
│   └── coordinator.py    # 核心协调逻辑
├── agent/                # 增强 Agent
│   └── agent_tool.py     # Agent 工具
├── memory/               # 记忆系统
│   └── memory.py         # 记忆管理
├── permission/           # 权限系统
│   └── permission.py     # 权限控制
├── workflow/             # 任务工作流
│   └── workflow.py       # 工作流引擎
├── nlp_parser.py         # 自然语言解析
└── main.py               # 入口文件
```

---

## 🤝 遇到问题？

1. **GitHub Issues**: https://github.com/ntaffffff/openclaw-claude-code-enhancement/issues
2. **文档**: 查看 `./docs/` 目录
3. **群聊**: 加入 OpenClaw Discord

---

## 📝 更新日志

### v1.0.0 (2026-04-03)
- 🎉 首发版本
- ✅ Coordinator 多 Agent 协调
- ✅ Tool Permission 权限系统  
- ✅ Memory System 记忆系统
- ✅ Task Workflow 任务工作流
- ✅ Enhanced Agent 增强代理

---

## ⭐ 支持我们

如果这个项目对你有帮助，请：

1. **点个 Star** ⭐
2. **分享给朋友** 📢
3. **提 Bug/建议** 🐛

---

<p align="center">
  <sub>Made with ❤️ by dxx</sub>
</p>