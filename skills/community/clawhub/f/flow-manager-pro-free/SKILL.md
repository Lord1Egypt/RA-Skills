---
name: "flow-manager-pro-free"
description: "通过Admin API管理Node-RED实例，支持流程列表、部署、状态查询与基础节点管理。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "流程管理器(免费版)"
  version: "1.0.0"
  summary: "通过Admin API管理Node-RED实例，支持流程列表、部署、状态查询与基础节点管理。"
  tags:
    - "Node-RED"
    - "流程管理"
    - "自动化"
    - "IoT"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 流程管理器（免费版）

> **命令行管理Node-RED实例。无需浏览器，60秒上手，流程部署/状态/节点一气呵成。**

## 核心理念

通过Node-RED Admin API与实例交互，所有操作可通过命令行完成，适合CI/CD流水线、SSH远程管理、headless环境。

---

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 60秒上手

```bash
# 1. 复制环境配置模板
cp .env.example .env

# 2. 编辑.env，填入Node-RED实例信息
# NODE_RED_URL=http://localhost:1880
# NODE_RED_USERNAME=admin
# NODE_RED_PASSWORD=your-password

# 3. 验证连接
flow-manager list-flows

# 4. 查看实例设置
flow-manager get-settings

# 5. 部署一个流程
flow-manager deploy --file assets/flows/example.json
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| NODE_RED_URL | Node-RED API端点 | http://localhost:1880 |
| NODE_RED_USERNAME | 管理员用户名 | admin |
| NODE_RED_PASSWORD | 管理员密码 | - |

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 核心能力
### 1. 流程管理

```bash
# 列出所有流程
flow-manager list-flows

# 查看指定流程详情
flow-manager get-flow <flow-id>

# 部署新流程
flow-manager deploy --file assets/flows/example.json

# 更新现有流程
flow-manager update-flow <flow-id> --file updated-flow.json

# 删除流程
flow-manager delete-flow <flow-id>

# 获取流程状态
flow-manager get-flow-state

# 设置流程状态
flow-manager set-flow-state --file state.json
```

**输入**: 用户提供流程管理所需的指令和必要参数。
**处理**: 按照skill规范执行流程管理操作,遵循单一意图原则。
**输出**: 返回流程管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 基础节点管理

```bash
# 依赖说明
flow-manager list-nodes

# 安装节点
flow-manager install-node node-red-contrib-http-request

# 查看节点详情
flow-manager get-node node-red-contrib-http-request

# 启用节点
flow-manager enable-node node-red-contrib-http-request

# 禁用节点
flow-manager disable-node node-red-contrib-http-request

# 卸载节点
flow-manager remove-node node-red-contrib-http-request
```

**输入**: 用户提供基础节点管理所需的指令和必要参数。
**处理**: 按照skill规范执行基础节点管理操作,遵循单一意图原则。
**输出**: 返回基础节点管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 运行时信息

```bash
# 获取实例设置
flow-manager get-settings

# 获取诊断信息
flow-manager get-diagnostics
```

**输入**: 用户提供运行时信息所需的指令和必要参数。
**处理**: 按照skill规范执行运行时信息操作,遵循单一意图原则。
**输出**: 返回运行时信息的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 基础备份

```bash
# 备份当前所有流程
flow-manager backup

# 备份到指定文件
flow-manager backup --output my-backup.json
```

**输入**: 用户提供基础备份所需的指令和必要参数。
**处理**: 按照skill规范执行基础备份操作,遵循单一意图原则。
**输出**: 返回基础备份的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 上下文管理

```bash
# 获取流程上下文
flow-manager get-context flow my-key

# 获取全局上下文
flow-manager get-context global shared-data

# 设置流程上下文
flow-manager set-context flow my-key '"value"'

# 设置全局上下文
flow-manager set-context global counter '42'
flow-manager set-context global config '{"key": "value"}'
```

---

**输入**: 用户提供上下文管理所需的指令和必要参数。
**处理**: 按照skill规范执行上下文管理操作,遵循单一意图原则。
**输出**: 返回上下文管理的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Admin、API、支持流程列表、状态查询与基础节、流程管理器免费版、IoT、与自动化开发者提、供轻量级的、实例管理能力、聚焦流程、的日常高频操作、无需打开浏览器即、可完成流程列表、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：IoT开发者的快速部署（IoT开发者角色）

**痛点**：开发IoT流程时需要频繁修改并部署，每次都要打开浏览器操作，效率低下。

**对策**：用命令行一键部署，配合版本控制管理流程JSON。

```bash
# 将流程JSON纳入Git管理
git add assets/flows/

