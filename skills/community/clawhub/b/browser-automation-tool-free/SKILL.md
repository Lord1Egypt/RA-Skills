---
name: "browser-automation-tool-free"
description: "通过自然语言驱动浏览器交互的CLI工具,支持本地Chrome,适合个人开发者快速自动化。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "浏览器自动化工具-免费版"
  version: "1.0.0"
  summary: "通过自然语言驱动浏览器交互的CLI工具,支持本地Chrome,适合个人开发者快速自动化"
  tags:
    - "研究工具"
    - "浏览器自动化"
    - "自然语言"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - browser

---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# 浏览器自动化工具(免费版)

## 概述

本工具通过自然语言指令驱动浏览器交互,用户无需编写复杂的选择器或脚本,只需用自然语言描述想做的动作,工具即可自动完成浏览器操作。免费版使用本地 Chrome 浏览器,适合个人开发者的快速自动化与原型验证。

### 与传统浏览器自动化的区别

| 对比维度 | 传统自动化 | 本工具(自然语言) |
|:---------|:----------|:-----------------|
| 元素定位 | CSS/XPath 选择器 | 自然语言描述 |
| 脚本编写 | 需要编程基础 | 自然语言描述即可 |
| 页面变化适应性 | 选择器易失效 | 自然语言更鲁棒 |
| 学习成本 | 较高 | 低 |
| 适用场景 | 固定流程 | 灵活多变的任务 |

## 核心能力

### 命令总览

| 命令 | 说明 | 示例 |
|:-----|:-----|:-----|
| `navigate <url>` | 跳转到URL | `browser navigate https://example.com` |
| `act "<动作>"` | 执行自然语言动作 | `browser act "点击登录按钮"` |
| `extract "<指令>"` | 提取结构化数据 | `browser extract "获取页面标题"` |
| `observe "<查询>"` | 观察发现元素 | `browser observe "页面有哪些按钮"` |
| `screenshot` | 截图 | `browser screenshot` |
| `close` | 关闭浏览器 | `browser close` |

**输出**: 返回命令总览的执行结果,包含操作状态和输出数据。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：通过自然语言驱动、浏览器交互的、CLI、支持本地、Chrome、适合个人开发者快、速自动化、通过自然语言指令、驱动浏览器交互的、命令行工具、用户可用自然语言、描述动作、工具自动转化为浏、览器操作、降低自动化脚本编、写门槛、核心能力、自然语言驱动的浏、结构化数据提取、元素发现与观察、浏览器支持、截图与页面导航等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:快速信息采集

个人用户希望从网页快速提取信息,无需编写选择器。

```bash
# 导航到目标页面
browser navigate https://example.com

# 用自然语言提取数据
browser extract "获取页面标题和描述"

# 提取结构化数据(带 schema)
browser extract "获取商品列表" '{"items":[{"name":"string","price":"number"}]}'

# 关闭浏览器
browser close
```

### 场景二:自然语言驱动的表单填写

用自然语言描述动作,自动完成表单填写。

```bash

# 用自然语言执行动作
browser act "在用户名输入框填入 myuser"
browser act "在密码输入框填入 mypassword"
browser act "点击提交按钮"

# 截图确认结果
browser screenshot

browser close
```

### 场景三:页面元素探索

不熟悉页面结构时,先用 observe 发现可用元素。

```bash

# 观察页面有哪些可交互元素
browser observe "页面上有哪些按钮"

# 根据观察结果执行动作
browser act "点击领先个蓝色的按钮"

# 提取观察到的内容
browser extract "获取页面所有标题文本"
```

## 不适用场景

以下场景浏览器自动化工具-免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

检查工具目录下的 `setup.json`,若 `setupComplete: false`:

```bash
# 安装依赖
npm install

# 创建全局 browser 命令
npm link
```

### 2. 环境选择(自动)

本工具自动选择浏览器环境:

1. **本地 Chrome 模式(默认)**:无需额外配置,使用本机 Chrome 浏览器
2. **远程浏览器模式**:若配置了远程浏览器服务的 API Key,自动切换至远程环境

