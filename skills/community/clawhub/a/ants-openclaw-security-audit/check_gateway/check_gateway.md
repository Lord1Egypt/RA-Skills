# Tool Name: check_gateway
# Description:
用于检查目标服务器上 OpenClaw 核心网关的运行状态。
该工具会执行底层的状态查询命令，以确认网关进程是否存活及是否存在异常报错。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "success" (运行正常), "error" (发生错误) 或 "timeout" (执行超时)
- `output`: 命令行执行的原始输出信息，请根据此信息向用户总结网关状态。