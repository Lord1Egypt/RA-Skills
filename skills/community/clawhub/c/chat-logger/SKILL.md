---
name: chat_logger
description: |
  对话记录 - 自动记录飞书/钉钉消息（严格触发规则版）
  
  ⚠️ 严格触发规则：
  - 消息 "chatlog汇总" → 只能执行此 Skill，禁止主 Agent 处理
  - 消息 "今日简报" → 只能执行此 Skill，禁止主 Agent 处理
  - 消息 "我的记录" → 只能执行此 Skill，禁止主 Agent 处理
  
  设计原则：
  - 精确匹配触发，不经过主 Agent 判断
  - 提供清晰的 API 供主 Agent 使用
  - 自检功能确保记录正常
---

# Chat Logger（严格触发规则版）

## ⚠️ 严格触发规则（AGENTS.md 必须遵守）

### 触发规则表

| 用户消息 | 执行动作 | 主 Agent 行为 |
|:---|:---|:---|
| `chatlog汇总` | 调用 `handle_chat_query()` | **禁止处理，直接返回结果** |
| `今日简报` | 调用 `handle_chat_query()` | **禁止处理，直接返回结果** |
| `我的记录` | 调用 `handle_chat_query()` | **禁止处理，直接返回结果** |
| 其他消息 | 调用 `record_message()` | 正常处理 |

### 主 Agent 必须遵守的流程

```python
from skills.chat_logger.skill import handle_chat_query, record_message

# 第1步：检查是否是 Chat-Logger 查询指令（严格匹配）
if message.strip() in ["chatlog汇总", "今日简报", "我的记录"]:
    # 严格触发规则：只能执行 Chat-Logger，禁止主 Agent 处理
    result = handle_chat_query(message, user_name, channel)
    if result:
        print(result)  # 直接返回，不执行其他逻辑
        return  # 立即返回，禁止继续处理

# 第2步：非查询指令，记录消息
record_message(channel, user_name, message, chat_type)

# 第3步：正常处理消息
# ... 主 Agent 其他逻辑
```

### 禁止行为

❌ **禁止**：主 Agent 自己读取 chat-logs 文件生成回复  
❌ **禁止**：主 Agent 修改 Chat-Logger 返回的格式  
❌ **禁止**：主 Agent 绕过 `handle_chat_query()` 直接查询  

✅ **必须**：严格匹配指令，直接调用 `handle_chat_query()`  
✅ **必须**：返回结果后立即 `return`，禁止继续执行  
✅ **必须**：非查询指令才调用 `record_message()` 和正常处理  

## 核心设计

## 核心设计

### 方案B：Hook + 显式调用双保险

**记录功能（双保险）：**
- ✅ **Hook 自动记录** - `on_incoming_message_hook` 自动触发
- ✅ **主 Agent 显式调用** - `record_message()` 备用
- ✅ **两者都执行** - 确保消息不丢失

**查询功能（主 Agent 显式调用）：**
- ✅ `handle_chat_query()` - 主 Agent 检查并处理查询指令
- ✅ 查询前自动记录当前消息

### 为什么用双保险？

| 方案 | 优点 | 缺点 |
|:---|:---|:---|
| 纯 Hook | 自动，无需干预 | Hook 可能失效，难调试 |
| 纯显式调用 | 可控，易调试 | 依赖主 Agent 遵守约定 |
| **双保险（方案B）** | **自动 + 可控** | **稍复杂，但最可靠** |

## 使用方式

### 1. 主 Agent 调用约定（AGENTS.md）

**每次收到用户消息时，必须调用：**

```python
from skills.chat_logger.skill import record_message

# 记录用户消息
record_message(
    channel="feishu",  # 或 "dingtalk"
    user_name="孟凡军",
    user_content="用户消息内容",
    chat_type="direct"  # direct=私聊, group=群聊（群聊自动跳过）
)
```

### 2. 查询指令处理

**当用户发送查询指令时，调用：**

```python
from skills.chat_logger.skill import handle_chat_query

result = handle_chat_query(
    message="chatlog汇总",
    user_name="孟凡军",
    channel="feishu"  # 当前渠道
)

if result:
    print(result)  # 直接返回结果
```

支持的查询指令：
- `chatlog汇总` - 查看所有用户完整汇总
- `今日简报` - 查看今日对话汇总
- `我的记录` - 查看个人今日记录

### 3. 自检功能

```python
from skills.chat_logger.skill import check_health

status = check_health()
print(status)
# {
#   'status': 'ok',
#   'base_dir_exists': True,
#   'base_dir_writable': True,
#   'total_channels': 2,
#   'total_users': 4,
#   'total_files': 9,
#   'last_error': None
# }
```

## API 参考

### record_message(channel, user_name, user_content, chat_type='direct')
记录用户消息

**参数：**
- `channel` (str): 渠道名称 (feishu/dingtalk/飞书/钉钉)
- `user_name` (str): 用户名称
- `user_content` (str): 用户消息内容
- `chat_type` (str): 聊天类型，默认 'direct'（私聊）

**返回：**
- `bool`: 是否记录成功

### handle_chat_query(message, user_name, channel=None)
处理查询指令

**参数：**
- `message` (str): 用户消息
- `user_name` (str): 用户名称
- `channel` (str, optional): 当前渠道

**返回：**
- `str or None`: 查询结果或 None（非查询指令）

### get_chatlog_summary() -> str
生成完整汇总报告

### get_daily_summary(user_name=None, date=None) -> str
生成每日简报

### check_health() -> dict
检查系统健康状态

## 存储结构

```
memory/chat-logs/
├── feishu/
│   └── {用户名}/
│       └── YYYY-MM-DD.md
└── dingtalk/
    └── {用户名}/
        └── YYYY-MM-DD.md
```

## 文件格式

```markdown
# 2026-03-23 提问记录 - 孟凡军（feishu）

## 提问列表

---

### 07:17
**用户**：chatlog汇总

### 07:26
**用户**：chatlog汇总
```

## 注意事项

1. **群聊自动跳过** - chat_type='group' 时自动返回 True，不记录
2. **渠道名称自动转换** - '飞书' 自动转为 'feishu'，'钉钉' 自动转为 'dingtalk'
3. **文件名安全处理** - 用户名称中的特殊字符会被替换为下划线
4. **查询前自动记录** - handle_chat_query 会先记录当前查询消息
