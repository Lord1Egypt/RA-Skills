# Tool Name: scan_ports
# Description:
用于扫描当前服务器上正在监听的网络端口。
当你需要排查 18789 等敏感端口是否暴露在公网 (0.0.0.0 或 ::) 时，请调用此工具。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "success" 或 "error"
- `tool_used`: 实际使用的底层命令（如 ss 或 netstat）
- `raw_output`: 包含所有监听端口的原始文本列表。