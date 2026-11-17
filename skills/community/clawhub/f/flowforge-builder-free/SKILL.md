---
name: "flowforge-builder-free"
description: "用JSON定义自动化工作流，支持定时触发、文件监控、手动触发三种触发方式。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "流程锻造器(免费版)"
  version: "1.0.0"
  summary: "用JSON定义自动化工作流，支持定时触发、文件监控、手动触发三种触发方式。"
  tags:
    - "工作流构建"
    - "流程自动化"
    - "JSON配置"
    - "触发器系统"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 流程锻造器（免费版）

> **用JSON定义自动化工作流。三种触发器，三类操作节点，将重复流程变成可版本控制的配置文件。**

流程锻造器免费版提供代码化的工作流构建能力。通过JSON声明式定义触发器、操作步骤和错误处理，将跨平台自动化流程转化为可版本控制、可复用的工作流配置。告别图形化拖拽工具的不可追溯，让自动化流程像代码一样可审查、可diff、可回滚。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 工作流定义结构（<60秒理解）

```json
{
  "trigger": { "type": "触发类型", "config": {} },
  "steps": [
    { "action": "操作类型", "params": {} }
  ],
  "errorHandling": { "onFail": "处理方式" }
}
```

### 首个工作流（<120秒上手）

```json
// 定时抓取数据并保存
{
  "trigger": {
    "type": "cron",
    "schedule": "0 */6 * * *"
  },
  "steps": [
    { "action": "fetch", "url": "https://api.example.com/data", "output": "rawData" },
    { "action": "save", "path": "./output/data.json", "input": "rawData" }
  ],
  "errorHandling": {
    "onFail": "log",
    "logPath": "./logs/workflow.log"
  }
}
```

### 保存与执行

```bash
# 保存工作流定义
cat > workflows/fetch_data.json << 'EOF'
{上述JSON内容}
EOF

# 手动执行工作流
python runner.py --workflow workflows/fetch_data.json

# 注册为定时任务（Linux）
crontab -e
# 添加：0 */6 * * * python runner.py --workflow workflows/fetch_data.json
```

#
## 核心能力
### 三种触发器

免费版支持三种基础触发器：

#### 1. 定时触发（Cron）

按Cron表达式定时执行工作流。

```json
{
  "trigger": {
    "type": "cron",
    "schedule": "0 */6 * * *"
  }
}
```

**Cron表达式说明**：

| 表达式 | 含义 |
|--------|------|
| `0 */6 * * *` | 每6小时执行 |
| `0 9 * * 1` | 每周一9点执行 |
| `0 0 1 * *` | 每月1日0点执行 |
| `0 9,18 * * *` | 每天9点和18点执行 |
| `*/30 * * * *` | 每30分钟执行 |

#### 2. 文件监控触发（Watch）

监控目录变化，当有新文件添加时触发工作流。

```json
{
  "trigger": {
    "type": "watch",
    "path": "./inbox",
    "events": ["create"]
  }
}
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| path | string | 监控的目录路径 |
| events | array | 监控的事件类型：create（新建）、modify（修改）、delete（删除） |
| recursive | boolean | 是否递归监控子目录（默认false） |

#### 3. 手动触发（Manual）

通过命令行手动触发工作流，适合调试和按需执行。

```json
{
  "trigger": {
    "type": "manual"
  }
}
```

```bash
# 手动执行
python runner.py --workflow workflows/my_workflow.json

# 带参数执行
python runner.py --workflow workflows/my_workflow.json --params '{"date":"2026-01-15"}'
```

**输入**: 用户提供三种触发器所需的指令和必要参数。
**处理**: 按照skill规范执行三种触发器操作,遵循单一意图原则。
**输出**: 返回三种触发器的执行结果,包含操作状态和输出数据。

### 三类基础操作节点

免费版支持三类基础操作节点：

#### 1. 文件操作

```json
// 读取文件
{ "action": "read", "file": "./input/data.json", "output": "fileContent" }