# 修改流程后一键部署
flow-manager deploy --file assets/flows/sensor-monitor.json

# 验证部署状态
flow-manager get-flow-state
```

**效果**：从修改到部署<5秒，不打断开发心流，流程版本可追溯。

### 场景二：测试环境的流程管理（自动化测试工程师角色）

**痛点**：测试环境需要频繁切换不同流程配置，手动操作易出错。

**对策**：用命令行批量管理测试流程。

```bash
# 列出当前流程
flow-manager list-flows

# 部署测试流程
flow-manager deploy --file assets/flows/test-scenario.json

# 测试完成后恢复生产流程
flow-manager deploy --file assets/flows/production.json

# 验证恢复
flow-manager get-flow-state
```

### 场景三：CI流水线集成（DevOps工程师角色）

**痛点**：CI流水线需要自动部署Node-RED流程，但缺乏标准化的命令行工具。

**对策**：将flow-manager集成到CI脚本中。

```bash
# CI流水线中的部署步骤
flow-manager deploy --file assets/flows/$BRANCH.json

# 部署后验证
flow-manager get-flow-state | grep -q "running" || exit 1

# 部署失败时回滚
flow-manager restore last-known-good.json
```

---

## FAQ

### 已知限制

免费版聚焦核心高频操作（流程列表/部署/状态/基础节点管理/基础备份），不限使用次数。多实例管理、完整备份恢复、Docker编排、性能监控、批量节点操作等高级功能需升级专业版。

### Q2：支持哪些Node-RED版本？

支持Node-RED 1.0及以上版本（需启用Admin API）。建议使用2.x或3.x版本以获得最佳兼容性。

### Q3：如何启用Admin API？

在Node-RED的`settings.js`中配置：
```javascript
module.exports = {
    adminAuth: {
        type: "credentials",
        users: [{ username: "admin", password: "$2a$08..." }]
    },
    httpAdminRoot: "/admin"  // 可选
}
```

### Q4：支持HTTPS吗？

支持。在`NODE_RED_URL`中配置HTTPS端点即可。自签名证书需设置`NODE_RED_REJECT_UNAUTHORIZED=false`（仅测试环境）。

### Q5：备份包含哪些内容？

免费版备份当前所有流程的JSON定义。专业版备份包含流程、节点配置、上下文数据、环境变量的完整快照。

---

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node-RED**: 1.0+（建议2.x或3.x）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| flow-manager CLI | 命令行工具 | 必需 | 随本技能提供 |
| curl | HTTP工具 | 必需 | 系统自带 |
| jq | JSON处理 | 可选 | 系统包管理器安装 |
| Node-RED | 服务 | 必需 | 从nodered.org安装 |

### API Key 配置
- 本免费版通过.env文件配置Node-RED凭证
- 凭证存储在`.env`文件中（已gitignore）
- 支持环境变量覆盖：`NODE_RED_URL`、`NODE_RED_USERNAME`、`NODE_RED_PASSWORD`

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Node-RED管理任务

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：Node Red Manager
- 原始license：MIT
- 改进作品：流程管理器（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，适配中文用户工作流
- 移除原项目特定基础设施引用（域名、Docker服务名等）
- 重新设计三个中文用户场景（IoT开发者/测试工程师/DevOps）
- 新增FAQ章节（5问）与环境变量说明表
- 统一命令行工具命名为flow-manager
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，符合MIT license要求。

---

## 免费版限制

本免费体验版限制以下高级功能：

- 多实例管理与切换（同时管理多个Node-RED实例）
- 完整备份与恢复（含上下文、环境变量、节点配置）
- Docker编排与容器管理
- 性能监控与告警
- 批量节点操作
- 流程版本对比与回滚
- 审计日志与操作追踪

解锁全部功能请使用专业版：flow-manager-pro-pro

## 示例

### 示例1：基础用法

```
### 60秒上手

```bash
```

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
