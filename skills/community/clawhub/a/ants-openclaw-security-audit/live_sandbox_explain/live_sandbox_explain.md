# Tool Name: live_sandbox_explain
# Description:
调用官方自带的诊断命令 `openclaw sandbox explain`。
它会从正在运行的 Gateway 网关进程中提取实际生效的沙箱规则心智模型（包括被阻止/被允许的工具，以及最终执行的层级）。
这能有效排查多智能体覆盖（Multi-agent Overrides）导致的配置冲突问题。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含：
- `status`: "success" 或 "error"。
- `explain_output`: 命令行返回的实时沙箱规则策略树（纯文本结构）。