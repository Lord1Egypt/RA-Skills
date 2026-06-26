---
name: evermemos
description: 集成 EverMemOS 记忆系统。用于存储对话记忆、检索历史、构建长期记忆。当用户说"记住"、"存储记忆"、"查询记忆"、"关于...的记忆"时使用此技能。
version: 1.0.0
author: OpenClaw Community
---

# EverMemOS 记忆技能

集成 EverMemOS 生产级 AI 记忆系统，让 AI 具有长期记忆能力。

> 📝 **配置说明**：使用前需要配置 EverMemOS 服务器地址和 API Key

## 快速配置

### 1. 安装 EverMemOS 服务器

参考官方文档：https://github.com/evermemos/EverMemOS

### 2. 配置技能

在环境中设置以下变量：
- `EVERMEMOS_URL` - EverMemOS API 地址 (默认: http://localhost:1995)
- `EVERMEMOS_API_KEY` - API Key (如需要)

### 3. Docker 快速启动

```bash
# 启动所有服务
cd EverMemOS
docker-compose up -d

# 确认服务运行
docker ps | grep memsys
```

## 记忆存储

### 1. 基本存储 (单条消息)

```bash
curl -X POST ${EVERMEMOS_URL}/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg_001",
    "content": "用户今天学习了AI部署",
    "sender": "user",
    "create_time": "2026-03-16T06:00:00Z",
    "scene": "assistant"
  }'
```

### 2. Python 存储函数

```python
import os
import requests
from datetime import datetime

EVERMEMOS_URL = os.getenv("EVERMEMOS_URL", "http://localhost:1995")

def store_memory(content, sender="user", user_id="default"):
    """存储记忆到 EverMemOS"""
    data = {
        "message_id": f"msg_{int(datetime.now().timestamp()*1000)}",
        "content": content,
        "sender": sender,
        "user_id": user_id,
        "create_time": datetime.utcnow().isoformat() + "Z",
        "scene": "assistant"
    }
    resp = requests.post(f"{EVERMEMOS_URL}/api/v1/memories", json=data)
    return resp.json()

# 使用示例
store_memory("用户部署了EverMemOS记忆系统", "user")
```

### 3. 自动存储要点

```python
def save_conversation_summary(messages):
    """从对话中提取关键点并存储"""
    for msg in messages:
        if is_important(msg):  # 判断是否为关键信息
            store_memory(
                content=msg["content"],
                sender=msg["sender"],
                metadata={"type": "conversation_summary"}
            )
```

## 记忆检索

### 1. 获取历史记忆

```bash
# 按用户ID获取
curl "${EVERMEMOS_URL}/api/v1/memories?user_id=user_001&limit=10"
```

### 2. 语义搜索

```bash
curl -X POST ${EVERMEMOS_URL}/api/v1/memories/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "关于部署的记忆",
    "user_id": "user_001",
    "retrieve_method": {
      "method": "semantic",
      "top_k": 5
    }
  }'
```

### 3. 检索方法选择

| 方法 | 适用场景 | 示例 |
|------|----------|------|
| keyword | 精确查找 | 查找"部署"相关记忆 |
| vector | 语义搜索 | 查找"AI助手相关"记忆 |
| hybrid | 综合需求 | 结合关键词和语义 |
| agentic | 复杂推理 | LLM 引导多轮检索 |

## 记忆类型

| 类型 | 用途 | 示例 |
|------|------|------|
| EPISODIC_MEMORY | 对话事件 | "用户学会了部署AI" |
| PROFILE | 用户画像 | "用户喜欢简洁界面" |
| FORESIGHT | 未来计划 | "用户打算学习LangChain" |
| EVENT_LOG | 原子事实 | "用户部署了MongoDB" |

## 常用命令

### 服务管理

```bash
# 查看 API 状态
curl ${EVERMEMOS_URL}/health

# 查看已存储记忆数量 (服务器上)
docker exec memsys-mongodb mongosh -u <username> -p <password> --authenticationDatabase admin memsys --quiet --eval 'db.episodic_memories.countDocuments()'
```

## 触发关键词

当用户说以下内容时，自动使用此技能：

- "记住..." / "存储记忆" / "保存这个"
- "记得之前..." / "之前说过..."
- "查询记忆" / "搜索记忆"
- "关于...的记忆"
- "我之前让你做过什么"
- "我的偏好是..."

## 自动记忆触发

在以下时机自动存储记忆：

1. **对话结束** - 提取关键要点
2. **用户自我介绍** - 存储用户信息
3. **任务完成** - 记录完成内容
4. **用户偏好表达** - 记住偏好设置

## 完整示例

```python
import os
import requests
import time
from datetime import datetime

class EverMemOS:
    def __init__(self, url=None, user_id="default"):
        self.base_url = url or os.getenv("EVERMEMOS_URL", "http://localhost:1995")
        self.user_id = user_id
    
    def store(self, content, sender="user"):
        """存储记忆"""
        return requests.post(
            f"{self.base_url}/api/v1/memories",
            json={
                "message_id": f"msg_{int(time.time()*1000)}",
                "content": content,
                "sender": sender,
                "user_id": self.user_id,
                "create_time": datetime.utcnow().isoformat() + "Z",
                "scene": "assistant"
            }
        ).json()
    
    def recall(self, query, top_k=5):
        """检索记忆"""
        return requests.post(
            f"{self.base_url}/api/v1/memories/retrieve",
            json={
                "query": query,
                "user_id": self.user_id,
                "retrieve_method": {"method": "hybrid", "top_k": top_k}
            }
        ).json()
    
    def get_all(self, limit=20):
        """获取所有记忆"""
        return requests.get(
            f"{self.base_url}/api/v1/memories",
            params={"user_id": self.user_id, "limit": limit}
        ).json()

# 使用
memory = EverMemOS(user_id="user_001")

# 存储
memory.store("用户部署了EverMemOS")

# 检索
results = memory.recall("关于部署的记忆")
for r in results.get("memories", []):
    print(r["content"])
```

## 注意事项

1. **首次配置** - 需要先部署 EverMemOS 服务器
2. **边界检测** - 系统自动检测对话边界触发记忆提取
3. **LLM 依赖** - 完整功能需要可访问的 LLM API

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| API 无法访问 | 检查服务器状态，确认端口 |
| 记忆未提取 | 检查 LLM API 是否可用 |
| 查询返回空 | 确认 user_id 正确 |

---

**作者**: OpenClaw Community  
**版本**: 1.0.0  
**最后更新**: 2026-03-16
