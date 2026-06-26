# Tool Name: openclaw_security_audit
# Description:
调用 OpenClaw 官方内置的命令行安全审计工具 (`openclaw security audit`) 进行只读扫描。
该工具能深度检查内部安全隐患，包括：Gateway 网关认证暴露、浏览器控制暴露、提权白名单配置、以及敏感文件的系统读写权限（如 ~/.openclaw, credentials 等）。
本工具仅用于诊断，不会修改任何系统配置或权限。

# Parameters:
包含一个可选参数 `mode` (字符串类型)。
- `standard` (默认): 执行常规的基础安全审计。
- `deep`: 执行深度审计 (`--deep`)，检查更底层的配置风险。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "success" (未发现问题), "issues_found" (发现安全隐患) 或 "error" (执行错误)。
- `mode`: 当前执行的扫描模式。
- `audit_output`: OpenClaw 命令行返回的详细审计报告原文。请根据此报告向用户提供手动修复建议。