# Auto Log Skill

> Automatically records AI agent activity to structured daily log files.

**Version**: v1.0 | **Author**: socneo | **Category**: productivity

📖 [中文文档 README.zh-CN.md](README.zh-CN.md)

---

## ✨ Features

- ✅ **Auto-create** — generates a daily log template automatically
- ✅ **Event logging** — appends important events to the log
- ✅ **Task tracking** — records task execution status in a table
- ✅ **Todo management** — add and manage todo items
- ✅ **Summary** — quickly retrieve today's log digest

---

## 📦 Installation

```bash
# Option 1: Install via ClawHub (recommended)
clawhub install auto-log

# Option 2: Copy manually
cp -r auto_log /your/workspace/
cd /your/workspace/auto_log
cp config.example.json config.json
```

---

## 🔧 Configuration

Edit `config.json`:

```json
{
  "memory_dir": "~/openclaw/workspace/memory",
  "auto_save": true,
  "format": "markdown"
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `memory_dir` | Directory to store log files | `~/openclaw/workspace/memory` |
| `auto_save` | Auto-save on each operation | `true` |
| `format` | Log format (`markdown` / `json`) | `markdown` |

---

## 🚀 Usage

### Python API

```python
from auto_log_skill import AutoLogSkill

# Initialize
skill = AutoLogSkill()

# Create today's log
log_path = skill.create_daily_log("my-agent")

# Log an event
skill.append_event("RAG skill packaging complete", section="Events")

# Log a task
skill.append_task("Skill development", "✅", "Done")

# Add a todo
skill.add_todo("Run integration tests")

# Get summary
print(skill.get_summary())
```

### Convenience functions

```python
from auto_log_skill import log_event, log_task, add_todo, get_today_summary

log_event("Feishu API test passed")
log_task("Polling mechanism", "✅", "Success")
add_todo("Team sync at 3 PM")
print(get_today_summary())
```

### CLI

```bash
# Create today's log
python auto_log_skill.py

# Log an event
python auto_log_skill.py event "RAG system configured"

# Get summary
python auto_log_skill.py summary
```

---

## 📄 Log Format Example

```markdown
# my-agent Daily Log — 2026-03-17

## 📅 Basic Info
- Date: 2026-03-17
- Timezone: UTC+8
- Agent: my-agent

## 🎯 Events
- 10:00 RAG skill packaging complete
- 14:30 Feishu API test passed

## ✅ Tasks
| Task | Status | Result |
|------|--------|--------|
| Skill development | ✅ | Done |
| Polling test | ✅ | 17 rounds successful |

## 📝 Todos
- [ ] Run integration tests
- [ ] Team sync at 3 PM
```

---

## 🛠️ Dependencies

All standard library — no pip install required.

| Module | Purpose |
|--------|---------|
| `pathlib` | File path handling |
| `json` | Config parsing |
| `datetime` | Timestamp generation |

---

## 📝 Changelog

### v1.0.0 (2026-03-17)
- ✅ Initial release
- ✅ Auto daily log creation
- ✅ Event / task / todo recording
- ✅ Summary generation

---

## 🤝 Contributing

Issues and Pull Requests welcome!

GitHub: https://github.com/openclaw/skills

---

## 📄 License

MIT License

---

*Last updated: 2026-03-18*
