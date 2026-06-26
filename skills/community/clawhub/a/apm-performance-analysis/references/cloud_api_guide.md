# 云API SendMCPMessage 接口详情

本文档包含 SendMCPMessage 接口的请求/响应结构、Endpoint 配置、参数格式和错误码等完整参考。

## 接口概述

| 项目 | 说明 |
|------|------|
| 接口名称 | `SendMCPMessage` |
| 产品 | 腾讯云 APM |
| API 版本 | `2021-06-22` |
| 默认 Endpoint | `apm.tencentcloudapi.com`（公网） |
| 认证方式 | 云API标准签名（TC3-HMAC-SHA256） |
| 客户端 Region | 固定 `ap-guangzhou` |
| SDK | 腾讯云官方 Python SDK（内嵌 vendored） |
| 客户端类 | `tencentcloud.apm.v20210622.ApmClient` |

## SDK 架构

本 Skill 采用 **内嵌（vendored）** 方式集成腾讯云官方 Python SDK v3.1.93，无需 pip 安装外部依赖。

### 目录结构

```
scripts/tencentcloud/
├── __init__.py                          # SDK 版本号 (__version__ = '3.1.93')
├── common/
│   ├── __init__.py
│   ├── abstract_client.py               # AbstractClient 基类（TC3签名、请求发送）
│   ├── abstract_model.py                # AbstractModel 基类（序列化/反序列化）
│   ├── credential.py                    # Credential 凭证类
│   ├── sign.py                          # TC3-HMAC-SHA256 签名实现
│   ├── circuit_breaker.py               # 熔断器
│   ├── common_client.py                 # 通用客户端
│   ├── retry.py                         # 重试逻辑
│   ├── exception/
│   │   └── tencent_cloud_sdk_exception.py  # SDK 异常类
│   ├── http/
│   │   ├── request.py                   # HTTP 请求封装
│   │   └── pre_conn.py                  # 预连接池
│   └── profile/
│       ├── client_profile.py            # 客户端配置
│       └── http_profile.py             # HTTP 配置（endpoint、超时等）
└── apm/
    └── v20210622/
        ├── __init__.py
        ├── apm_client.py                # ApmClient（SendMCPMessage 方法）
        ├── models.py                    # 请求/响应模型
        └── errorcodes.py               # 错误码定义
```

### 核心模型类

| 类名 | 说明 |
|------|------|
| `SendMCPMessageRequest` | 请求参数：`Method`、`ToolName`、`Arguments` |
| `SendMCPMessageResponse` | 响应参数：`MCPMessage`（MCPMessage对象）、`RequestId` |
| `MCPMessage` | MCP 响应体：`Result`（JSON 字符串） |
| `APMKVItem` | 工具参数键值对：`Key`、`Value` |

### 响应解析（重要）

官方 SDK 的响应结构为：

```python
resp = client.SendMCPMessage(req)
# 正确的响应数据访问方式：
content = resp.MCPMessage.Result  # JSON 字符串
request_id = resp.RequestId
```

**注意**：响应数据在 `resp.MCPMessage.Result` 中，而非 `resp.Content`。

## Endpoint 配置

| 环境 | Endpoint | 说明 |
|------|----------|------|
| 公网（默认） | `apm.tencentcloudapi.com` | 外部网络均可访问 |
| 内网 | `apm.ap-guangzhou.tencentcloudapi.woa.com` | 仅腾讯内网 |

切换方式（环境变量，写入 `~/.zshrc` 永久生效）：

```bash
# 切换为内网（仅腾讯内网环境使用）
export APM_API_ENDPOINT="apm.ap-guangzhou.tencentcloudapi.woa.com"

# 恢复公网（默认，无需设置）
unset APM_API_ENDPOINT
```

## 请求参数结构

### Method: `tools/list`

列举 MCP Server 当前支持的所有工具。

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Method | String | 是 | 固定值 `"tools/list"` |

**请求示例**：

```python
from tencentcloud.apm.v20210622.models import SendMCPMessageRequest

req = SendMCPMessageRequest()
req.Method = "tools/list"
resp = client.SendMCPMessage(req)
# resp.MCPMessage.Result 为 JSON 字符串
```

**响应示例**（`resp.MCPMessage.Result` 解析后）：

```json
{"tools": [{"name": "DescribeApmOverview", "description": "...", "inputSchema": {...}}]}
```

### Method: `tools/call`

调用指定的 MCP 工具。

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Method | String | 是 | 固定值 `"tools/call"` |
| ToolName | String | 是 | 工具名称 |
| Arguments | list of APMKVItem | 否 | 工具参数，APMKVItem 对象列表 |

**Arguments 构造方式**：

