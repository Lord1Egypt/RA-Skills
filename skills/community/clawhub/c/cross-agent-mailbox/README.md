# 📬 Cross-Agent Mailbox - 文件信箱通信

跨框架AI Agent通信的最简单方案。适用于任何框架之间的通信（Hermes、OpenClaw、Claude等）。

## 核心理念

两个Agent共享一个文件目录，通过写信/读信方式通信。简单、可靠、无依赖。

## 快速开始

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

## 适用场景

- ✅ 跨框架通信（Hermes ↔ OpenClaw）
- ✅ 简单可靠的通信需求
- ✅ 不需要实时性的场景
- ✅ 无额外依赖要求

## 不适用场景

- ❌ 需要实时通信（用 CFM Redis）
- ❌ 高频消息（>10条/分钟）
- ❌ 需要消息持久化和查询

## 与CFM Redis对比

| 特性 | 文件信箱 | CFM Redis |
|------|----------|-----------|
| 实时性 | 🐢 延迟 | ⚡ < 10ms |
| 依赖 | 无 | Redis |
| 复杂度 | 低 | 中 |
| Token消耗 | 按轮询频率 | 通信零token |

## 许可证

MIT License

---

**简单、可靠、无依赖 — 跨框架通信的第一选择！** 📬
