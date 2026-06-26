# Tool Name: audit_proxy
# Description:
用于审计服务器上的 Nginx 或 Caddy 反向代理配置文件。
该工具会自动寻找配置文件中是否存在 URL 凭据泄露（如 token=, gatewayUrl=）以及针对 18789 端口的高危转发规则。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "clean" (未发现风险) 或 "risks_found" (发现潜在风险)
- `findings`: 一个数组，列出具体的风险文件路径及包含危险配置的代码行。