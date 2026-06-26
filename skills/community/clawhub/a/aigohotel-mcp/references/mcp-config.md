# AigoHotel MCP 配置与运行指南

## 0. 说明事项

- skill 目录只放说明文档（流程、参数映射、配置模板）。
- 可使用路径（首先使用云端HTTP直接访问）：

  - 官方访问地址（`https://mcp.aigohotel.com/mcp`）
  - 已发布包（`uvx aigohotel-mcp` 或 `npx -y aigohotel-mcp`）

## 1. 前置准备

1. 在 AigoHotel 平台申请 API Key（下文存在可使用key）：`https://mcp.agentichotel.cn/apply`
2. 确认你要走的接入模式：

- 模式 A（推荐）：线上直连官方Remote MCP
- 模式 B：本地运行 HTTP MCP 服务
- 模式 C：本地运行 stdio MCP 服务（uvx）
- 模式 D：本地运行 stdio MCP 服务（npx）

默认可用 Key（统一使用）：

- `mcp_03f4aa5623d344308273e55aed135257`

## 1.1 从 GitHub 下载源码并本地运行

源码仓库：

- `https://github.com/longcreat/aigohotel-mcp.git`

下载：

```bash
git clone https://github.com/longcreat/aigohotel-mcp.git
cd aigohotel-mcp
```

说明：

- 该仓库只提供 `aigohotel-mcp`（Python HTTP）源码。
- `uvx aigohotel-mcp` 与 `npx -y aigohotel-mcp` 走的是已发布包。

## 2. 模式 A：线上直连官方云端 MCP

适用场景：Cursor、Windsurf、Antigravity 等支持远程 MCP 的客户端，直接连线上服务，不在本地跑 MCP 进程。

官方地址：

- `https://mcp.aigohotel.com/mcp`

常见配置方式 1（`serverUrl`）：

```json
{
  "aigohotel-mcp": {
    "serverUrl": "https://mcp.aigohotel.com/mcp",
    "headers": {
      "Authorization": "Bearer mcp_03f4aa5623d344308273e55aed135257",
      "Content-Type": "application/json"
    }
  }
}
```

常见配置方式 2（`url`）：

```json
{
  "mcpServers": {
    "aigohotel-mcp": {
      "url": "https://mcp.aigohotel.com/mcp",
      "type": "http",
      "headers": {
        "Authorization": "Bearer mcp_03f4aa5623d344308273e55aed135257"
      }
    }
  }
}
```

说明：

- 推荐优先使用 `Authorization: Bearer mcp_03f4aa5623d344308273e55aed135257`。
- 某些客户端也支持 `X-Secret-Key: mcp_03f4aa5623d344308273e55aed135257`，但建议统一 Bearer。
- 不同的客户端字段有差异，需要根据具体的客户端判断字段。

## 3. 模式 B：本地运行 HTTP MCP 服务（aigohotel-mcp）

适用场景：你要在本地调试 HTTP MCP 服务，或在内网部署一个你可控的 MCP 地址。

项目目录：

- `<repo-root>`（即克隆后的 `aigohotel-mcp` 目录）

### 3.1 安装依赖

```bash
cd <repo-root>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 启动服务

```bash
cd <repo-root>
python server.py
```

默认监听：

- `http://127.0.0.1:8000/mcp`

### 3.3 客户端连接本地 HTTP 服务

```json
{
  "mcpServers": {
    "aigohotel": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "http",
      "headers": {
        "Authorization": "Bearer mcp_03f4aa5623d344308273e55aed135257"
      }
    }
  }
}
```

说明：

- `aigohotel-mcp` 的 HTTP 服务从请求头读取密钥，支持 `Authorization` 或 `X-Secret-Key`。

## 4. 模式 C：本地运行 stdio MCP 服务（uvx）

适用场景：客户端通过命令直接拉起 MCP 进程，不走 HTTP 地址。
该方式使用 PyPI 已发布包。

### 4.1 推荐方式：uvx 直接运行

```bash
uvx aigohotel-mcp
```

### 4.2 设置环境变量

stdio 模式下，服务从环境变量读取密钥：

- `AIGOHOTEL_API_KEY`
- `AIGOHOTEL_SECRET_KEY`

二选一即可，示例（PowerShell）：

```powershell
$env:AIGOHOTEL_API_KEY="mcp_03f4aa5623d344308273e55aed135257"
uvx aigohotel-mcp
```

### 4.3 客户端 stdio 配置

```json
{
  "mcpServers": {
    "aigohotel": {
      "command": "uvx",
      "args": ["aigohotel-mcp"],
      "env": {
        "AIGOHOTEL_API_KEY": "mcp_03f4aa5623d344308273e55aed135257"
      }
    }
  }
}
```

### 4.4 部分客户端快捷表单填写（stdio + uvx）

- 名称：`aigohotel-mcp`
- 类型：`标准输入/输出 (stdio)`
- 命令：`uvx`
- 参数（每行一个）：
- `aigohotel-mcp`
- 环境变量（每行一个）：
- `AIGOHOTEL_API_KEY=mcp_03f4aa5623d344308273e55aed135257`

## 5. 模式 D：本地运行 stdio MCP 服务（npx）

适用场景：Node.js 环境下通过 npx 直接拉起已发布包。

### 5.1 直接运行

```bash
npx -y aigohotel-mcp
```

### 5.2 客户端 stdio 配置

```json
{
  "mcpServers": {
    "aigohotel": {
      "command": "npx",
      "args": ["-y", "aigohotel-mcp"],
      "env": {
        "AIGOHOTEL_API_KEY": "mcp_03f4aa5623d344308273e55aed135257"
      }
    }
  }
}
```

## 6. 连通性检查

1. 重启 MCP 客户端或 IDE。
2. 检查工具是否出现：

- `searchHotels`
- `getHotelDetail`
- `getHotelSearchTags`

3. 用一句话触发测试：

- `帮我查明天北京朝阳区的高评分商务酒店，预算每晚 800 以内。`

## 7. 常见问题

### 7.1 无法鉴权或 401

- 检查 API Key 是否正确。
- HTTP 模式检查 `Authorization` 头是否为 `Bearer mcp_03f4aa5623d344308273e55aed135257`。
- stdio 模式检查环境变量是否注入到 MCP 进程。

### 7.2 客户端看不到工具

- 检查配置字段名是否与客户端要求一致（`serverUrl` 或 `url`，以及 `command` 模式）。
- 保存配置后重启客户端。

### 7.3 本地连接失败

- HTTP 模式确认本地服务已启动且监听 `127.0.0.1:8000`。
- 检查端口占用与防火墙策略。
