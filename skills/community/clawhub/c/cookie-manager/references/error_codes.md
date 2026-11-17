# 错误码定义 - cookie-manager

> 来源: SKILL.md v3.0 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| COOKIE_MANAGER_OK | 操作成功 | 无需处理 |
| NO_COOKIE | 无Cookie配置 | 返回失败,提示配置.env中的XIANYU_COOKIE_1 |
| HTTPX_NOT_INSTALLED | httpx库未安装 | 仅执行格式检查,告警提示安装httpx |
| TIMEOUT | 网络请求超时 | 标记该Cookie为TIMEOUT状态,下次保活时重试 |
| MCP_UNAVAILABLE | fishclaw-mcp不可用 | 跳过深度检查,仅执行HTTP轻量检查 |
| ALERT_FAILED | QQBot告警发送失败 | 降级为本地文件日志记录 |
| DB_NOT_CONNECTED | 数据库未连接 | 仍执行Cookie检查+保活,跳过审计表写入 |
| BACKUP_FAILED | 备用Cookie也失效 | 全部暂停操作+发送紧急CRITICAL告警 |
| SYNC_PARTIAL_FAILED | 4端Cookie同步部分失败 | 逐端重试3次,记录失败端 |
| DEGRADE_FAILED | 降级模式启动失败 | 记录错误+发送ERROR告警+人工介入 |
| RATE_LIMITED | Cookie切换触发平台风控 | 立即停止切换+等待≥17分钟后重试 |
| DECRYPT_FAILED | Fernet解密Cookie失败 | 跳过该Cookie,记录审计日志 |