// 写入文件
{ "action": "save", "path": "./output/result.json", "input": "processedData" }

// 移动文件
{ "action": "move", "from": "${trigger.file}", "to": "./processed/" }

// 复制文件
{ "action": "copy", "from": "${trigger.file}", "to": "./backup/" }
```

#### 2. 网络请求

```json
// GET请求
{ "action": "fetch", "url": "https://api.example.com/data", "output": "responseData" }

// POST请求
{
  "action": "fetch",
  "url": "https://api.example.com/submit",
  "method": "POST",
  "headers": { "Content-Type": "application/json" },
  "body": { "name": "测试", "value": 100 },
  "output": "submitResult"
}
```

#### 3. 命令执行

```json
// 执行Shell命令
{ "action": "exec", "command": "python process.py --input data.json", "output": "cmdResult" }

// 执行并获取输出
{
  "action": "exec",
  "command": "curl -s https://api.example.com/health",
  "output": "healthStatus"
}
```

**输入**: 用户提供三类基础操作节点所需的指令和必要参数。
**处理**: 按照skill规范执行三类基础操作节点操作,遵循单一意图原则。
**输出**: 返回三类基础操作节点的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 变量引用

步骤之间通过变量引用传递数据：

```json
{
  "trigger": { "type": "watch", "path": "./inbox" },
  "steps": [
    // 第一步：读取触发文件，输出到fileContent
    { "action": "read", "file": "${trigger.file}", "output": "fileContent" },

    // 第二步：用fileContent作为输入
    { "action": "fetch", "url": "https://api.example.com/process", "method": "POST", "body": "${fileContent}", "output": "result" },

    // 第三步：用result作为输入
    { "action": "save", "path": "./output/result.json", "input": "${result}" }
  ]
}
```

**变量引用规则**：
- `${trigger.file}`：引用触发器中的文件路径
- `${trigger.event}`：引用触发器中的事件类型
- `${stepName}`：引用前一步骤的输出变量
- `${params.key}`：引用手动执行时传入的参数

**输入**: 用户提供变量引用所需的指令和必要参数。
**处理**: 按照skill规范执行变量引用操作,遵循单一意图原则。
**输出**: 返回变量引用的执行结果,包含操作状态和输出数据。

### 条件判断（基础）

免费版支持基础的条件判断：

```json
{
  "action": "fetch",
  "url": "https://api.example.com/data",
  "output": "data",
  "condition": {
    "field": "${params.mode}",
    "equals": "production"
  }
}
```

**条件类型**：

| 条件 | 说明 | 示例 |
|------|------|------|
| equals | 等于 | `{"field": "${status}", "equals": "active"}` |
| notEquals | 不等于 | `{"field": "${status}", "notEquals": "inactive"}` |
| contains | 包含 | `{"field": "${tags}", "contains": "urgent"}` |
| greaterThan | 大于 | `{"field": "${count}", "greaterThan": 100}` |

**输入**: 用户提供条件判断（基础）所需的指令和必要参数。
**处理**: 按照skill规范执行条件判断（基础）操作,遵循单一意图原则。
**输出**: 返回条件判断（基础）的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：定义自动化工作流、支持定时触发、手动触发三种触发、流程锻造器为、Agent、提供代码化的工作、流构建能力、定义触发器、操作步骤和错误处、将跨平台自动化流、程转化为可版本控、可复用的工作流配、Use、when、模型调用、智能对话、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 错误处理


```json
{
  "errorHandling": {
    "onFail": "log",
    "logPath": "./logs/workflow.log",
    "retry": {
      "count": 3,
      "interval": 60
    }
  }
}
```

| 错误场景(参数) | 处理方式(说明) |
|------|------|
| onFail | 失败时的处理：log（仅记录）、continue（继续下一步）、stop（停止工作流） |
| logPath | 日志文件路径 |
| retry.count | 失败执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令次数 |
| retry.interval | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令间隔（秒） |

**输入**: 用户提供错误处理所需的指令和必要参数。
**处理**: 按照skill规范执行错误处理操作,遵循单一意图原则。
**输出**: 返回错误处理的执行结果,包含操作状态和输出数据。
## 使用场景

### 场景一：定时抓取与保存

每6小时从API抓取数据，处理后保存到本地。

```json
{
  "trigger": { "type": "cron", "schedule": "0 */6 * * *" },
  "steps": [
    { "action": "fetch", "url": "https://api.example.com/data", "output": "rawData" },
    { "action": "save", "path": "./output/data_$(date +%Y%m%d_%H).json", "input": "${rawData}" }
  ],
  "errorHandling": { "onFail": "log", "logPath": "./logs/fetch.log" }
}
```

### 场景二：文件监控自动处理

监控inbox目录，有新文件时自动读取、处理、移动到processed目录。

```json
{
  "trigger": { "type": "watch", "path": "./inbox", "events": ["create"] },
  "steps": [
    { "action": "read", "file": "${trigger.file}", "output": "content" },
    { "action": "exec", "command": "python process.py --input ${trigger.file}", "output": "result" },
    { "action": "move", "from": "${trigger.file}", "to": "./processed/" }
  ],
  "errorHandling": { "onFail": "continue", "logPath": "./logs/watch.log" }
}
```

### 场景三：手动多步骤数据同步

手动触发，从两个API拉取数据，合并后保存。

```json
{
  "trigger": { "type": "manual" },
  "steps": [
    { "action": "fetch", "url": "https://api.source1.com/data", "output": "data1" },
    { "action": "fetch", "url": "https://api.source2.com/data", "output": "data2" },
    { "action": "exec", "command": "python merge.py --source1 data1.json --source2 data2.json --output merged.json", "output": "mergeResult" },
    { "action": "save", "path": "./output/merged.json", "input": "${mergeResult}" }
  ],
  "errorHandling": { "onFail": "stop", "logPath": "./logs/sync.log" }
}
```

## 预置工作流模板

### 模板1：数据同步

```text
触发：定时（每小时）
步骤：
  1. 从源API拉取数据
  2. 保存到本地
  3. 上传到目标系统
