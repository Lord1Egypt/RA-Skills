---
slug: azure-gateway-cli-free
name: azure-gateway-cli-free
version: 1.0.0
displayName: Azure网关CLI免费版
summary: 轻量级本地代理，将OpenAI兼容请求路由到用户自建的Azure OpenAI端点，支持基础健康检查与单实例转发
license: Proprietary
edition: free
description: Azure网关CLI免费版是一款面向独立开发者的本地代理工具，用于解决OpenAI兼容客户端与Azure OpenAI服务之间的协议适配问题。Azure
  OpenAI使用专属的URL路径与查询参数格式，与标准OpenAI API存在差异，直接对接往往导致请求失败或参数丢失。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。
tags:
- 集成工具
- API网关
- 本地代理
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "Azure,云计算,DevOps"
---
# Azure网关CLI免费版

一款轻量级本地代理工具，桥接标准OpenAI兼容客户端与Azure OpenAI服务，解决URL路径与认证头的协议差异问题。

## 概述

Azure OpenAI服务要求请求URL携带部署名与`api-version`查询参数，并使用`api-key`请求头而非Bearer令牌进行认证。这种差异导致大量OpenAI兼容客户端无法直接对接Azure端点。本工具通过在本地启动一个代理服务，自动完成协议转换，让客户端只需指向本地端口即可透明访问Azure OpenAI。

免费版聚焦于单实例转发与基础配置能力，适合个人开发者在本地环境中快速验证Azure OpenAI的接入方案。

## 核心能力

### 协议适配
- 将标准`/chat/completions`路径重写为Azure部署级URL
- 自动注入`api-version`查询参数，避免被客户端覆盖
- 转换认证头：从`Authorization: Bearer`映射为`api-key`头

**输入**: 用户提供协议适配所需的指令和必要参数。
**处理**: 解析协议适配的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回协议适配的响应数据,包含状态码、结果和日志。

### 配置管理
- 通过环境变量配置所有运行参数，便于容器化部署
- 支持端点、部署名、API版本、端口、绑定地址独立设置
- 提供默认值兜底，降低初次使用门槛

**输入**: 用户提供配置管理所需的指令和必要参数。
**处理**: 解析配置管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回配置管理的响应数据,包含状态码、结果和日志。

### 健康检查
- 内置`/health`端点，返回服务存活状态
- 便于与外部监控系统集成

**输入**: 用户提供健康检查所需的指令和必要参数。
**处理**: 解析健康检查的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回健康检查的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级本地代理、OpenAI、兼容请求路由到用、户自建的、Azure、支持基础健康检查、与单实例转发、CLI、免费版是一款面向、独立开发者的本地、代理工具、用于解决、兼容客户端与、服务之间的协议适、配问题、使用专属的、URL、路径与查询参数格、与标准、API、存在差异、直接对接往往导致、请求失败或参数丢、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求等。

## 使用场景

### 场景一：本地Agent接入Azure额度
开发者希望在本地Agent平台中复用企业Azure OpenAI额度，但Agent平台仅支持标准OpenAI接口。启动本代理后，将Agent的模型供应商指向本地端口即可透明转发。

### 场景二：自动化脚本统一调用
运维脚本需要同时调用OpenAI与Azure OpenAI，通过本代理可将两者接口统一为标准格式，简化脚本逻辑。

### 场景三：原型验证与调试
在学习或原型阶段，开发者希望快速验证Azure OpenAI的响应质量，无需修改现有客户端代码即可切换供应商。

## 快速开始

预计上手时间：约60秒。

