# AI, McpServer, TensorRT, Agents - 1Panel API

## 模块说明
AI, McpServer, TensorRT, Agents 模块接口，提供 Ollama 模型管理、MCP 服务器、TensorRT LLM 以及 AI Agents 的完整 API。

---

## 一、Ollama 模型接口

### GET /ai/gpu/load
**功能**: 获取 GPU/XPU 信息

**参数**: 无

**返回示例**:
```json
{
  "gpuInfo": {
    "name": "NVIDIA GeForce RTX 3080",
    "memoryTotal": "10GB",
    "memoryUsed": "2GB",
    "utilization": "30%"
  }
}
```

---

### POST /ai/ollama/model/sync
**功能**: 同步 Ollama 模型列表

**参数**: 无

**返回示例**:
```json
[
  { "id": 1, "name": "llama2" },
  { "id": 2, "name": "codellama" }
]
```

---

### POST /ai/ollama/model/search
**功能**: 分页查询 Ollama 模型列表

**参数 (SearchWithPage)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| info | string | 否 | 搜索关键词 | - |

---

### POST /ai/ollama/model
**功能**: 创建 Ollama 模型

**参数 (OllamaModelName)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 模型名称 | 有效的 Ollama 模型名，如 llama2, codellama, mistral 等 |
| taskID | string | 否 | 任务ID | - |

---

### POST /ai/ollama/model/recreate
**功能**: 重新创建 Ollama 模型（重试失败的任务）

**参数 (OllamaModelName)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 模型名称 | 有效的 Ollama 模型名 |
| taskID | string | 否 | 任务ID | - |

---

### POST /ai/ollama/model/load
**功能**: 获取 Ollama 模型详情

**参数 (OllamaModelName)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 模型名称 | 有效的 Ollama 模型名 |
| taskID | string | 否 | 任务ID | - |

**返回示例**:
```json
{
  "id": 1,
  "name": "llama2",
  "size": "3.8GB",
  "from": "ollama",
  "status": "running",
  "message": ""
}
```

---

### POST /ai/ollama/close
**功能**: 关闭 Ollama 模型连接

**参数 (OllamaModelName)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 模型名称 | 有效的 Ollama 模型名 |
| taskID | string | 否 | 任务ID | - |

---

### POST /ai/ollama/model/del
**功能**: 删除 Ollama 模型

**参数 (ForceDelete)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| ids | []uint | 是 | 模型ID列表 | - |
| forceDelete | bool | 否 | 是否强制删除 | true/false |

---

## 二、Ollama 域名绑定接口

### POST /ai/domain/bind
**功能**: 绑定域名到 Ollama 服务

**参数 (OllamaBindDomain)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| domain | string | 是 | 域名 | 有效的域名，如 ollama.example.com |
| appInstallID | uint | 是 | 应用安装ID | - |
| sslID | uint | 否 | SSL证书ID | - |
| websiteID | uint | 否 | 网站ID | - |
| ipList | string | 否 | IP白名单 | 逗号分隔的IP列表，如 "192.168.1.1,10.0.0.1" |

---

### POST /ai/domain/get
**功能**: 获取绑定的域名信息

