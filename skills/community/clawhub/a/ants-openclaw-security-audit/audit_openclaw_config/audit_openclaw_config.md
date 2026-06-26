# Tool Name: audit_openclaw_config
# Description:
依据 OpenClaw 官方安全指南 (Gateway/Security)，对本地的 `openclaw.json` 配置文件进行静态基线审计。
重点检查以下官方明确警告的高危层级配置：
1. **日志脱敏**: `logging` 层级下的 `redactSensitive` 是否被危险地设为 "off"。
2. **群组策略**: 根层级的 `groupPolicy` 是否为 "open"。
3. **私信策略**: 根层级的 `dmPolicy` 是否为 "open"。
4. **UI 认证降级**: `gateway.controlUi` 层级下的 `allowInsecureAuth` 和 `dangerouslyDisableDeviceAuth`。
5. **多用户会话隔离**: `session` 层级下的 `dmScope`。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含：
- `status`: "clean" (符合安全基线) 或 "risks_found" (发现基线偏离)。
- `checked_file`: 读取的 `openclaw.json` 绝对路径。
- `findings`: 发现的具体配置风险及官方建议的修复方案。