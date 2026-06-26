# 常见问题 FAQ

## 配置相关

### Q: 配置格式是什么？

A: 使用 `accounts` + `bindings` 格式：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "writer": { "appId": "xxx", "appSecret": "xxx" }
      }
    }
  },
  "bindings": [
    { "agentId": "writer", "match": { "channel": "feishu", "accountId": "writer" } }
  ]
}
```

### Q: 可以用环境变量吗？

A: 不建议。`${VAR}` 不会被自动展开，必须填入实际值。

### Q: 可以配置几个 Agent？

A: 理论上无限制，但建议 2-6 个为宜。

## 飞书开放平台

### Q: 事件订阅显示"未检测到应用连接"

A: 这是正常的。先保存配置，然后重启 Gateway，飞书会自动检测到连接。

### Q: 权限导入失败

A: 确保使用的是"批量导入/导出权限"功能，不要手动添加。

### Q: 应用发布后多久生效？

A: 通常立即生效，但可能需要 1-2 分钟传播。

## 配对相关

### Q: 没收到配对码

A: 检查：
1. 飞书应用是否已添加为联系人
2. 事件订阅是否配置正确
3. Gateway 是否重启

### Q: 配对码过期了

A: 重启 Gateway 会生成新的配对码。

## 消息相关

### Q: 机器人能收到消息但不回复

A: 检查：
1. Agent 模型配置是否正确
2. 是否有可用模型
3. 查看日志是否有错误

### Q: 消息延迟很高

A: 检查网络连接和 Gateway 负载。

## 调试相关

### Q: 如何查看日志？

A: `tail -f /tmp/openclaw/openclaw-*.log`

### Q: 如何检查配置？

A: `openclaw skill run feishu-multiagent-onboard --check`

### Q: 如何诊断问题？

A: `openclaw skill run feishu-multiagent-onboard --debug`

---

*持续更新中...*
