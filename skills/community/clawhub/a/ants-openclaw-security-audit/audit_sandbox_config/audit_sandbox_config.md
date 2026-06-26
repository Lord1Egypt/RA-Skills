# Tool Name: audit_sandbox_config
# Description:
深度审计 OpenClaw 配置文件中与 Docker 沙箱 (Sandboxing) 相关的安全基线。
排查官方文档中警告的常见沙箱逃逸和权限滥用风险：
1. **沙箱模式**: 检查 `agents.defaults.sandbox.mode` 是否处于危险的 "off" 状态（这会导致所有命令直接在宿主机执行）。
2. **工作区越权**: 检查 `workspaceAccess` 是否被过度授权为 "rw"（读写模式），官方建议默认为 "none" 或 "ro"（只读）。
3. **高危挂载 (Binds)**: 扫描 `sandbox.docker.binds` 数组，检查是否将宿主机的敏感目录（如 `/var/run/docker.sock`, `/etc`, `/root`）以 "rw" 模式挂载到了沙箱内部，这会导致直接的容器逃逸。
4. **网络暴露**: 检查是否为不需要联网的沙箱修改了默认的 `network: "none"`。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "clean" (沙箱配置严密) 或 "risks_found" (发现沙箱逃逸隐患)。
- `findings`: 具体的沙箱配置风险及官方建议的修复方案。