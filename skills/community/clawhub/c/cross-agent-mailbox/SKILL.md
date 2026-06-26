---
name: cross-agent-mailbox
description: 文件信箱方案 - 跨框架Agent通信（适用于任何框架）
metadata:
  openclaw:
    requires:
      bins: []
    homepage: https://github.com/AmeyLover/cross-agent-mailbox
    install:
      localPath: https://github.com/AmeyLover/cross-agent-mailbox.git
---

# 📬 Cross-Agent Mailbox - 文件信箱通信

跨框架Agent通信的最简单方案。适用于任何AI框架之间的通信（Hermes、OpenClaw、Claude等）。

## 核心理念

两个Agent共享一个文件目录，通过写信/读信方式通信。简单、可靠、无依赖。

## 工作原理

```
Agent A → 写信到 → shared-mailbox/a-to-b/ → Agent B 读取
Agent B → 写信到 → shared-mailbox/b-to-a/ → Agent A 读取
```

## 安装

### 1. 创建信箱目录

```bash
mkdir -p ~/.shared-mailbox/{agent-a-to-b,agent-b-to-a}/{archive}
```

### 2. 创建通信协议文件

```bash
cat > ~/.shared-mailbox/README.md << 'EOF'
# 跨Agent通信信箱

## 目录结构
- agent-a-to-b/: Agent A 发给 Agent B 的信件
- agent-b-to-a/: Agent B 发给 Agent A 的信件
- archive/: 已处理的信件

## 信件格式
文件名: YYYY-MM-DD_NNN_主题.md
内容: Markdown格式，包含发件人、收件人、时间、内容
EOF
```

## 信件格式模板

```markdown
# 📬 主题

**发件人**：Agent名称
**收件人**：Agent名称  
**时间**：YYYY-MM-DD HH:MM
**类型**：通知/回复/请求

---

信件内容...

**签名**
时间
```

## 使用方法

### 发送信件

```python
import os
from datetime import datetime

def send_letter(to_agent, content, subject="通信"):
    # 根据目标选择目录
    if to_agent == "agent-b":
        mailbox = os.path.expanduser("~/.shared-mailbox/agent-a-to-b/")
    else:
        mailbox = os.path.expanduser("~/.shared-mailbox/agent-b-to-a/")
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}_{subject}.md"
    
    # 写入信件
    with open(os.path.join(mailbox, filename), "w") as f:
        f.write(content)
    
    return filename
```

### 检查新信件

```python
import os

def check_mail(my_mailbox):
    """检查是否有新信件（排除archive目录）"""
    mailbox = os.path.expanduser(f"~/.shared-mailbox/{my_mailbox}/")
    
    new_letters = []
    for f in os.listdir(mailbox):
        if f.endswith(".md") and not f.startswith("."):
            new_letters.append(f)
    
    return sorted(new_letters)
```

### 归档信件

```python
import shutil

def archive_letter(mailbox, filename):
    """处理完后归档"""
    src = os.path.expanduser(f"~/.shared-mailbox/{mailbox}/{filename}")
    dst = os.path.expanduser(f"~/.shared-mailbox/{mailbox}/archive/{filename}")
    shutil.move(src, dst)
```

## 触发机制选择

### 方案A：定时轮询（简单）

创建cron任务，每5-10分钟检查一次信箱：

```bash
# 每5分钟检查
*/5 * * * * cd /path/to/scripts && python3 check_mail.py
```

**优点**：简单，任何框架都能用
**缺点**：有延迟，消耗token

### 方案B：文件监控（推荐）

使用 `watchdog` 监控文件变化：

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MailHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".md"):
            print(f"📬 新信件: {event.src_path}")
            # 触发处理

