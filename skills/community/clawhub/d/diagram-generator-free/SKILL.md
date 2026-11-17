---
slug: "diagram-generator-free"
name: "diagram-generator-free"
version: "1.0.0"
displayName: "Diagram基础版"
summary: "通过MCP工具生成基础Mermaid流程图与Draw.io架构图,适合快速文档化。diagram-generator 基础客户端(免费版)。通过 mcp-diagram-generator"
summary_zh: "通过MCP工具生成基础Mermaid流程图与Draw.io架构图,适合快速文档化。diagram-generator 基础客户端(免费版)。通过 mcp-diagram-generator"
license: "MIT"
description: "|-. 适用于需要diagram generator相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  diagram-generator 基础客户端(免费版)。通过 mcp-diagram-generator MCP 服务器将自然语言意图转换为 JSON 规范,
  生成 Mermaid 流程图与 Draw.io 架构图两种基础能力。支持默认输出路径、交互式采集、基础质量校验.
tags:
  - 研发工具
  - diagram
  - generator
  - automation
  - productivity
  - 工具
  - 效率
  - type
  - mermaid
  - json
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free
---
# Diagram Generator LITE

基础版图表生成客户端,通过 mcp-diagram-generator MCP 服务器生成 Mermaid 流程图与 Draw.io 架构图.
**范围外**(本技能不做): Excalidraw 白板手绘、网络拓扑、泳道、UML 时序/类/ER、自定义输出路径、复杂几何坐标控制(需升级付费版).
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Diagram基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 必需 MCP 工具

- `mcp__mcp-diagram-generator__generate_diagram`: 提交 JSON 规范生成图表
- `mcp__mcp-diagram-generator__get_config`: 查看输出目录配置

