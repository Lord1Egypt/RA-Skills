# Binance Announce Monitor - 币安公告 + X 账号监控技能

实时监控币安（Binance）官方公告和 X 账号动态，检测到新内容时立即通过飞书通知用户。

## 功能

- 🔍 **实时监控** - 公告 API 每 30 秒检查，X 账号每分钟检查
- 📬 **即时通知** - 检测到新动态立即发送飞书消息
- 📝 **内容摘要** - 自动提取公告/推文内容
- 🐦 **X 账号监控** - 监控 @binance 和 @binancezh 两个官方账号
- 💾 **状态持久化** - 记录已读动态，避免重复通知
- ⏰ **自动运行** - 后台持续监控，无需人工干预

## 使用场景

- 币安上币/下架公告第一时间获知
- 合约调整、交易规则变更及时知晓
- 系统维护、API 变更提前准备
- 空投、活动公告不错过
- 🐦 币安 X 账号（@binance、@binancezh）最新动态

## 安装

```bash
# 技能已内置，无需额外安装
# 确保 Node.js 18+ 已安装
```

## 配置

编辑 `config.json`（可选，使用默认值可跳过）：

```json
{
  "checkIntervalSeconds": 30,
  "targetUser": "ou_xxxxxxxxxxxxxx",
  "channel": "feishu"
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `checkIntervalSeconds` | 30 | 检查间隔（秒） |
| `targetUser` | 当前用户 | 通知接收者 open_id |
| `channel` | feishu | 通知渠道 |

## 使用方法

### 启动监控

```bash
cd skills/binance-announce-monitor
node monitor.js
```

### 后台运行（推荐）

```bash
# 使用 nohup
nohup node monitor.js > monitor.log 2>&1 &

# 或使用 screen
screen -S binance-monitor
node monitor.js
# Ctrl+A, D 退出屏幕

# 或使用 systemd（生产环境）
sudo systemctl enable binance-monitor
sudo systemctl start binance-monitor
```

### 查看状态

```bash
# 查看运行日志
tail -f monitor.log

# 查看已读公告记录
cat binance-announce-state.json

# 查看待发送通知
cat binance-pending-notify.json
```

### 停止监控

```bash
# 找到进程
ps aux | grep binance-monitor

# 停止
kill <PID>

# 或如果使用 screen
screen -r binance-monitor
# Ctrl+C
```

## 通知格式

```
📢 **币安新公告**

**{公告标题}**

{公告摘要}

👉 [查看详情](https://www.binance.com/en/support/announcement/{id})
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `monitor.js` | 主监控脚本 |
| `sender.js` | 通知发送器（可选，独立部署） |
| `config.json` | 配置文件（可选） |
| `binance-announce-state.json` | 已读公告状态（自动生成） |
| `binance-pending-notify.json` | 待发送通知队列（自动生成） |
| `binance-sent-ids.json` | 已发送记录（自动生成） |

## API 来源

- **币安公告 API**: `https://www.binance.com/bapi/composite/v1/public/cms/article/list/query`
- **公告分类 ID**: `48`（最新公告）
- **请求频率**: 每 30 秒一次（安全范围内）

## 注意事项

1. **不要设置过短的检查间隔** - 低于 10 秒可能触发 API 限流
2. **保持脚本运行** - 停止后会错过期间的公告
3. **定期清理状态文件** - 避免文件过大（脚本自动保留最近 100 条）
4. **网络要求** - 需要能访问 `www.binance.com`

## 扩展

### 添加其他交易所

复制 `monitor.js` 并修改 API URL：

```javascript
// 示例：OKX 公告
const OKX_ANNOUNCE_URL = 'https://www.okx.com/api/v5/support/announcements';

// 示例：Bybit 公告
const BYBIT_ANNOUNCE_URL = 'https://api.bybit.com/spot/v1/announcement';
```

### 添加其他通知渠道

修改 `queueNotification` 函数，支持：

- Telegram Bot
- Discord Webhook
- 微信企业机器人
- 邮件通知

### 多用户支持

在 `config.json` 中添加用户列表：

```json
{
  "users": [
    {"id": "ou_xxx1", "channel": "feishu"},
    {"id": "ou_xxx2", "channel": "telegram"}
  ]
}
```

## 故障排除

### 无法获取公告

```bash
# 测试 API 连通性
curl -s "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=5&catalogId=48" | head
```

### 通知未发送

```bash
# 检查通知队列
cat binance-pending-notify.json

# 检查已发送记录
cat binance-sent-ids.json

# 查看日志
tail -f monitor.log
```

### 重复通知

删除状态文件重置：

```bash
rm binance-announce-state.json
rm binance-sent-ids.json
```

## 版本历史

- **1.0.0** - 初始版本，支持币安公告监控 + 飞书通知

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 PR！

---

**作者**: OpenClaw Community  
**最后更新**: 2026-03-12
