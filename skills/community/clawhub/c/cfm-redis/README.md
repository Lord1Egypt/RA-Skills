# ⚡ CFM Redis - 跨框架AI Agent实时通信

基于Redis Pub/Sub的跨框架Agent通信方案。事件驱动，毫秒级延迟，通信零token消耗。

## 核心优势

- ⚡ **实时通信** - 消息延迟 < 10ms
- 💰 **通信零token** - Redis直接传递，不消耗LLM token
- 🔄 **双向通信** - 支持任意框架之间通信
- 💾 **消息持久化** - 自动保存历史记录
- 🔍 **Agent发现** - 自动发现网络中的Agent

## 快速开始

### 1. 安装Redis

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# 验证
redis-cli ping  # 应返回 PONG
```

### 2. 安装Python依赖

```bash
pip install redis
```

### 3. 下载CFM库

```bash
mkdir -p ~/.shared/cfm
# 将 cfm_messenger.py 和 cfm_cli.py 放入此目录
```

## 使用方法

### 发送消息

```bash
cd ~/.shared/cfm
python3 cfm_cli.py send chanel "你好！" --from hermes
```

### 监听消息

```bash
python3 cfm_cli.py listen chanel --timeout 30
```

### 查看历史

```bash
python3 cfm_cli.py history hermes
```

## OpenClaw自动检查配置

### 添加Cron任务（每分钟检查）

```bash
openclaw cron add --name "cfm-check" --every 1m --agent main --message "执行以下Python脚本检查CFM消息：

\`\`\`python
import redis, json
r = redis.Redis(decode_responses=True)
msgs = r.lrange('cfm:chanel:messages', 0, 20)
hermes_msgs = [json.loads(m) for m in msgs if json.loads(m).get('from') == 'hermes']
print(f'共 {len(hermes_msgs)} 条消息')
for msg in hermes_msgs[:3]:
    print(f'[{msg[\"timestamp\"]}] {msg[\"content\"]}')
r.close()
\`\`\`

如果有新消息，告诉我内容。如果没有，说'无新消息'。"
```

### 查看Cron任务

```bash
openclaw cron list
```

### 删除Cron任务

```bash
openclaw cron rm <job-id>
```

## 消息格式

```json
{
  "id": "a1b2c3d4",
  "from": "hermes",
  "to": "chanel",
  "type": "text",
  "content": "消息内容",
  "timestamp": "2026-04-16T01:30:00.000000"
}
```

## 性能特点

| 指标 | 值 |
|------|-----|
| 消息延迟 | < 10ms |
| 内存占用 | ~10MB (Redis) |
| 吞吐量 | 1000+ msg/s |
| 持久化 | 最近1000条/Agent |

## 适用场景

- ✅ 跨框架实时通信（Hermes ↔ OpenClaw）
- ✅ 高频消息（>10条/分钟）
- ✅ 需要消息持久化
- ✅ 多Agent协作

## 与文件信箱对比

| 特性 | 文件信箱 | CFM Redis |
|------|----------|-----------|
| 实时性 | 🐢 延迟1-5分钟 | ⚡ < 10ms |
| 依赖 | 无 | Redis |
| Token消耗 | 按轮询频率 | 通信零token |
| 可靠性 | 高 | 高 |
| 扩展性 | 2个Agent | 多Agent |

## 故障排除

### Redis连接失败

```bash
redis-cli ping  # 检查Redis状态
brew services restart redis  # 重启Redis
```

### Python导入错误

```bash
pip install redis
python3 -c "import redis; print('✅ 导入成功')"
```

## 许可证

MIT License

---

**CFM Redis — 让跨框架Agent通信像本地聊天一样流畅！** ⚡
