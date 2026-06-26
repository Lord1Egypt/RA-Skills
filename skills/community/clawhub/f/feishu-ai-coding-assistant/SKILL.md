# feishu-ai-coding-assistant

🤖 飞书 AI 编程助手 - 调用子 Agent 完成大型项目

## 版本要求

> **⚠️ 重要：本 Skill 需要以下版本支持**

| 版本 | 新增功能 |
|------|----------|
| **OpenClaw ≥ 2026.3.0** | 基础子代理功能（`sessions_spawn`, `subagents`） |
| **OpenClaw ≥ 2026.3.5** | ACP 编码模式支持 |
| **OpenClaw ≥ 2026.3.7** | Session History 持久化、Persistent Channel Bindings |

## 功能描述

本 Skill 提供一个完整的 AI 编程工作流，通过调用子 Agent 来完成大型项目开发任务。支持多种编程工具的选择和安装引导，包括 OpenCode、Claude Code、Codex 等，并支持 `subagent` 和 `acp` 两种运行时模式。

## 核心能力

### 1. 编程工具选择与安装（明确版本）

> **📅 版本更新时间：2026-03-10**

| 工具 | 最新版本 | 安装命令 | 适用场景 |
|------|---------|----------|----------|
| **OpenCode** | v1.2.24 | `npm install -g opencode@1.2.24` | 开源免费，SST 出品，基础代码生成 |
| **Claude Code** | v2.1.72 | `npm install -g @anthropic-ai/claude-code@2.1.72` | Anthropic 官方，强大推理，复杂逻辑 |
| **Codex** | v3.5.0 | `npm install -g openai-codex@3.5.0` | 多语言支持，全栈开发 |
| **Cursor** | v0.40.0 | `npm install -g cursor-cli@0.40.0` | 编辑器集成，日常开发 |
| **Continue** | v0.8.0 | `npm install -g continue-dev@0.8.0` | VS Code 插件，轻量级 |

### 2. 子 Agent 管理

#### 支持两种 Runtime

| Runtime | 用途 | 特点 | 版本要求 |
|---------|------|------|----------|
| **subagent** | 通用任务 | 继承主代理能力，适合研究、分析、写作 | ≥ 2026.3.7 |
| **acp** | 编码任务 | 专业编码环境，支持 Claude Code、Codex 等 | ≥ 2026.3.7 |

#### 支持两种 Mode

| Mode | 说明 | 适用场景 |
|------|------|----------|
| **run** | 一次性任务 | 执行完毕后自动结束 |
| **session** | 持久会话 | 需要多次交互、持续对话的任务 |

#### 核心功能
- ✅ 创建专用编程子 Agent 会话
- ✅ 支持 `thread: true` 绑定到当前对话线程
- ✅ Session History 持久化（服务重启后可恢复）
- ✅ Persistent Channel Bindings（消息自动路由）
- ✅ 监控子 Agent 执行进度
- ✅ 收集子 Agent 输出结果

### 3. 项目工作流

```
步骤 1: 需求分析 → 步骤 2: 工具选择 → 步骤 3: 子 Agent 创建 → 步骤 4: 执行监控 → 步骤 5: 结果整合
```

- 需求分析与任务拆解
- 代码生成与审查
- 测试用例编写
- 文档自动生成

## 使用场景

| 场景 | 推荐 Runtime | 推荐 Mode | 说明 |
|------|-------------|-----------|------|
| 大型项目开发 | acp | session | 拆分多个子任务并行处理 |
| 代码重构 | acp | session | 分析现有代码结构，生成重构方案 |
| 技术栈迁移 | acp | session | 协助从一种技术栈迁移到另一种 |
| 自动化测试 | subagent | run | 生成测试用例并执行 |
| 文档生成 | subagent | run | 根据代码自动生成 API 文档 |
| 研究分析 | subagent | run | 搜索资料、整理笔记 |

## 使用方法

### 基础命令

```
/ai-coding 启动 AI 编程助手
```

### 交互式引导流程

**步骤 1: 选择编程工具**
```
请选择你要使用的编程工具：
1. OpenCode (v1.2.24) - 开源免费，SST 出品，适合基础代码生成
2. Claude Code (v2.1.72) - Anthropic 官方，强大推理，适合复杂逻辑
3. Codex (v3.5.0) - 多语言支持，适合全栈开发
4. Cursor (v0.40.0) - 编辑器集成，适合日常开发
5. Continue (v0.8.0) - VS Code 插件，轻量级选择
```

**步骤 2: 选择运行时**
```
请选择任务类型：
1. 编码任务 → 使用 ACP 模式（专业编码环境）
2. 研究/分析/写作 → 使用 Subagent 模式（通用任务）
```

