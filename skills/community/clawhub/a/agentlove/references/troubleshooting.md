# 故障排查

## 常见问题

### Q1: 安装后没有弹出卡片
**原因**: OpenClaw 未触发 `post_install` hook  
**解决**: 使用命令触发 `/agentlove` 或关键词"创建机器人"

### Q2: 配置完成后重启丢失
**原因**: 内存存储，会话结束即清除  
**解决**: 这是设计行为，安全考虑。配置信息已在 OpenClaw 控制台保存

### Q3: 输入验证失败
**原因**: 输入包含危险字符或过长  
**解决**: 检查输入是否包含 `<>{}[]` 等字符

### Q4: 状态管理异常
**原因**: Map 存储可能溢出  
**解决**: 重启 OpenClaw 清除所有状态

## 日志脱敏测试

```javascript
// 测试用例
sanitizeLog('token: abc123xyz789')  
// → 'token: [REDACTED]'

sanitizeLog('email: test@example.com')
// → 'email: [EMAIL_REDACTED]'

sanitizeLog('phone: 13812345678')
// → 'phone: [PHONE_REDACTED]'
```

## 安全扫描

发布前运行自检脚本：
```bash
./scripts/pre-publish-check.sh
```

检查项：
- ✅ 敏感凭证收集
- ✅ 文件写入操作
- ✅ 输入验证函数
- ✅ post_install hook
- ✅ 依赖检查