observer = Observer()
observer.schedule(MailHandler(), mailbox_path, recursive=False)
observer.start()
```

**优点**：实时，几乎零token
**缺点**：需要常驻进程

## 通信规范

### 命名约定
- Agent A → Agent B: `agent-a-to-b/`
- Agent B → Agent A: `agent-b-to-a/`

### 文件命名
```
YYYY-MM-DD_NNN_简短主题.md
例: 2026-04-15_001_打招呼.md
```

### 处理流程
1. 检查信箱目录
2. 读取新信件
3. 处理内容
4. 回复信件（可选）
5. 归档已处理信件

## ⚠️ 已读机制（必须！避免重复读取）

**踩坑经验（2026-04-18）**：没有已读机制时，每次检查信箱都会重新读取所有历史消息，导致效率低下。

### 创建已读状态文件

```json
{
  "version": 1,
  "lastUpdated": "2026-04-18T22:55:00+08:00",
  "readStatus": {
    "hermes-to-chanel": {
      "lastReadFile": "2026-04-17_013_回复-Workspace目录评估.md",
      "readFiles": ["2026-04-17_001_身份提醒.md"],
      "lastReadAt": "2026-04-18T22:38:00+08:00"
    },
    "chanel-to-hermes": {
      "lastReadFile": "2026-04-17_010_紧急-Workspace目录检查结果.md",
      "readFiles": [],
      "lastReadAt": null
    }
  }
}
```

### 使用规则

1. **读信件前**：先读 `read-status.json` 获取上次读到哪个文件
2. **只读新信件**：跳过已读文件，只读新增的 `.md` 文件
3. **读完后**：更新 `read-status.json` 记录最新已读状态

### Python实现

```python
import json
import os
from pathlib import Path

def get_unread_letters(mailbox_dir: str, status_file: str) -> list:
    """获取未读信件列表"""
    # 读取已读状态
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
    
    mailbox_name = os.path.basename(mailbox_dir)
    read_status = status.get('readStatus', {}).get(mailbox_name, {})
    read_files = set(read_status.get('readFiles', []))
    
    # 获取所有信件
    all_letters = []
    for f in os.listdir(mailbox_dir):
        if f.endswith('.md') and not f.startswith('.'):
            all_letters.append(f)
    
    # 过滤已读
    unread = [l for l in sorted(all_letters) if l not in read_files]
    return unread

def mark_as_read(mailbox_dir: str, status_file: str, filename: str):
    """标记信件为已读"""
    # 读取现有状态
    status = {}
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
    
    mailbox_name = os.path.basename(mailbox_dir)
    if 'readStatus' not in status:
        status['readStatus'] = {}
    if mailbox_name not in status['readStatus']:
        status['readStatus'][mailbox_name] = {'readFiles': [], 'lastReadFile': None}
    
    # 更新状态
    read_status = status['readStatus'][mailbox_name]
    if filename not in read_status['readFiles']:
        read_status['readFiles'].append(filename)
    read_status['lastReadFile'] = filename
    read_status['lastReadAt'] = datetime.now().isoformat()
    status['lastUpdated'] = datetime.now().isoformat()
    
    # 保存
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
```

### 快捷命令

```bash
# 查看未读信件
cat ~/.shared-mailbox/read-status.json | jq '.readStatus."hermes-to-chanel".lastReadFile'

# 对比已读状态
ls -1t ~/.shared-mailbox/hermes-to-chanel/*.md | head -5
```

---

## 故障排除

### 信件没收到
1. 检查目录权限
2. 确认文件名格式正确
3. 查看archive目录是否已归档

### 信件重复处理
- 使用已读机制避免重复
- 处理后更新 `read-status.json`

## 适用场景

- ✅ 跨框架通信（Hermes ↔ OpenClaw）
- ✅ 简单可靠的通信需求
- ✅ 不需要实时性的场景
- ✅ 无额外依赖要求

## 不适用场景

- ❌ 需要实时通信（用 CFM Redis）
- ❌ 高频消息（>10条/分钟）
- ❌ 需要消息持久化和查询

## 与其他方案对比

| 方案 | 实时性 | 依赖 | 复杂度 | token消耗 |
|------|--------|------|--------|-----------|
| 文件信箱 | 🐢 延迟 | 无 | 低 | 按轮询频率 |
| CFM Redis | ⚡ 实时 | Redis | 中 | ~0 |
| Webhook | ⚡ 实时 | HTTP服务 | 高 | ~0 |

---

**简单、可靠、无依赖 — 跨框架通信的第一选择！** 📬