**步骤 3: 选择模式**
```
请选择执行模式：
1. 一次性任务 (run) - 执行完毕后自动结束
2. 持久会话 (session) - 需要多次交互
```

**步骤 4: 确认安装**
- 自动检测已安装的工具
- 提供一键安装命令
- 验证安装是否成功

**步骤 5: 创建子 Agent**
- 配置子 Agent 参数（超时、模型、工作目录等）
- 设置 `thread: true` 绑定到当前对话
- 分配具体任务

**步骤 6: 执行与监控**
- 实时查看子 Agent 进度
- 使用 `steer` 引导方向
- 接收完成通知
- 获取输出结果

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `defaultTool` | string | "claude-code" | 默认编程工具 |
| `defaultRuntime` | string | "acp" | 默认运行时（acp/subagent） |
| `autoInstall` | boolean | true | 自动安装缺失工具 |
| `subagentTimeout` | number | 3600 | 子 Agent 超时时间（秒） |
| `maxSubagents` | number | 5 | 最大并行子 Agent 数量 |
| `workspace` | string | "./workspace" | 默认工作目录 |
| `threadBound` | boolean | true | 是否绑定到当前对话线程 |

## 输出格式

### 工具安装状态
```json
{
  "tool": "claude-code",
  "version": "2.0.0",
  "installed": true,
  "path": "/usr/local/bin/claude-code"
}
```

### 子 Agent 任务状态
```json
{
  "sessionId": "sess_xxx",
  "runtime": "acp",
  "mode": "session",
  "status": "running",
  "progress": 45,
  "currentTask": "生成 API 接口代码",
  "estimatedTime": "5 分钟",
  "threadBound": true
}
```

### 项目完成报告
```json
{
  "projectId": "proj_xxx",
  "status": "completed",
  "filesGenerated": 24,
  "testsPassed": 156,
  "documentationGenerated": true,
  "outputPath": "/workspace/project-output"
}
```

## 依赖项

- Node.js >= 18.0.0
- npm >= 9.0.0
- Git >= 2.30.0
- OpenClaw >= 2026.3.7
- 所选编程工具的 CLI

## 最佳实践

### 1. 任务拆分原则

**好的拆分：**
- ✅ 任务边界清晰
- ✅ 依赖关系明确
- ✅ 可独立执行
- ✅ 结果可验证

**不好的拆分：**
- ❌ 任务过于模糊
- ❌ 强耦合，必须同步
- ❌ 依赖主代理频繁干预
- ❌ 无法判断完成标准

### 2. 选择合适的 Runtime

| 任务类型 | 推荐 Runtime | 原因 |
|----------|-------------|------|
| 编程/代码生成 | `acp` | 专业编码环境，支持文件操作 |
| 研究分析 | `subagent` | 通用能力强，适合文本任务 |
| 文档写作 | `subagent` | 无需文件系统，文本处理即可 |
| 项目初始化 | `acp` | 需要创建文件、运行命令 |

### 3. 任务描述技巧

**好的任务描述示例：**
```
使用 Next.js 14 + TypeScript 创建一个博客系统：

1. 功能需求：
   - 文章列表页（分页）
   - 文章详情页
   - Markdown 支持
   - 标签分类

2. 技术要求：
   - 使用 App Router
   - Tailwind CSS 样式
   - 响应式设计

3. 输出：
   - 完整的项目代码
   - README 文档
```

**不好的任务描述：**
```
帮我写个博客
```

### 4. 监控和管理

**定期检查：**
1. 每隔一段时间执行 `subagents list`
2. 查看各子代理状态和进度
3. 发现问题及时 `steer` 或 `kill`

**主动引导：**
当子代理方向偏离时，使用 `steer` 发送指导信息

## 注意事项

1. **子 Agent 资源消耗** - 每个子 Agent 会独立消耗 API 配额，请注意监控
2. **并发限制** - 建议控制并发子代理数量（通常 2-5 个）
3. **超时设置** - 长时间任务请设置合理的超时时间
4. **安全审查** - 生成的代码建议进行人工审查后再部署
5. **版本兼容** - 确保 OpenClaw 版本 ≥ 2026.3.7

## 版本历史

- **v1.0.0** (2026-03-10) - 初始版本
  - 支持 5 种编程工具（明确版本）
  - 支持 subagent 和 acp 两种运行时
  - 支持 run 和 session 两种模式
  - Session History 持久化支持
  - Persistent Channel Bindings 支持
  - 子 Agent 创建与管理
  - 基础项目工作流

## 作者

OpenClaw Skill Master

## 许可证

MIT

## 相关链接

- [OpenClaw 子代理使用教程](https://my.feishu.cn/docx/IgkrdJvgxowAuMxAAkAcDaCOntf)
- [ClawHub](https://clawhub.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