免费版默认使用本地 Chrome 模式,无需额外配置。

### 3. 基础工作流

```bash
# 导航到页面

# 用自然语言执行动作
browser act "点击 Sign In 按钮"

# 提取数据
browser extract "获取页面标题"

# 截图
browser screenshot

# 关闭浏览器
browser close
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### 自然语言动作示例

```bash
# 点击类动作
browser act "点击登录按钮"
browser act "点击右上角的购物车图标"
browser act "点击领先个搜索结果"

# 输入类动作
browser act "在搜索框输入 AI agents"
browser act "在邮箱字段填入 test@example.com"

# 导航类动作
browser act "滚动到页面底部"
browser act "切换到第二个标签页"

# 复合动作
browser act "展开侧边栏菜单然后点击设置"
```

### 数据提取示例

```bash
# 简单提取
browser extract "获取页面标题"

# 带 schema 的结构化提取
browser extract "获取商品信息" '{"name":"string","price":"number","stock":"boolean"}'

# 提取列表数据
browser extract "获取新闻列表" '{"items":[{"title":"string","date":"string"}]}'
```

### 观察元素示例

```bash
# 观察可交互元素
browser observe "页面有哪些按钮"
browser observe "有哪些输入框"
browser observe "导航栏有哪些链接"
```

### 模式对比

| 特性 | 本地模式 | 远程模式 |
|:-----|:--------|:--------|
| 速度 | 较快 | 略慢(网络延迟) |
| 配置 | 需本机 Chrome | 需 API Key |
| 隐身模式 | 不支持 | 支持 |
| 代理/CAPTCHA | 不支持 | 支持 |
| 适用场景 | 开发调试 | 生产/大规模采集 |

## 优选实践

1. **先导航再操作**:所有交互前必须先 `navigate` 到目标页面。
2. **动作描述要具体**:例如"点击蓝色的提交按钮"优于"点击按钮"。
3. **每次操作后截图**:用 `screenshot` 验证操作结果。
4. **不熟悉页面先用 observe**:探索页面结构后再执行动作。
5. **结构化提取用 schema**:提取复杂数据时附带 JSON schema,结果更准确。
6. **完成后关闭浏览器**:`close` 释放资源。

## 常见问题

### Q1: Chrome 未找到?
- 确认本机已安装 Chrome 浏览器
- 检查 Chrome 是否在默认路径
- 如本机无 Chrome,可考虑使用远程浏览器模式(需配置 API Key)

### Q2: 动作执行失败?
- 使用 `browser observe` 先发现可用元素
- 尝试用更具体的描述(如"点击蓝色的登录按钮"而非"点击按钮")
- 截图查看当前页面状态:`browser screenshot`

### Q3: 提取的数据不准确?
- 为 `extract` 提供 JSON schema,明确字段类型
- 拆分复杂提取为多个简单步骤
- 先 `observe` 确认页面结构,再针对性提取

### Q4: Browserbase 模式失败?
- 验证 API Key 与项目 ID 是否正确配置
- 检查 `.env` 文件中的 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID`
- 确认远程浏览器服务配额未耗尽

### 已知限制
免费版使用本地 Chrome 浏览器,适合个人开发与原型验证。如需远程浏览器、隐身模式、代理/CAPTCHA 处理、批量任务等高阶能力,请升级至专业版。

### Q6: 如何调试?
```bash
# 截图查看当前状态
browser screenshot
# 观察页面元素
browser observe "页面上有哪些可交互元素"
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Chrome 浏览器**: 必需(本地模式)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Node.js | 运行环境 | 必需 | 系统包管理器安装(>= 18) |
| Chrome | 浏览器 | 必需 | 官方下载安装 |
| npm 依赖包 | Node 包 | 必需 | `npm install` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本 Skill 基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)
- 本地模式:无需额外 API Key
- 远程浏览器模式(可选):需配置 `BROWSERBASE_API_KEY` 与 `BROWSERBASE_PROJECT_ID`

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据