# 错误码定义 - account-manager

> 来源: SKILL.md v1.0 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| ACCOUNT_NOT_FOUND | 旧账号不存在 | 检查账号ID是否正确,确认账号已在系统中注册 |
| ACCOUNT_ALREADY_EXISTS | 新账号已存在 | 使用其他account_id,避免ID冲突 |
| DEVICE_LOGIN_FAILED | 设备登录失败 | 重试登录或检查设备状态,确认device-operations-mcp可用 |
| DATA_MIGRATION_FAILED | 数据迁移失败 | 部分迁移或手动迁移好友档案和聊天记忆 |
| PLATFORM_NOT_SUPPORTED | 平台不支持 | 添加对应平台支持,确认platform参数正确 |
| MCP_NOT_CONNECTED | MCP未连接 | 检查openclaw.json配置,重启Gateway |