### 第一步：配置环境变量

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Azure网关CLI免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
export AZURE_OPENAI_ENDPOINT="your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
export AZURE_OPENAI_API_VERSION="2025-01-01-preview"
```

### 第二步：启动代理服务

```bash
node （请参考skill目录中的脚本文件）
```

### 第三步：配置客户端指向本地端口

在Agent平台的供应商配置中添加：

```json
{
  "models": {
    "providers": {
      "azure-gpt4o": {
        "baseUrl": "http://127.0.0.1:18790",
        "apiKey": "YOUR_AZURE_API_KEY",
        "api": "openai-completions",
        "authHeader": false,
        "headers": {
          "api-key": "YOUR_AZURE_API_KEY"
        },
        "models": [
          { "id": "gpt-4o", "name": "GPT-4o (Azure)" }
        ]
      }
    }
  }
}
```

注意：必须设置`authHeader: false`，因为Azure使用`api-key`头而非Bearer令牌。

### 第四步：验证连通性

```bash
curl http://localhost:18790/health
```

返回`{"status":"ok"}`即表示代理服务正常运行。

## 示例

### 环境变量说明

| 变量名 | 默认值 | 说明 | 是否必需 |
|:-----|:-----|:-----|:-----|
| `AZURE_PROXY_PORT` | `18790` | 本地代理监听端口 | 否 |
| `AZURE_PROXY_BIND` | `127.0.0.1` | 绑定地址，`0.0.0.0`可对外暴露 | 否 |
| `AZURE_OPENAI_ENDPOINT` | — | Azure资源主机名 | 是 |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4o` | 部署名称 | 是 |
| `AZURE_OPENAI_API_VERSION` | `2025-01-01-preview` | API版本 | 否 |

### 子代理路由配置（可选）

若希望子代理任务也走Azure通道以节省成本：

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "azure-gpt4o/gpt-4o"
      }
    }
  }
}
```

## 最佳实践

### 安全建议
- 绑定地址保持`127.0.0.1`，避免代理对外暴露
- API Key通过环境变量注入，不要硬编码到配置文件
- 生产环境将配置文件加入`.gitignore`

### 部署建议
- 使用systemd服务实现开机自启与异常恢复
- 健康检查端点接入外部监控，及时发现服务中断
- 端口选择避开常用端口，减少冲突风险

### 性能建议
- 代理本身开销极低（约10ms），瓶颈在Azure端响应
- 高并发场景考虑启用连接复用
- 避免在代理层做复杂日志，影响吞吐

## 常见问题

### Q1：启动后请求返回404资源未找到？
检查`AZURE_OPENAI_ENDPOINT`与`AZURE_OPENAI_DEPLOYMENT`是否与Azure门户中的配置完全一致。部署名区分大小写。

### Q2：返回401未授权？
API Key错误或已过期。在Azure门户的"密钥和终结点"页面重新获取Key，更新环境变量后重启服务。

### Q3：内容被Azure过滤拦截？
Azure的内容过滤策略比OpenAI更严格。部分在OpenAI上可用的提示词可能在Azure端被阻断。可在Azure门户的"内容过滤"中调整策略。

### Q4：端口被占用如何处理？
修改`AZURE_PROXY_PORT`环境变量为其他空闲端口，同步更新客户端配置中的`baseUrl`。

### Q5：能否同时代理多个Azure部署？
免费版仅支持单实例转发。如需多部署路由、负载均衡与故障切换，请使用专业版。

## 已知限制

本免费体验版限制以下高级功能：
- 单部署转发，不支持多端点路由与负载均衡
- 无故障自动切换与熔断机制
- 无请求级缓存与成本统计
- 无systemd服务模板与开机自启配置脚本
- 无多租户隔离与API Key轮换

解锁全部功能请使用专业版：azure-gateway-cli-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+（推荐LTS版本）
- **网络**: 需可访问Azure OpenAI端点

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时 | 必需 | nodejs.org官方下载 |
| Azure OpenAI服务 | API | 必需 | Azure门户订阅 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- **Azure API Key**: 通过`AZURE_OPENAI_API_KEY`环境变量注入，或写入客户端配置的`headers.api-key`字段
- **禁止**: 在SKILL.md或脚本中硬编码API Key
- **建议**: 使用`.env`文件管理环境变量，并加入`.gitignore`

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Azure网关CLI免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "azure gateway cli"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
