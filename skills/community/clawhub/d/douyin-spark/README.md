# 抖音自动续火花 Skill

🔥 自动为抖音私信联系人续火花，保持火花标识不灭！

## 安装

### 方法 1：本地安装（推荐）

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/douyin-spark

# 链接到全局
npm link
```

### 方法 2：直接使用

技能已内置在 OpenClaw 工作区，可直接使用。

## 使用

### 命令行使用

```bash
# 续火花（默认消息）
douyin-spark

# 续火花（自定义消息）
douyin-spark --message "你好，来聊天了"

# 查看联系人列表
douyin-spark --list

# 添加联系人
douyin-spark --add "用户名"

# 移除联系人
douyin-spark --remove "用户名"

# 查看帮助
douyin-spark --help
```

### 在 OpenClaw 对话中使用

直接告诉 AI 助手：

```
帮我续火花
给火花联系人发消息
续火花，说：你好呀
查看火花联系人列表
```

## 火花联系人管理

联系人列表保存在：`~/.openclaw/workspace/memory/douyin-spark-contacts.md`

### 添加联系人

当发现新的火花联系人时（名字旁边有数字/火花图标）：

```bash
douyin-spark --add "用户名"
```

或在对话中说："把 XXX 加到火花联系人列表"

### 移除联系人

```bash
douyin-spark --remove "用户名"
```

## 火花规则说明

| 状态 | 说明 | 操作 |
|------|------|------|
| 🔥 彩色火花 | 正常状态，连续聊天中 | 每天发消息保持 |
| 🌫️ 灰色火花 | 超过 24 小时未聊天 | 发消息重新点亮 |
| ⏳ 重燃中 | 火花已灭，恢复中 | 连续聊 3 天恢复 |

## 注意事项

1. **每天至少发一次消息** - 保持火花不灭
2. **避免相同内容** - 可能被抖音限流
3. **群聊也有火花** - 多人聊天同样适用
4. **浏览器需登录** - 确保抖音网页版已登录

## 自动化建议

可以设置每日定时任务：

```bash
# 使用 cron 每天下午 6 点执行
0 18 * * * douyin-spark
```

或在 OpenClaw 中使用 HEARTBEAT.md 设置定期检查。

## 故障排除

### 浏览器无法连接

```bash
# 重启 OpenClaw gateway
openclaw gateway restart
```

### 消息发送失败

1. 检查抖音网页版是否已登录
2. 检查浏览器是否正常运行
3. 确认联系人列表格式正确

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 支持批量发送续火花消息
- 支持联系人列表管理
- 支持自定义消息内容

## 许可证

MIT License
