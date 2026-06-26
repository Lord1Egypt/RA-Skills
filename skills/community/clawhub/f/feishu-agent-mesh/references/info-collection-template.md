# 信息采集模板 / Information Intake Form

将以下信息收集一次后，按需填入 `templates/accounts.example.json`，并与团队共享。

| 类别 | 需填写字段 | 说明 |
| --- | --- | --- |
| 飞书应用 | label, appId, appSecret, encryptKey, verificationToken, botName | 每个机器人一个条目。建议 label 与 Agent ID 保持一致。 |
| 回调服务 | callbackUrl | 统一回调 HTTPS 地址。 |
| 日志存储 | appToken, tableId, fieldMap | 如果使用飞书多维表格，列出真实表字段；如使用数据库，写连接方式。 |
| 群聊清单 | chatId, description, allowedBots, approvalPoints | `allowedBots` 为可入群的机器人标签；`approvalPoints` 可为空。 |
| 审批配置 | name, trigger, approverOpenIds | 在 `approvalPoints` 内定义；`trigger` 支持表达式或状态枚举。 |
| Agent 会话 | agentId, sessionKey | 用 `openclaw sessions list` 获取，确保 Relay 能向正确会话发送指令。 |
| 其它 | 例如 Bitable 字段 mapping、外部日志备份、监控通知 | 可根据业务附加。 |

> 建议把该表格复制到飞书文档或多维表格，让不同角色（IT/业务/安全）各自填写，保证一次收集即可满足全部配置需求。