```python
from tencentcloud.apm.v20210622.models import SendMCPMessageRequest, APMKVItem

req = SendMCPMessageRequest()
req.Method = "tools/call"
req.ToolName = "DescribeApmOverview"

# 构造 APMKVItem 参数列表
item1 = APMKVItem()
item1.Key = "start_time"
item1.Value = "1744786829"

item2 = APMKVItem()
item2.Key = "end_time"
item2.Value = "1744787429"

item3 = APMKVItem()
item3.Key = "region"
item3.Value = "ap-beijing"

req.Arguments = [item1, item2, item3]
resp = client.SendMCPMessage(req)
```

> **重要**：所有 Value 均为字符串类型。脚本 `apm_mcp_client.py` 的 `call-tool` 命令会自动将 `--args '{"key":"value"}'` 的 JSON dict 格式转换为 APMKVItem 列表，AI 无需手动构造。

### Method: `ping`

检测 MCP Server 连通性。

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Method | String | 是 | 固定值 `"ping"` |

## 客户端 Region 说明

`SendMCPMessage` 接口的客户端 Region 固定为 `ap-guangzhou`，这是 APM 服务的接入地域。与工具内部的 `region` 参数（如 Arguments 中传递的 `region=ap-beijing`）不同：

- **客户端 Region**：决定 API 请求发送到哪个接入点，固定 `ap-guangzhou`
- **工具 region 参数**：决定查询哪个地域的 APM 数据，由用户指定

## 与旧版方案的差异

| 维度 | 旧方案（自建 shim） | 新方案（官方 SDK vendored） |
|------|---------------------|---------------------------|
| SDK 来源 | 基于 `AbstractClient` 自行封装 | 腾讯云官方 SDK v3.1.93 |
| 安装方式 | 需 pip install `tencentcloud-sdk-python-common` | 内嵌无需安装 |
| 客户端类 | 自建 `ApmMcpClient` | 官方 `ApmClient` |
| 请求方法 | `call_json()` | 官方 `call()` + `_serialize()` |
| 响应结构 | `resp.Content`（错误） | `resp.MCPMessage.Result`（正确） |
| 参数格式 | plain dict `{"Key": "k", "Value": "v"}` | `APMKVItem` 对象（property-based） |
| 虚拟环境 | 需要 `.apm-venv` | 不需要 |

## 错误码

### 云API级别错误

| 错误码 | 描述 | 处理建议 |
|--------|------|----------|
| `AuthFailure.SecretIdNotFound` | SecretId 不存在 | 检查环境变量配置 |
| `AuthFailure.SignatureFailure` | 签名错误 | 检查 SecretKey 是否正确 |
| `AuthFailure.TokenFailure` | Token 错误 | 检查临时凭证是否过期 |
| `InternalError` | 服务端内部错误 | 重试或联系管理员 |
| `InvalidParameter` | 参数错误 | 检查 Method/ToolName/Arguments 格式 |
| `RequestLimitExceeded` | 请求限流 | 降低调用频率 |

### 工具级别错误

工具执行失败时，错误信息包含在 `MCPMessage.Result` 字段中，需解析 JSON 获取具体错误原因。

## 命令行使用示例

```bash
# 检测连通性
python scripts/apm_mcp_client.py ping

# 列出工具（JSON 格式）
python scripts/apm_mcp_client.py list-tools --output json

# 列出工具（表格格式）
python scripts/apm_mcp_client.py list-tools --output table

# 调用工具
python scripts/apm_mcp_client.py call-tool \
    --name DescribeApmOverview \
    --args '{"start_time":"1744786829","end_time":"1744787429","region":"ap-beijing"}'

# 调用工具（JSON输出）
python scripts/apm_mcp_client.py call-tool \
    --name DescribeApmOverview \
    --args '{"start_time":"1744786829","end_time":"1744787429","region":"ap-beijing"}' \
    --output json
```

## 程序化调用（Python）

```python
import sys
sys.path.insert(0, "<skill_base_dir>/scripts")

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.apm.v20210622.apm_client import ApmClient
from tencentcloud.apm.v20210622.models import SendMCPMessageRequest, APMKVItem

# 创建凭证和客户端
cred = credential.Credential("your-secret-id", "your-secret-key")
httpProfile = HttpProfile()
httpProfile.endpoint = "apm.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = ApmClient(cred, "ap-guangzhou", clientProfile)

# 列出工具
req = SendMCPMessageRequest()
req.Method = "tools/list"
resp = client.SendMCPMessage(req)
print(resp.MCPMessage.Result)  # JSON 字符串

# 调用工具
req = SendMCPMessageRequest()
req.Method = "tools/call"
req.ToolName = "DescribeApmOverview"

item1 = APMKVItem()
item1.Key = "start_time"
item1.Value = "1744786829"

item2 = APMKVItem()
item2.Key = "end_time"
item2.Value = "1744787429"

item3 = APMKVItem()
item3.Key = "region"
item3.Value = "ap-beijing"

req.Arguments = [item1, item2, item3]
resp = client.SendMCPMessage(req)
print(resp.MCPMessage.Result)  # JSON 字符串
```
