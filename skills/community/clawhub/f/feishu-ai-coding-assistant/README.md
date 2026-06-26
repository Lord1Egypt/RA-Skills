# 🤖 飞书 AI 编程助手

> 调用子 Agent 完成大型项目，支持 OpenCode、Claude Code、Codex 等多种编程工具

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.ai/skills/feishu-ai-coding-assistant)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

## 📖 简介

飞书 AI 编程助手是一个强大的 Skill，专为大型项目开发而设计。它通过调用子 Agent 来并行处理复杂任务，支持多种主流 AI 编程工具的选择和安装。

### ✨ 核心特性

- 🛠️ **多工具支持** - OpenCode、Claude Code、Codex、Cursor、Continue
- 📦 **版本管理** - 明确指定每个工具的版本，确保环境一致性
- 🤖 **子 Agent 编排** - 创建和管理多个子 Agent 并行执行任务
- 📊 **进度监控** - 实时查看子 Agent 执行状态和进度
- 🔧 **自动安装** - 一键安装缺失的编程工具
- 📝 **完整文档** - 自动生成项目文档和 API 说明

## 🚀 快速开始

### 安装 Skill

```bash
# 通过 Claw-CLI 安装
claw skill install feishu-ai-coding-assistant
```

### 首次使用

```bash
# 启动交互式引导
/ai-coding
```

Skill 会引导你完成以下步骤：

1. 选择要使用的编程工具
2. 检查并安装工具（如需要）
3. 描述项目任务
4. 创建子 Agent 执行

## 📋 支持的编程工具

| 工具 | 版本 | 描述 | 适用场景 |
|------|------|------|----------|
| **OpenCode** | v1.0.0 | 开源免费代码生成工具 | 基础代码生成、快速原型 |
| **Claude Code** | v2.0.0 | Anthropic 官方代码助手 | 复杂逻辑、代码审查 |
| **Codex** | v3.5.0 | OpenAI 代码生成模型 | 多语言支持、全栈开发 |
| **Cursor** | v0.40.0 | AI 优先的代码编辑器 | 日常开发、编辑器集成 |
| **Continue** | v0.8.0 | VS Code AI 编程插件 | 轻量级、VS Code 用户 |

## 💡 使用示例

### 1. 查看可用工具

```
/ai-coding list
```

输出：
```
**OpenCode** v1.0.0
开源免费，适合基础代码生成

**Claude Code** v2.0.0
强大推理，适合复杂逻辑

**Codex** v3.5.0
多语言支持，适合全栈开发

**Cursor** v0.40.0
编辑器集成，适合日常开发

**Continue** v0.8.0
VS Code 插件，轻量级选择
```

### 2. 检查工具安装状态

```
/ai-coding check claude-code
```

输出：
```
✅ Claude Code v2.0.0 已安装
```

### 3. 安装编程工具

```
/ai-coding install claude-code
```

输出：
```
正在安装 Claude Code v2.0.0...

命令：`npm install -g @anthropic-ai/claude-code@2.0.0`
```

### 4. 执行项目任务

```
/ai-coding run 创建一个 React 待办事项应用，包含用户认证和任务管理功能
```

输出：
```
✅ 已创建子 Agent 执行任务

**会话 ID:** `sess_abc123`
**工具:** Claude Code v2.0.0
**任务:** 创建一个 React 待办事项应用，包含用户认证和任务管理功能

子 Agent 正在后台执行，完成后会通知你。使用 `/ai-coding status` 查看进度。
```

### 5. 查看子 Agent 状态

```
/ai-coding status
```

输出：
```
📊 当前子 Agent 状态:

- **ai-coding-claude-code-1710057600**: running
- **ai-coding-codex-1710054000**: completed
```

### 6. 终止子 Agent

```
/ai-coding kill sess_abc123
```

## 🔧 配置选项

在 `skill.json` 中配置以下参数：

```json
{
  "config": {
    "defaultTool": "claude-code",      // 默认编程工具
    "autoInstall": true,               // 自动安装缺失工具
    "subagentTimeout": 3600,           // 子 Agent 超时时间（秒）
    "maxSubagents": 5,                 // 最大并行子 Agent 数量
    "workspace": "./workspace"         // 默认工作目录
  }
}
```

## 📁 项目结构

```
feishu-ai-coding-assistant/
├── SKILL.md                 # ClawHub 格式说明
├── skill.json               # Skill 元数据
├── package.json             # NPM 配置
├── tsconfig.json            # TypeScript 配置
├── README.md                # 完整文档
├── src/
│   └── index.ts             # 主入口
├── tests/
│   └── index.test.ts        # 单元测试
└── .gitignore
```

## 🧪 测试

```bash
# 安装依赖
npm install

# 运行测试
npm test

# 构建
npm run build
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👤 作者

**OpenClaw Skill Master**

- ClawHub: [@skill-master](https://clawhub.ai/users/skill-master)
- GitHub: [@openclaw-skills](https://github.com/openclaw-skills)

## 📝 更新日志

### v1.0.0 (2026-03-10)

- ✨ 初始版本发布
- 🛠️ 支持 5 种编程工具（OpenCode、Claude Code、Codex、Cursor、Continue）
- 🤖 子 Agent 创建与管理
- 📊 进度监控和状态查询
- 📦 自动安装和版本管理
- 📝 完整文档和示例

## ❓ 常见问题

### Q: 子 Agent 执行失败怎么办？

A: 检查以下几点：
1. 确认编程工具已正确安装
2. 查看子 Agent 日志了解错误原因
3. 确保工作目录有写入权限
4. 尝试增加超时时间

### Q: 如何选择合适的编程工具？

A: 根据项目需求选择：
- **简单脚本/原型**: OpenCode
- **复杂业务逻辑**: Claude Code
- **多语言项目**: Codex
- **日常开发**: Cursor
- **VS Code 用户**: Continue

### Q: 子 Agent 最多可以并行运行多少个？

A: 默认最多 5 个，可在配置中调整 `maxSubagents` 参数。

### Q: 如何查看子 Agent 的详细日志？

A: 使用 `sessions_history` 命令查看指定会话的完整历史。

## 🔗 相关链接

- [ClawHub Skill 页面](https://clawhub.ai/skills/feishu-ai-coding-assistant)
- [使用教程（飞书文档）](https://www.feishu.cn/docx/HcQGd4wDsok2wTxOeWAcAXmEnje)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/openclaw-skills/feishu-ai-coding-assistant)
- [问题反馈](https://github.com/openclaw-skills/feishu-ai-coding-assistant/issues)

---

⭐ 如果这个 Skill 对你有帮助，请给个 Star！
