---
name: chat-bus
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  共享目录消息总线 — 让不同用户/Agent 之间通过文件系统实现聊天对话。
  支持单聊、群聊、广播、消息历史查询。
  纯 Python 标准库，零外部依赖，跨 Windows/macOS/Linux。
  通信基于共享目录（NAS/云同步/网络驱动器），用户自行配置共享路径。
---

# chat-bus — 共享目录消息总线

## 定位

让使用本技能的不同用户/Agent 之间，通过共享文件目录实现聊天对话。

## 核心规则

1. **共享目录** — 所有用户必须能访问同一个目录（NAS / OneDrive / Syncthing / SMB 挂载等）
2. **先注册再聊天** — 用户必须先 `register` 才能发送/接收消息
3. **消息即文件** — 每条消息是一个 JSON 文件，天然按时间排序，天然持久化

## 快速上手

```bash
# 用户 A 注册
python register.py '{"user":"alice","display_name":"Alice"}'

# 用户 B 注册
python register.py '{"user":"bob","display_name":"Bob"}'

# A 发消息给 B
python send.py '{"user":"alice","to":"bob","content":"你好 Bob!"}'

# B 接收消息
python receive.py '{"user":"bob"}'

# 创建群聊房间
python rooms.py '{"action":"create","user":"alice","room":"general","topic":"公共讨论"}'

# B 加入房间
python rooms.py '{"action":"join","user":"bob","room":"general"}'

# 在群里发消息
python send.py '{"user":"alice","type":"room","room":"general","content":"大家好!"}'
```

## 脚本清单

| 脚本 | 功能 | 调用方式 |
|------|------|---------|
| `register.py` | 用户注册/信息管理 | `python register.py '{"action":"register","user":"alice"}'` |
| `send.py` | 发送消息 | `python send.py '{"user":"alice","to":"bob","content":"..."}'` |
| `receive.py` | 接收新消息 | `python receive.py '{"user":"bob"}'` |
| `history.py` | 消息历史查询 | `python history.py '{"source":"inbox","user":"bob"}'` |
| `rooms.py` | 群聊房间管理 | `python rooms.py '{"action":"create","user":"alice","room":"..."}'` |

## 共享目录结构

```
.chat-bus/                     ← chat_dir（共享目录）
├── users/                     ← 用户注册信息
│   ├── alice.json
│   └── bob.json
├── inbox/                     ← 私聊收件箱
│   ├── alice/
│   │   ├── 2026-04-13_220500_bob_abc123.json
│   │   └── 2026-04-13_220600_bob_def456.json.read
│   └── bob/
└── rooms/                     ← 群聊房间
    └── general/
        ├── _room.json         ← 房间配置（成员列表等）
        ├── 2026-04-13_221000_alice_msg001.json
        └── 2026-04-13_221100_bob_msg002.json
```

## JSON 协议

- **输入**：JSON 字符串（命令行第一个参数 或 stdin）
- **输出**：`{"status":"ok","data":{...}}` 或 `{"status":"error","code":N,"message":"..."}`
- **共享目录**：通过 `chat_dir` 参数指定，默认为当前目录下 `.chat-bus/`

## 安全说明

- 消息明文存储在共享目录，不加密
- 依赖共享目录本身的访问控制（文件系统权限）
- 用户名安全化处理（仅允许字母数字下划线）
