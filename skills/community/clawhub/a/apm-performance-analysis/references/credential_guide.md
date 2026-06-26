# 凭证配置指南

腾讯云凭证（SecretId / SecretKey）的完整配置步骤、安全规则及对话引导模板。

## 凭证用途

`apm_mcp_client.py` 自动从 shell 环境变量读取凭证，通过腾讯云标准签名算法（TC3-HMAC-SHA256）对请求签名，密钥不以明文传输。

## 凭证就绪检查

调用前执行 `echo $TENCENTCLOUD_SECRET_ID` 确认环境变量存在（不输出具体值）。

凭证缺失时，**必须按以下格式模板**向用户展示配置引导（格式不可修改）：

---

🔑 **请配置腾讯云 AK/SK**

需提供 SecretId 和 SecretKey，步骤如下：

**第一步：获取密钥**

前往 👉 [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi) 获取（建议创建最小权限子账号，避免使用主账号密钥）。

**第二步：写入 shell 配置文件（永久生效）**

在终端执行（将 your-secret-id 和 your-secret-key 替换为实际密钥）：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="your-secret-id"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="your-secret-key"' >> ~/.zshrc
source ~/.zshrc
```

**第三步：确认配置**

配置完成后告知，即可立即验证并开始执行。

⚠️ **安全提示**：勿在聊天中发送密钥明文，建议直接在终端中操作。密钥仅通过环境变量读取，不会写入任何文件或日志。

---

## 配置步骤

### 第一步：获取密钥

前往 [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi) 获取。

**安全建议**：创建最小权限子账号，避免使用主账号密钥。

### 第二步：写入 shell 配置文件（永久生效）

在终端执行以下命令（将 `your-secret-id` 和 `your-secret-key` 替换为你的实际密钥）：

**macOS / Linux (Zsh)**：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="your-secret-id"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="your-secret-key"' >> ~/.zshrc
source ~/.zshrc
```

**macOS / Linux (Bash)**：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="your-secret-id"' >> ~/.bashrc
echo 'export TENCENTCLOUD_SECRET_KEY="your-secret-key"' >> ~/.bashrc
source ~/.bashrc
```

### 第三步：验证配置

```bash
# 检查环境变量是否生效（应输出你的 SecretId）
echo $TENCENTCLOUD_SECRET_ID
```

### 第四步（可选）：配置其他环境变量

```bash
# 切换为内网 Endpoint（仅腾讯内网环境使用，公网无需设置）
# echo 'export APM_API_ENDPOINT="apm.ap-guangzhou.tencentcloudapi.woa.com"' >> ~/.zshrc

source ~/.zshrc
```

## 支持的环境变量

| 变量名 | 必填 | 说明 |
|-------|------|------|
| `TENCENTCLOUD_SECRET_ID` | 是 | 腾讯云 API SecretId（用于请求签名） |
| `TENCENTCLOUD_SECRET_KEY` | 是 | 腾讯云 API SecretKey（用于请求签名） |
| `APM_API_ENDPOINT` | 否 | 云API Endpoint，默认公网 `apm.tencentcloudapi.com` |
| `APM_ERROR_LOG_DIR` | 否 | 错误日志目录，不设置则为 `./logs/` |

## 凭证优先级

1. 命令行参数 `--secret-id` / `--secret-key`（最高优先级）
2. 环境变量 `TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`

## 认证方式说明

本 skill 使用腾讯云API标准签名认证（TC3-HMAC-SHA256），由 SDK 自动完成签名计算。与旧版 MCP SSE 方案（通过 HTTP Header 明文传递密钥）相比，签名认证具有以下安全优势：

- **密钥不离开本地**：仅用于本地计算签名，不会通过网络传输
- **防篡改**：签名覆盖请求的全部内容，任何篡改都会导致验签失败
- **防重放**：签名包含时间戳，过期请求会被拒绝

## 安全强制规则

1. **禁止硬编码**: 任何代码中不得出现真实的 SecretId 或 SecretKey 值。
2. **占位符引用**: 在文档、示例代码、终端输出中，必须使用占位符。
3. **版本控制排除**: 密钥仅存在于用户的 shell 配置文件中，不会出现在项目文件里。
4. **日志脱敏**: 错误日志不记录密钥值，日志文件权限 `600`。
5. **对话安全**: 用户提供密钥明文时不得回显，应提示在终端中配置环境变量。
6. **不使用 .env 文件**: 凭证不通过 `.env` 文件管理，避免被意外提交到版本控制。
