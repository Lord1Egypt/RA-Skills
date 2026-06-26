# Tool Name: check_file_permissions
# Description:
专门针对 OpenClaw 本地敏感目录（配置、凭证、会话日志）进行操作系统级别的文件权限审计。
确保 `~/.openclaw` 目录被设置为安全的 `700`，且关键凭证文件（如 OAuth 令牌、WhatsApp 会话凭证等）未向组用户或其他系统用户开放读取权限。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "clean" (权限安全) 或 "risks_found" (存在越权读取风险)。
- `vulnerable_files`: 权限过大的危险文件/目录列表及其当前权限掩码。