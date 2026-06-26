# Tool Name: check_docker_ports
# Description:
用于检查当前运行的 Docker 容器及其端口映射状态。
当你需要排查 OpenClaw 相关容器是否错误地将敏感服务通过 Docker 映射到宿主机的公网接口时，请调用此工具。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "success" 或 "error"
- `docker_info`: 包含容器名称和其绑定的宿主机端口列表。