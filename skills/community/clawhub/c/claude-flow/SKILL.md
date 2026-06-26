---
name: claude-flow
description: Claude Code 多智能体编排平台，部署 100+ 专业 AI 智能体协同工作，通过蜂群拓扑（层级/网状/环形/星形）协调自主工作流，内置自学习、向量记忆和原生 MCP 集成
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npx
    emoji: 🌊
    homepage: https://github.com/ruvnet/claude-flow
---

# Claude-Flow — Claude Code 多智能体编排平台

Claude-Flow（现更名为 Ruflo）是专为 Claude Code 设计的企业级多智能体编排框架，将 Claude Code 变成强大的多智能体开发平台。通过 MCP 原生集成，可在 Claude Code 会话中直接协调 100+ 专业智能体（coder、tester、reviewer、architect、security 等），智能体通过蜂群拓扑自组织，支持层级（Queen/Worker）或网状（P2P）协作模式，并具备持续自学习能力。

## 核心使用场景

- **复杂软件工程任务**：自动分解大型任务，分配给专业智能体并行处理
- **代码审查与安全审计**：同时运行 reviewer、security、tester 智能体进行全面检查
- **架构设计**：architect 智能体协调 researcher、analyst 智能体完成技术选型
- **自动化测试**：tester 智能体批量生成和执行测试，optimizer 智能体分析结果
- **文档生成**：documenter 智能体并发处理多个模块的文档

## AI 辅助使用流程

1. **一键安装** — AI 执行 `npx ruflo@latest init --wizard` 完成 Claude Code MCP 集成
2. **选择智能体** — AI 根据任务选择合适的专业智能体类型
3. **启动蜂群** — AI 启动智能体蜂群，自动设置 Queen/Worker 拓扑
4. **监控协调** — AI 实时查看智能体状态和任务分配
5. **收集成果** — 智能体协作完成后，Queen 整合所有工作成果
6. **知识复用** — 成功模式自动存入向量记忆，未来同类任务直接复用

## 关键章节导航

- [安装指南](guides/01-installation.md) — npx 安装、MCP 配置、Claude Code 集成
- [快速开始](guides/02-quickstart.md) — 启动智能体、蜂群模式、对话驱动编排
- [高级用法](guides/03-advanced-usage.md) — 自定义智能体、多模型切换、向量记忆、插件
- [故障排查](troubleshooting.md) — MCP 连接、智能体超时、记忆数据库

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 安装 Claude-Flow 并配置 Claude Code MCP 集成
- ✅ 启动和配置专业智能体（coder、tester、reviewer 等）
- ✅ 组建蜂群，设置 Queen/Worker 层级拓扑
- ✅ 分解复杂任务并分配给最合适的智能体
- ✅ 监控智能体状态和任务进度
- ✅ 查询和利用智能体向量记忆中存储的成功模式
- ✅ 切换不同 LLM 提供商（Claude/GPT/Gemini/Ollama）

## 核心功能

- ✅ **100+ 专业智能体** — 涵盖 coder、tester、reviewer、architect、security 等角色
- ✅ **蜂群协调** — 层级（Queen/Worker）、网状（P2P）、环形、星形拓扑
- ✅ **容错共识** — Raft、Byzantine、Gossip 三种共识算法
- ✅ **自学习记忆** — HNSW 向量搜索 + SQLite 持久化，成功模式自动复用
- ✅ **MCP 原生集成** — 310+ MCP 工具，直接在 Claude Code 中使用
- ✅ **多 LLM 支持** — Claude/GPT/Gemini/Cohere/Ollama，自动故障切换
- ✅ **WASM 优化引擎** — 简单任务跳过 LLM 调用（<1ms），Token 压缩 30-50%
- ✅ **安全防护** — 内置提示注入防护、路径遍历防护、命令注入拦截
- ✅ **插件系统** — 自定义 Worker、Hook、Provider，IPFS 市场分发

## 快速示例

```bash
# 一键安装（推荐）
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash

# 或通过 npx
npx ruflo@latest init --wizard

# 启动 Claude Code MCP 服务器
npx ruflo@latest mcp start

# 查看可用智能体
npx ruflo@latest agent list

# 启动蜂群处理复杂任务
npx ruflo@latest swarm start --topology hierarchical --agents coder,tester,reviewer
```

在 Claude Code 对话中直接使用：
```
# 直接描述任务，Claude-Flow 自动路由到合适智能体
帮我审查 src/auth/ 目录的安全性，需要代码审查、安全扫描和测试覆盖率检查
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Node.js | >= 18.0 |
| Claude Code | 最新版 |
| npm/npx | 任意版本 |
| Anthropic API Key | 必需（用于 Claude） |

## 项目链接

- GitHub：https://github.com/ruvnet/claude-flow
- npm：https://www.npmjs.com/package/claude-flow
- Discord：https://discord.com/invite/dfxmpwkG2D