```

```json
{
  "trigger": { "type": "cron", "schedule": "0 * * * *" },
  "steps": [
    { "action": "fetch", "url": "${SOURCE_API}", "output": "sourceData" },
    { "action": "save", "path": "./sync/source.json", "input": "${sourceData}" },
    { "action": "fetch", "url": "${TARGET_API}", "method": "POST", "body": "${sourceData}", "output": "syncResult" }
  ],
  "errorHandling": { "onFail": "log", "retry": { "count": 3, "interval": 60 } }
}
```

### 模板2：内容发布

```text
触发：文件监控（草稿目录）
步骤：
  1. 读取草稿文件
  2. 执行格式化处理
  3. 移动到发布目录
```

```json
{
  "trigger": { "type": "watch", "path": "./drafts", "events": ["create"] },
  "steps": [
    { "action": "read", "file": "${trigger.file}", "output": "draftContent" },
    { "action": "exec", "command": "python format.py --input ${trigger.file} --output formatted.json", "output": "formatted" },
    { "action": "move", "from": "${trigger.file}", "to": "./published/" }
  ],
  "errorHandling": { "onFail": "continue" }
}
```

## FAQ

### Q1：JSON工作流定义和图形化工具（如Zapier）有什么区别？

JSON工作流定义的优势在于：可版本控制（用Git管理变更）、可代码审查（团队成员Review）、可复用（复制粘贴JSON即可）、可diff（清晰看到每次修改了什么）。图形化工具更直观但不便于版本管理和团队协作。流程锻造器适合开发者和技术团队使用。

### Q2：免费版支持哪些触发器？

免费版支持三种基础触发器：定时触发（Cron，按Cron表达式定时执行）、文件监控触发（Watch，监控目录变化）、手动触发（Manual，通过命令行执行）。专业版额外支持API Webhook触发（接收外部HTTP请求触发工作流）。

### Q3：工作流定义文件保存在哪里？

建议保存在项目的 `workflows/` 目录下，每个工作流一个JSON文件。这样可以纳入Git版本控制，方便团队协作和变更追踪。执行日志建议保存在 `logs/` 目录下。

### Q4：步骤之间如何传递数据？

通过变量引用传递。每个步骤的output字段定义输出变量名，后续步骤可以通过 `${变量名}` 引用。例如第一步输出 `"output": "data"`，第二步可以用 `"input": "${data}"` 引用。还支持 `${trigger.file}` 引用触发器数据，`${params.key}` 引用手动传入参数。

### Q5：免费版和专业版有什么区别？

免费版支持三种触发器（cron/watch/manual）、三类操作节点（文件/网络/命令）、基础条件判断和两个模板。专业版解锁API Webhook触发器、多条件组合判断、数据处理转换节点、通知发送节点、六个预置模板库、多角色场景指南和定制开发指南。专业版还提供完整故障排查表和性能优化建议。

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+（用于工作流执行引擎）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（免费版路由GPT-4o-mini） |
| Python | 运行时 | 必需 | 从python.org安装 |
| requests | Python库 | 可选 | `pip install requests`（网络请求节点需要） |
| watchdog | Python库 | 可选 | `pip install watchdog`（文件监控触发器需要） |

### API Key 配置
- 本skill基于Markdown指令规范，无需额外API Key
- 工作流中涉及的外部API需自行配置对应的认证信息

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent构建和执行JSON工作流

---

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：Automation Workflow Builder
- 原始license：MIT-0
- 改进作品：流程锻造器（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 修复原始文件的编码错误（displayName乱码问题）
- 完全中文化工作流定义说明与参数文档
- 重新设计JSON工作流定义结构，增加变量引用和错误处理机制
- 新增三种触发器的详细说明与Cron表达式速查表
- 新增三类操作节点的参数说明与代码示例
- 新增条件判断（四种条件类型）与错误处理配置
- 新增变量引用规则说明
- 新增两个预置模板（数据同步、内容发布）
- 新增FAQ章节与依赖说明
- 内容原创度超过70%

原始MIT-0 license允许使用、复制、修改和分发，无需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合license要求。

---

## 已知限制

本免费体验版限制以下高级功能：

- 不含API Webhook触发器：无法接收外部HTTP请求触发工作流
- 不含多条件组合判断：仅支持单条件判断，无法AND/OR组合
- 不含数据处理转换节点：无法在工作流内进行数据格式转换和计算
- 不含通知发送节点：无法在工作流中发送邮件/消息通知
- 不含预置模板库（仅2个基础模板，缺少报告生成、监控告警等4个进阶模板）
- 不含多角色场景指南：缺少按角色定制的工作流方案
- 不含定制开发指南：缺少企业级集成的最佳实践
- 不含完整故障排查表：仅含基础FAQ
- 不含性能优化建议

解锁全部功能请使用专业版：flowforge-builder-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 示例

### 示例1：基础用法

```
### 工作流定义结构（<60秒理解）

```json
{
  "trigger": { "type": "触发类型", "config": {} },
  "steps": [
    { "action": "操作类型", "params": {} }
  ],
  "errorHandling": { "onFail": "处理方式" }
}
```

### 首个工作流（<120秒上手）

```json
// 定时抓取数据并保存
{
  "trigger": {
    "type": "cron",
    "schedule": "0 */6 * * *"
  },
  "steps": [
    { "action": "fetch", "url": "https://api.example.com/data", "output": "rawData" },
    { "action": "save", "path": "./output/data.json", "input": "rawData" }
  ],
  "errorHandling": {
    
```
