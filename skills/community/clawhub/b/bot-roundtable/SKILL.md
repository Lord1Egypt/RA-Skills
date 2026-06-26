# Bot Roundtable Discussion

多Bot圆桌讨论系统 - 让飞书群里的多个Bot像真人一样讨论问题。

## 功能

- 单个Bot收到问题，自动spawn多个专业分脑
- 各分脑通过不同Bot身份发送到群聊
- 群里呈现多Bot讨论效果，像真人群聊

## 触发词

- "讨论 XXX"
- "大家怎么看"
- "多角度分析"
- "辩论 XXX"

## 使用方法

### 自动触发
在飞书群里说"讨论 XXX"即可自动触发

### 手动调用
```bash
python skills/bot-roundtable/coordinator.py "讨论问题"
```

### 手动spawn
```python
from feishu_sender import send_message_as_bot

# spawn分脑
sessions_spawn(label="tech", task="技术专家分析：XXX")
sessions_spawn(label="product", task="产品专家分析：XXX")

# 发送结果
send_message_as_bot("qiwang", chat_id, "技术观点...")
send_message_as_bot("meidou2", chat_id, "产品观点...")
```

## 文件结构

```
bot-roundtable/
├── SKILL.md           # 本文件
├── feishu_sender.py   # 飞书多Bot发消息模块
├── coordinator.py     # 协调脚本
├── config.json        # Bot凭证配置
└── README.md          # 详细文档
```

## 配置

config.json:
```json
{
  "bots": {
    "default": {"app_id": "...", "app_secret": "..."},
    "qiwang": {"app_id": "...", "app_secret": "..."},
    "meidou2": {"app_id": "...", "app_secret": "..."}
  },
  "group_chat_id": "oc_xxx"
}
```

## 依赖

- Python 3.8+
- 飞书开放平台应用（需配置 app_id + app_secret）

## 注意事项

1. 每条消息间隔0.5秒，避免频率限制
2. 消息300字以内
3. Bot凭证从 openclaw.json 的 channels.feishu.accounts 读取