**参数 (OllamaBindDomainReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| appInstallID | uint | 是 | 应用安装ID | - |

**返回示例 (OllamaBindDomainRes)**:
```json
{
  "domain": "ollama.example.com",
  "sslID": 1,
  "allowIPs": ["192.168.1.1"],
  "websiteID": 1,
  "connUrl": "https://ollama.example.com",
  "acmeAccountID": 1
}
```

---

### POST /ai/domain/update
**功能**: 更新绑定的域名信息

**参数 (OllamaBindDomain)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| domain | string | 是 | 域名 | 有效的域名 |
| appInstallID | uint | 是 | 应用安装ID | - |
| sslID | uint | 否 | SSL证书ID | - |
| websiteID | uint | 否 | 网站ID | - |
| ipList | string | 否 | IP白名单 | 逗号分隔的IP列表 |

---

## 三、MCP 服务器接口

### POST /ai/mcp/search
**功能**: 分页查询 MCP 服务器列表

**参数 (McpServerSearch)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| name | string | 否 | 服务器名称搜索 | - |
| sync | bool | 否 | 是否同步 | true/false |

---

### POST /ai/mcp/server
**功能**: 创建 MCP 服务器

**参数 (McpServerCreate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 服务器名称 | - |
| command | string | 是 | 启动命令 | 如 npx, python 等 |
| environments | []Environment | 否 | 环境变量列表 | - |
| volumes | []Volume | 否 | 卷挂载列表 | - |
| port | int | 是 | 端口号 | 1024-65535 |
| containerName | string | 否 | 容器名称 | - |
| baseUrl | string | 否 | 基础URL | - |
| ssePath | string | 否 | SSE 路径 | - |
| hostIP | string | 否 | 主机IP | - |
| streamableHttpPath | string | 否 | Streamable HTTP 路径 | - |
| outputTransport | string | 是 | 输出传输方式 | stdio, sse, streamable-http |
| type | string | 是 | 服务器类型 | mcp |

**Environment 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 环境变量名 |
| value | string | 是 | 环境变量值 |

**Volume 结构**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | 主机路径 |
| target | string | 是 | 容器路径 |

---

### POST /ai/mcp/server/update
**功能**: 更新 MCP 服务器

**参数 (McpServerUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 服务器ID | - |
| name | string | 是 | 服务器名称 | - |
| command | string | 是 | 启动命令 | - |
| environments | []Environment | 否 | 环境变量列表 | - |
| volumes | []Volume | 否 | 卷挂载列表 | - |
| port | int | 是 | 端口号 | 1024-65535 |
| containerName | string | 否 | 容器名称 | - |
| baseUrl | string | 否 | 基础URL | - |
| ssePath | string | 否 | SSE 路径 | - |
| hostIP | string | 否 | 主机IP | - |
| streamableHttpPath | string | 否 | Streamable HTTP 路径 | - |
| outputTransport | string | 是 | 输出传输方式 | stdio, sse, streamable-http |
| type | string | 是 | 服务器类型 | mcp |

---

### POST /ai/mcp/server/del
**功能**: 删除 MCP 服务器

**参数 (McpServerDelete)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 服务器ID | - |

---

### POST /ai/mcp/server/op
**功能**: 操作 MCP 服务器（启动/停止/重启）

**参数 (McpServerOperate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 服务器ID | - |
| operate | string | 是 | 操作类型 | start, stop, restart |

---

### GET /ai/mcp/domain/get
**功能**: 获取 MCP 服务器绑定的域名

**参数**: 无

**返回示例**:
```json
{
  "domain": "mcp.example.com",
  "sslID": 1,
  "allowIPs": ["192.168.1.1"],
  "websiteID": 1
}
```

---

### POST /ai/mcp/domain/bind
**功能**: 绑定域名到 MCP 服务器

**参数 (McpBindDomain)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| domain | string | 是 | 域名 | 有效的域名 |
| sslID | uint | 否 | SSL证书ID | - |
| ipList | string | 否 | IP白名单 | 逗号分隔的IP列表 |

---

### POST /ai/mcp/domain/update
**功能**: 更新 MCP 服务器绑定的域名

**参数 (McpBindDomainUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| websiteID | uint | 是 | 网站ID | - |
| sslID | uint | 否 | SSL证书ID | - |
| ipList | string | 否 | IP白名单 | 逗号分隔的IP列表 |

---

## 四、TensorRT LLM 接口

### POST /ai/tensorrt/search
**功能**: 分页查询 TensorRT LLM 列表

**参数 (TensorRTLLMSearch)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| name | string | 否 | 模型名称搜索 | - |

---

### POST /ai/tensorrt/create
**功能**: 创建 TensorRT LLM

**参数 (TensorRTLLMCreate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | 模型名称 | - |
| containerName | string | 是 | 容器名称 | - |
| version | string | 是 | TensorRT-LLM 版本 | 如 v0.13.0 |
| modelDir | string | 是 | 模型目录路径 | - |
| image | string | 是 | Docker 镜像 | 如 nvcr.io/nvidia/trt_llm:latest |
| command | string | 是 | 启动命令 | - |
| modelType | string | 否 | 模型类型 | llama, chatglm, etc. |
| modelSpeedup | bool | 否 | 是否启用加速 | true/false |
| exposedPorts | []ExposedPort | 否 | 暴露端口列表 | - |
| environments | []Environment | 否 | 环境变量列表 | - |
| volumes | []Volume | 否 | 卷挂载列表 | - |

---

### POST /ai/tensorrt/update
**功能**: 更新 TensorRT LLM

**参数 (TensorRTLLMUpdate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 模型ID | - |
| name | string | 是 | 模型名称 | - |
| containerName | string | 是 | 容器名称 | - |
| version | string | 是 | TensorRT-LLM 版本 | - |
| modelDir | string | 是 | 模型目录路径 | - |
| image | string | 是 | Docker 镜像 | - |
| command | string | 是 | 启动命令 | - |
| modelType | string | 否 | 模型类型 | - |
| modelSpeedup | bool | 否 | 是否启用加速 | - |
| exposedPorts | []ExposedPort | 否 | 暴露端口列表 | - |
| environments | []Environment | 否 | 环境变量列表 | - |
| volumes | []Volume | 否 | 卷挂载列表 | - |

---

### POST /ai/tensorrt/delete
**功能**: 删除 TensorRT LLM

**参数 (TensorRTLLMDelete)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 模型ID | - |

---

### POST /ai/tensorrt/operate
**功能**: 操作 TensorRT LLM（启动/停止/重启）

**参数 (TensorRTLLMOperate)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 模型ID | - |
| operate | string | 是 | 操作类型 | start, stop, restart |

---

## 五、Agents 接口

### POST /ai/agents
**功能**: 创建 Agent

**参数 (AgentCreateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| name | string | 是 | Agent 名称 | - |
| appVersion | string | 是 | 应用版本 | - |
| webUIPort | int | 是 | WebUI 端口 | 1024-65535 |
| bridgePort | int | 否 | 桥接端口 | - |
| agentType | string | 否 | Agent 类型 | - |
| provider | string | 否 | 模型提供商 | openai, anthropic, local, etc. |
| model | string | 否 | 模型名称 | - |
| apiType | string | 否 | API 类型 | - |
| maxTokens | int | 否 | 最大 token 数 | - |
| contextWindow | int | 否 | 上下文窗口大小 | - |
| accountID | uint | 否 | 账户ID | - |
| apiKey | string | 否 | API Key | - |
| baseURL | string | 否 | 基础 URL | - |
| token | string | 否 | Agent Token | - |
| advanced | bool | 否 | 是否启用高级配置 | - |
| containerName | string | 否 | 容器名称 | - |
| allowPort | bool | 否 | 是否允许自动分配端口 | - |
| specifyIP | string | 否 | 指定IP | - |
| restartPolicy | string | 否 | 重启策略 | always, on-failure, unless-stopped |
| cpuQuota | float64 | 否 | CPU 配额 | - |
| memoryLimit | float64 | 否 | 内存限制 | - |
| memoryUnit | string | 否 | 内存单位 | MB, GB |
| pullImage | bool | 否 | 是否拉取镜像 | - |
| editCompose | bool | 否 | 是否编辑 Compose | - |
| dockerCompose | string | 否 | Docker Compose 配置 | - |

---

### POST /ai/agents/search
**功能**: 分页查询 Agent 列表

**参数 (SearchWithPage)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| info | string | 否 | 搜索关键词 | - |

---

### POST /ai/agents/delete
**功能**: 删除 Agent

**参数 (AgentDeleteReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | Agent ID | - |
| taskID | string | 否 | 任务ID | - |
| forceDelete | bool | 否 | 是否强制删除 | - |

---

### POST /ai/agents/token/reset
**功能**: 重置 Agent Token

**参数 (AgentTokenResetReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | Agent ID | - |

---

### POST /ai/agents/model/update
**功能**: 更新 Agent 模型配置

**参数 (AgentModelConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| accountID | uint | 是 | 账户ID | - |
| model | string | 是 | 模型名称 | - |

---

### GET /ai/agents/providers
**功能**: 获取支持的模型提供商列表

**参数**: 无

**返回示例**:
```json
[
  {
    "provider": "openai",
    "displayName": "OpenAI",
    "baseURL": "https://api.openai.com/v1",
    "models": [
      { "id": "gpt-4", "name": "GPT-4" },
      { "id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo" }
    ]
  }
]
```

---

### POST /ai/agents/accounts
**功能**: 创建 Agent 账户

**参数 (AgentAccountCreateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| provider | string | 是 | 模型提供商 | openai, anthropic, etc. |
| name | string | 是 | 账户名称 | - |
| apiKey | string | 是 | API Key | - |
| rememberAPIKey | bool | 否 | 是否记住 API Key | - |
| baseURL | string | 否 | 基础 URL | - |
| model | string | 否 | 默认模型 | - |
| apiType | string | 否 | API 类型 | - |
| maxTokens | int | 否 | 最大 token 数 | - |
| contextWindow | int | 否 | 上下文窗口大小 | - |
| remark | string | 否 | 备注 | - |

---

### POST /ai/agents/accounts/update
**功能**: 更新 Agent 账户

**参数 (AgentAccountUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 账户ID | - |
| name | string | 是 | 账户名称 | - |
| apiKey | string | 是 | API Key | - |
| rememberAPIKey | bool | 否 | 是否记住 API Key | - |
| baseURL | string | 否 | 基础 URL | - |
| model | string | 否 | 默认模型 | - |
| apiType | string | 否 | API 类型 | - |
| maxTokens | int | 否 | 最大 token 数 | - |
| contextWindow | int | 否 | 上下文窗口大小 | - |
| remark | string | 否 | 备注 | - |
| syncAgents | bool | 否 | 是否同步到 Agent | - |

---

### POST /ai/agents/accounts/search
**功能**: 分页查询 Agent 账户列表

**参数 (AgentAccountSearch)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |
| provider | string | 否 | 提供商筛选 | - |
| name | string | 否 | 账户名称搜索 | - |

---

### POST /ai/agents/accounts/verify
**功能**: 验证 Agent 账户

**参数 (AgentAccountVerifyReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| provider | string | 是 | 模型提供商 | - |
| apiKey | string | 是 | API Key | - |
| baseURL | string | 否 | 基础 URL | - |

---

### POST /ai/agents/accounts/delete
**功能**: 删除 Agent 账户

**参数 (AgentAccountDeleteReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 是 | 账户ID | - |

---

### POST /ai/agents/channel/feishu/get
**功能**: 获取飞书频道配置

**参数 (AgentFeishuConfigReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |

---

### POST /ai/agents/channel/feishu/update
**功能**: 更新飞书频道配置

**参数 (AgentFeishuConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| botName | string | 是 | 机器人名称 | - |
| appID | string | 是 | App ID | - |
| appSecret | string | 是 | App Secret | - |
| enabled | bool | 否 | 是否启用 | - |
| dmPolicy | string | 是 | 私信策略 | all, approved, none |

---

### POST /ai/agents/channel/feishu/approve
**功能**: 批准飞书配对

**参数 (AgentFeishuPairingApproveReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| pairingCode | string | 是 | 配对码 | - |

---

### POST /ai/agents/channel/telegram/get
**功能**: 获取 Telegram 频道配置

**参数 (AgentTelegramConfigReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |

---

### POST /ai/agents/channel/telegram/update
**功能**: 更新 Telegram 频道配置

**参数 (AgentTelegramConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| enabled | bool | 否 | 是否启用 | - |
| dmPolicy | string | 是 | 私信策略 | all, approved, none |
| botToken | string | 是 | Bot Token | - |
| proxy | string | 否 | 代理地址 | - |

---

### POST /ai/agents/channel/discord/get
**功能**: 获取 Discord 频道配置

**参数 (AgentDiscordConfigReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |

---

### POST /ai/agents/channel/discord/update
**功能**: 更新 Discord 频道配置

**参数 (AgentDiscordConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| enabled | bool | 否 | 是否启用 | - |
| dmPolicy | string | 是 | 私信策略 | all, approved, none |
| groupPolicy | string | 是 | 群组策略 | open, allowlist, disabled |
| token | string | 是 | Bot Token | - |
| proxy | string | 否 | 代理地址 | - |

---

### POST /ai/agents/browser/get
**功能**: 获取浏览器配置

**参数 (AgentBrowserConfigReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |

---

### POST /ai/agents/browser/update
**功能**: 更新浏览器配置

**参数 (AgentBrowserConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| enabled | bool | 否 | 是否启用 | - |
| headless | bool | 否 | 是否无头模式 | - |
| noSandbox | bool | 否 | 是否禁用沙箱 | - |
| defaultProfile | string | 是 | 默认浏览器配置 | - |

---

### POST /ai/agents/other/get
**功能**: 获取其他配置

**参数 (AgentOtherConfigReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |

---

### POST /ai/agents/other/update
**功能**: 更新其他配置

**参数 (AgentOtherConfigUpdateReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| userTimezone | string | 是 | 用户时区 | 如 Asia/Shanghai, America/New_York |

---

### POST /ai/agents/channel/pairing/approve
**功能**: 批准频道配对

**参数 (AgentChannelPairingApproveReq)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| agentID | uint | 是 | Agent ID | - |
| type | string | 是 | 频道类型 | feishu, telegram, discord |
| pairingCode | string | 是 | 配对码 | - |

---

## 通用结构说明

### PageInfo
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| page | int | 是 | 页码 | > 0 |
| pageSize | int | 是 | 每页数量 | 1-100 |

### Environment
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | 环境变量名 |
| value | string | 是 | 环境变量值 |

### Volume
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | string | 是 | 主机路径 |
| target | string | 是 | 容器路径 |

### ExposedPort
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hostPort | int | 是 | 主机端口 |
| containerPort | int | 是 | 容器端口 |
| hostIP | string | 否 | 主机IP |
