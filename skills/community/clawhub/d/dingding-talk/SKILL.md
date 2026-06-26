---
name: dingding-talk
version: 2.2.0
description: Windows 电脑端钉钉消息自动发送技能，通过键盘模拟给指定联系人发送消息。快捷命令：dt
triggers:
  - dt
  - 钉钉发送
  - 发钉钉
---

# DingDing Talk

Windows 电脑端钉钉消息自动发送技能。

## 功能

- 👤 搜索并打开联系人聊天窗口
- ✉️ 给指定联系人发送消息（自动追加后缀）
- 🔄 批量发送（智能优化执行步骤）
- ⌨️ 纯键盘模拟，无需 API

## 安装

需要先安装 Python 依赖：

```bash
pip install pyautogui pygetwindow pillow pyperclip
```

## 使用方法

### 1. 发送消息到指定联系人

```bash
python send_batch.py "[王沛]" "消息内容"
```

### 2. 批量发送（轮询模式）

```bash
# 初始化并发送第一条
python send_batch.py "[王沛，高哲，贾福果]" "消息内容"

# 继续发送下一条
python send_batch.py --next

# 继续发送下一条
python send_batch.py --next
```

**注意**: 联系人格式必须为 `[A,B,C]` 格式

### 3. 获取钉钉状态

```python
from server import get_dingding_status
status = get_dingding_status()
```

## 执行流程

### 标准步骤

| 步骤 | 操作 | 快捷键/方法 | 延迟 |
|------|------|-------------|------|
| 1 | 打开钉钉 | `Ctrl+Shift+Z` | 1.0s |
| 2 | 最大化钉钉窗口 | `Win+↑` | 0.5s |
| 3 | 点击坐标激活窗口 | `click(1000, 30)` | 0.3s |
| 4 | 输入联系人名称 | `Ctrl+A` → `Delete` → `Ctrl+V` | 0.5s |
| 5 | 等待搜索结果加载 | - | 2.0s |
| 6 | 打开聊天窗口 | `Enter` | 0.5s |
| 7 | 点击坐标激活输入框 | `click(1300, 1150)` | 0.3s |
| 8 | 输入消息内容 | `Ctrl+V` | 0.3s |
| 9 | 发送消息 | `Enter` | 0.3s |
| 10 | 还原窗口 | `Win+↓` | 0.3s |

### 智能执行逻辑

| 场景 | 位置 | 执行步骤 | 说明 |
|------|------|----------|------|
| **单人发送** | 唯一 | Step 1-10 | 完整流程 |
| **多人发送** | 第一个人 | Step 1-9 | 不还原窗口 |
| **多人发送** | 中间人 | Step 3-9 | 跳过打开、最大化、还原 |
| **多人发送** | 最后一个人 | Step 3-10 | 跳过打开、最大化，还原窗口 |

## 输入格式

### 联系人格式

**必须为 `[A,B,C]` 格式**

✅ 正确示例:
```bash
python send_batch.py "[王沛]" "消息"
python send_batch.py "[王沛，高哲]" "消息"
```

❌ 错误示例:
```bash
python send_batch.py "王沛" "消息"      # 缺少括号
python send_batch.py "王沛，高哲" "消息"  # 缺少括号
```

错误时返回：`请输入正确的发送人格式`

### 消息内容

**自动追加后缀**: 所有消息会自动在末尾追加 `【OpenClaw 自动发送】`

| 输入 | 实际发送 |
|------|---------|
| `测试` | `测试【OpenClaw 自动发送】` |
| `你好` | `你好【OpenClaw 自动发送】` |

## 注意事项

1. 钉钉 PC 客户端需要已安装并登录
2. 发送消息时会自动激活钉钉窗口
3. 中文输入需要确保系统中文输入法正常工作
4. 执行过程中不要干扰键盘操作
5. 批量发送时请保持窗口打开状态，不要手动关闭
6. 联系人格式必须为 `[A,B,C]` 格式
7. 消息会自动追加 `【OpenClaw 自动发送】` 后缀

## 文件结构

```
dingding-talk/
├── server.py       # 核心实现
├── send_batch.py   # 批量发送脚本
├── requirements.txt
├── send_queue.json # 批量队列（临时）
└── SKILL.md
```