若工具缺失,需配置 MCP 服务器:
```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
# ...
# ...
**输入**: 用户提供必需 MCP 工具相关的配置参数、输入数据和处理选项.
# ...
### 支持的格式与图类型(基础)
# ...
| 图类型 | 默认格式 | 默认方向 |
|---:|---:|---:|
| 流程图 | Mermaid | 垂直 |
| 系统架构 | Draw.io | 垂直 |
# ...
> **升级提示**: Excalidraw 白板手绘、网络拓扑、泳道、UML 时序/类/ER、自定义输出路径、复杂几何坐标控制等高级能力仅在 diagram-generator 付费版中提供.
# ...
# ...
### 主工作流
# ...
# ...

- 参考`主工作流`的配置文档进行参数调优
### 采集意图
收集以下基础选项:
- 图类型(流程图或系统架构)
- 输出格式(Mermaid 或 Draw.io)
- 可选文件名
# ...

### 构建 JSON 规范
核心结构:
```json
{
  "format": "mermaid",
  "diagramType": "flowchart",
  "title": "图表标题",
  "elements": [
    { "id

**输入**: 用户提供主工作流相关的配置参数、输入数据和处理选项.
### 图类型

针对图类型,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供图类型相关的配置参数、输入数据和处理选项.
**输出**: 返回图类型的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`图类型`的配置文档进行参数调优
### 流程图

针对流程图,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供流程图相关的配置参数、输入数据和处理选项.
**输出**: 返回流程图的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`流程图`的配置文档进行参数调优

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 必需 MCP 工具(补充)

若工具缺失,需配置 MCP 服务器:
```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

## 支持的格式与图类型(基础)(补充)

| 图类型(续)| 默认格式 | 默认方向 |
|:-----:|:-----:|:-----:|
| 流程图 | Mermaid | 垂直 |
| 系统架构 | Draw.io | 垂直 |

## 主工作流(补充)

### 采集意图(补充)

收集以下基础选项:
- 图类型(流程图或系统架构)
- 可选文件名

### 构建 JSON 规范(补充)

核心结构:
```json
{
  "format": "mermaid",
  "diagramType": "flowchart",
  "title": "图表标题",
  "elements": [
    { "id": "node-1", "type": "node", "name": "开始" },
    { "id": "node-2", "type": "node", "name": "处理" },
    { "type": "edge", "source": "node-1", "target": "node-2" }
  ]
}
```

通用规则:
- `elements` 必须是数组
- ID 必须唯一
- 边必须为顶层元素
- 边的 `source` 与 `target` 必须指向已存在的节点

### 调用 MCP 工具生成

```json
{ "diagram_spec": "<规范对象>", "filename": "my-flowchart.mmd" }
```

服务器校验 schema 并写入默认目录 `diagrams/{format}/`.
## 适用场景

| 场景 | 典型输入 | 输出内容 |
|:------|------:|:------|
| 流程文档化 | 为用户注册流程画流程图 | Mermaid 流程图文件 |
| 基础架构图 | 为单体应用画架构图 | Draw.io 架构图文件 |

**不适用于**: Excalidraw 白板、网络拓扑、泳道、UML、自定义输出路径(需升级付费版)

## 使用流程

### 检查 MCP 工具可用性
确认 `mcp__mcp-diagram-generator__generate_diagram` 已注册。若缺失,按"必需 MCP 工具"章节配置.
### 采集意图(补充)(补充)
收集图类型(流程图/架构)与可选文件名.
### 构建规范
按 schema 构建 `elements` 数组,确保 ID 唯一与边引用有效.
### 调用生成
传入 `diagram_spec` 与可选 `filename`,服务器返回保存文件路径.
#
## 案例展示

### 案例一： 用户注册流程图
**场景**: 产品团队需要快速绘制用户注册流程的 Mermaid 流程图

构建规范:
```json
{
  "format": "mermaid",
  "diagramType": "flowchart",
  "title": "用户注册流程",
  "elements": [
    { "id": "start", "type": "node", "name": "开始" },
    { "id": "input", "type": "node", "name": "填写注册信息" },
    { "id": "check", "type": "node", "name": "校验唯一性" },
    { "id": "save", "type": "node", "name": "写入数据库" },
    { "id": "end", "type": "node", "name": "注册成功" },
    { "type": "edge", "source": "start", "target": "input" },
    { "type": "edge", "source": "input", "target": "check" },
    { "type": "edge", "source": "check", "target": "save" },
    { "type": "edge", "source": "save", "target": "end" }
  ]
}
```

调用: `{ "diagram_spec": "<上述规范>", "filename": "user-signup.mmd" }`

**输出**: `diagrams/mermaid/user-signup.mmd` 文件路径,可直接嵌入 markdown 渲染

**说明**: Mermaid 流程图代码仓库友好,生成后可直接复制到 markdown 代码块.
### 案例二： 单体应用架构图
**场景**: 开发者需要为新项目绘制基础分层架构图

构建规范:
```json
{
  "format": "drawio",
  "diagramType": "architecture",
  "title": "单体应用架构",
  "elements": [
    { "id": "web", "type": "node", "name": "Web 前端" },
    { "id": "api", "type": "node", "name": "API 服务" },
    { "id": "db", "type": "node", "name": "数据库" },
    { "type": "edge", "source": "web", "target": "api" },
    { "type": "edge", "source": "api", "target": "db" }
  ]
}
```

**输出**: `diagrams/drawio/monolith-arch.drawio` 文件路径

**说明**: 基础三层架构,节点平铺,边表示调用关系。复杂分层与显式几何坐标需升级付费版.
## 错误处理

| 错误场景 | 错误信息 | 原因分析 | 处理方式 |
|---:|:---|---:|---:|
| mcp_tool_missing | `mcp__mcp-diagram-generator__*` 未注册 | MCP 服务器未配置 | 配置 `mcp-diagram-generator` 服务器并重启 Agent |
| schema_validation_failed | `Error: schema validation failed` | ID 重复或边 source/target 无效 | 检查 ID 唯一性与边引用 |
| directory_error | `EACCES: permission denied` | 输出目录无写权限 | 检查目录权限,必要时 `init_config()` 重置 |
| wrong_extension | `File saved as .md` | `filename` 扩展名与格式不匹配 | Mermaid 用 `.mmd`、Draw.io 用 `.drawio` |
| edge_target_not_found | `Edge target "x" not found` | 边引用了不存在的 ID | 检查 ID 拼写,确保 source/target 已定义 |

## 常见问题

### Q1: 免费版支持哪些图类型?
A: 免费版(LITE)支持 Mermaid 流程图与 Draw.io 架构图两种基础能力。付费版(diagram-generator)额外提供 Excalidraw 白板手绘、网络拓扑、泳道、UML(时序/类/ER)、自定义输出路径、复杂几何坐标控制等高级能力.
### Q2: 如何配置 MCP 服务器?
A: 在 Agent 的 MCP 配置中添加 `mcp-diagram-generator` 条目,`command` 设为 `npx`,`args` 设为 `["-y", "mcp-diagram-generator"]`。配置后重启 Agent 环境。首次调用会创建默认输出目录 `diagrams/{format}/`.
### Q3: 生成的文件保存在哪里?
A: 默认保存到 `diagrams/{format}/` 目录下,`{format}` 为 `mermaid` 或 `drawio`。可通过 `filename` 参数指定文件名,但免费版不支持自定义完整输出路径(需升级付费版).
### Q4: Mermaid 文件如何嵌入 markdown?
A: 生成的 `.mmd` 文件内容可直接复制到 markdown 的 mermaid 代码块中渲染。这是代码仓库文档化的推荐方式.
## 已知限制

1. **基础格式**: 仅支持 Mermaid 与 Draw.io,不支持 Excalidraw(需升级付费版)
2. **基础图类型**: 仅支持流程图与架构图,不支持网络拓扑/泳道/UML(需升级付费版)
3. **默认输出路径**: 不支持自定义完整输出路径,仅支持 `filename` 参数
4. **依赖 MCP 服务器**: 必须配置 `mcp-diagram-generator`,无 MCP 环境无法使用
5. **生成质量取决于 prompt 描述**: 节点命名与连接描述越具体,结果越符合预期

---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> **想要 Excalidraw 白板、网络拓扑、泳道、UML 时序图?** 升级到 diagram-generator 付费版解锁全部高级能力.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Diagram基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "diagram-generator"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
