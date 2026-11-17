---
slug: "feishu-card-free"
name: "feishu-card-free"
version: "1.4.11"
displayName: "协作平台卡片基础版"
summary: "基础协作平台卡片发送，支持文本、标题和颜色设置。向协作平台用户或群组发送基础文本卡片的免费版。支持简单文本、卡片标题和颜色设置、 安全发送（自动处理转义）。适用于基础通知和简单消息推送场景."
summary_zh: "基础协作平台卡片发送，支持文本、标题和颜色设置。向协作平台用户或群组发送基础文本卡片的免费版。支持简单文本、卡片标题和颜色设置、 安全发送（自动处理转义）。适用于基础通知和简单消息推送场景."
license: "MIT"
description: "|-. 适用于需要feishu card相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  向协作平台用户或群组发送基础文本卡片的免费版。支持简单文本、卡片标题和颜色设置、
  安全发送（自动处理转义）。适用于基础通知和简单消息推送场景.
  升级至完整版可解锁Markdown复杂卡片、按钮组件、图片嵌入和人格化消息功能.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 通用办公
  - feishu
  - card
  - automation
  - productivity
  - 工具
  - 效率
  - 自动化
  - 开发
  - 代码
category: "Automation"
pricing_tier: free
---
# 协作平台卡片（免费版）

向协作平台用户或群组发送基础文本卡片的免费版。支持简单文本发送、卡片标题和颜色设置，以及安全发送（自动处理shell转义）.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 协作平台卡片基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 前置依赖

- 需先安装 `feishu-common` 依赖
- 本skill依赖 `./feishu-common/index.js` 进行Token和API认证

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

### 1. 简单文本卡片
通过 `node skills/feishu-card/send.js --target "ou_..." --text "Hello World"` 发送简单文本卡片。`--target` 参数接受用户Open ID（`ou_` 前缀）或群组Chat ID（`oc_` 前缀）。适用于不含特殊字符的简单消息推送场景.
### 2. 卡片标题和颜色
通过 `--title <string>` 设置卡片头部标题，`--color <string>` 设置头部颜色。支持6种颜色：`blue`（默认）、`red`、`orange`、`green`、`purple`、`grey`。适用于按消息类型区分卡片视觉样式.

### 3. 安全发送

通过 `node skills/feishu-card/send_safe.js` 包装器安全发送原始文本。自动处理临时文件创建和清理，避免shell转义问题。支持 `--text` 直接传入含特殊字符的内容，配合 `--title` 设置卡片标题。适用于自动化流程中的安全消息发送。- 验证返回数据的完整性和格式正确性
- 参考`安全发送`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 升级提示

以下为完整版（feishu-card）独有功能，免费版不可用：

- **Markdown复杂卡片**：`--text-file` 从文件读取Markdown内容，支持代码块、表格、列表
- **按钮组件**：`--button-text` 和 `--button-url` 在卡片底部添加可点击操作按钮
- **图片嵌入**：`--image-path` 上传本地图片并嵌入卡片，支持PNG/JPG/GIF格式
- **人格化消息**：`send_persona.js` 发送带主题样式的人格化消息
- **多种人格样式**：`d-guide`/`green-tea`/`mad-dog`/`default` 四种预设人格样式

升级至完整版以获取全部能力.
## 使用流程

1. 确认已安装 `feishu-common` 依赖，Token和API认证已配置
2. 获取目标ID：用户Open ID（`ou_` 前缀）或群组Chat ID（`oc_` 前缀）
3. 使用 `--text` 发送简单文本，或使用 `send_safe.js` 发送含特殊字符的内容
4. 按需配置 `--title` 和 `--color` 设置卡片头部样式
5. 执行发送命令并检查响应确认消息已送达
6. 如需Markdown、按钮、图片或人格化功能，升级至完整版

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 示例

### 示例1：发送带标题和颜色的文本卡片

```bash
# 发送简单文本卡片
node skills/feishu-card/send.js \
  --target "ou_abc123def456" \
  --text "部署完成，服务已上线" \
  --title "部署通知" \
  --color green
```

### 示例2：使用安全发送处理特殊字符

```bash
# 安全发送含特殊字符的内容
node skills/feishu-card/send_safe.js \
  --target "oc_group123456" \
  --text "错误日志: [ERROR] path=/api/v1/users status=500" \
  --title "系统告警" \
  --color red
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| `--text` 中反引号消失 | Shell将反引号解释为命令替换 | 使用 `send_safe.js` 包装器自动处理转义 |
| 目标ID格式错误 | 传入的ID不以 `ou_` 或 `oc_` 开头 | 确认Open ID格式为 `ou_` 前缀，群组Chat ID为 `oc_` 前缀 |
| 颜色参数无效 | 传入了不在支持列表中的颜色 | 使用6种有效颜色之一：`blue`/`red`/`orange`/`green`/`purple`/`grey` |
| 依赖缺失 | 未安装 `feishu-common` | 先安装 `feishu-common`，确保 `..js` 可访问 |
| 请求Markdown功能 | 免费版不支持 `--text-file` | 升级至完整版以使用Markdown复杂卡片功能 |
| 请求按钮组件 | 免费版不支持 `--button-text`/`--button-url` | 升级至完整版以使用按钮组件功能 |
| 请求图片嵌入 | 免费版不支持 `--image-path` | 升级至完整版以使用图片嵌入功能 |
| 请求人格化消息 | 免费版不支持 `send_persona.js` | 升级至完整版以使用人格化消息功能 |

## 常见问题

### Q1: 免费版可以发送Markdown内容吗？

不可以。`--text-file` Markdown复杂卡片是完整版独有功能。免费版仅支持简单文本（`--text`）和安全发送（`send_safe.js`）。如需发送代码块、表格等Markdown内容，请升级至完整版.
### Q2: 为什么反引号消失了？

Shell将反引号（`` ` ``）解释为命令替换，导致内容丢失。免费版可使用 `send_safe.js` 包装器自动处理转义问题。完整版的 `--text-file` 从文件读取内容可完全避免此问题.
### Q3: 免费版支持哪些颜色？

支持6种卡片头部颜色：`blue`（默认）、`red`、`orange`、`green`、`purple`、`grey`。通过 `--color <string>` 参数设置。`red` 用于告警，`green` 用于成功，`orange` 用于警告，`grey` 用于普通通知.
### Q4: Open ID和Group Chat ID有什么区别？

Open ID（`ou_` 前缀）标识单个用户，消息发送到该用户的私聊。Group Chat ID（`oc_` 前缀）标识群组，消息发送到群聊中所有成员。通过 `--target` 参数指定.
### Q5: 免费版可以发送图片吗？

不可以。`--image-path` 图片嵌入是完整版独有功能。免费版仅支持文本内容。如需发送截图、图表等图片内容，请升级至完整版.
### Q6: 免费版支持人格化消息吗？

不支持。`send_persona.js` 和4种预设人格（`d-guide`/`green-tea`/`mad-dog`/`default`）是完整版独有功能。如需带主题样式的人格化消息，请升级至完整版.
## 已知限制

- 不支持Markdown复杂卡片（`--text-file`），完整版可用
- 不支持按钮组件（`--button-text`/`--button-url`），完整版可用
- 不支持图片嵌入（`--image-path`），完整版可用
- 不支持人格化消息（`send_persona.js`），完整版可用
- 依赖 `feishu-common` 进行Token认证，需提前配置

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "协作平台卡片基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "feishu-card"
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
