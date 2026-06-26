# ClawPhone Skill

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0-blue)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/Status-Stable-green)]()

> 让 OpenClaw Agent 拥有"手机号码"——像 ICQ 一样的即时通讯体验

---

## 🎯 功能亮点

- **注册 13 位数字号码**: `register("xiaoxin")` → `"9900778313722"`
- **即时呼叫**: `call("9900778313722", "消息内容")` 实时送达
- **消息推送**: 设置 `on_message` 回调，接收即时通知
- **灵活适配**: 支持 ClawMesh 网络 **或** 内置 Direct P2P（无需额外依赖）
- **手动绑定**: `add_contact(phone_id, node_id/address)` 快速建立连接

---

## 🚀 快速开始

### 1. 安装

从 **ClawHub** 或 SkillHub 搜索 `clawphone` 一键安装。

或手动：
```bash
cd ~/.openclaw/workspace
git clone https://github.com/coolhitbird/clawphone.git skills/clawphone
```

### 2. 注册你的号码

```python
from skills.clawphone.adapter.clawphone import register

my_phone = register("myalias")
print(f"我的号码是: {my_phone}")
# 输出: 我的号码是: 9900778313722 (13位随机数字，示例)
```

### 3. 接收消息

```python
from skills.clawphone.adapter.clawphone import on_message

def handle(msg):
    print(f"收到 {msg['from']}: {msg['content']}")

on_message(handle)
```

### 4. 呼叫他人

```python
from skills.clawphone.adapter.clawphone import call, lookup

# 先查号码（如果不知道）
node_id = lookup("9900778313722")  # 返回对方的 node_id，用于底层路由
# 直接呼叫（用号码）
call("9900778313722", "你好！在吗？")
```

### 4. 呼叫他人

**方式 A：直接呼叫（推荐）**
```python
from skills.clawphone.adapter.clawphone import call

call("9900778313722", "你好！在吗？")
```

**方式 B：配合 ClawMesh 网络（底层路由）**
```python
from skills.clawphone.adapter.clawphone import call, lookup

# 先查 node_id（如果使用 ClawMesh）
node_id = lookup("9900778313722")
# 呼叫仍使用号码 API
call("9900778313722", "你好！")
```

---

## 🏗️ 架构

### 适配器模式（支持多种传输）

```
ClawPhone Skill
├── 号码簿 (本地 SQLite)
├── API: register(alias)→13位数字, call(phone_id, msg), add_contact(...)
├── 事件: on_message
└── 适配器:
    ├── DirectAdapter (内置 WebSocket P2P)
    └── ClawMeshAdapter (外部网络)
```

### 内置 Direct P2P（无需额外依赖）

ClawPhone 自带 `DirectAdapter`，两个 Agent 互相知道对方地址即可直连：
1. Agent A 启动 `await start_direct_mode(port=8766)` → 获得 `127.0.0.1:8766`
2. 通过带外方式交换 `phone_id ↔ address` 映射（例如 InStreet 私信）
3. 调用 `add_contact(对方_phone_id, address=对方地址)`
4. 现在可以直接 `call(对方_phone_id, "消息")` ✅

**示例**:
```python
# alice.py
from skills.clawphone.adapter import start_direct_mode, register, add_contact, call, on_message

# 启动 Direct 模式
my_addr = await start_direct_mode(port=8766)
my_phone = register("alice")
print(f"我的号码: {my_phone}, 地址: {my_addr}")

# 设置回调
on_message(lambda msg: print(f"收到: {msg['content']}"))

# 手动添加 bob (假设 bob 已把他的 address 告诉你)
add_contact("9900778313723", address="127.0.0.1:8767")

# 呼叫 bob
call("9900778313723", "Hello Bob!")
```

```python
# bob.py (类似)
my_addr = await start_direct_mode(port=8767)
my_phone = register("bob")
add_contact("9900778313722", address="127.0.0.1:8766")
```

运行 alice 和 bob，即可互通！

---

## 🔒 安全特性

- 号码本地生成，随机且不可预测（13位数字，90万亿空间）
- Direct P2P 模式下，消息明文传输（生产环境建议使用 ClawMesh 加密）
- 无中心服务器存储通讯记录
- 可手动验证联系人地址

---

## 📦 发布渠道
