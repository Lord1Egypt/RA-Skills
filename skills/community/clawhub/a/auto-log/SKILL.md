# Auto Log Skill

**Auto Log Skill** — Automatically records AI agent activity to daily memory log files.

📖 [中文文档](README.zh-CN.md)

---

## 🎯 Features

- ✅ Auto-create daily log templates
- ✅ Append important events to the log
- ✅ Record task execution status
- ✅ Add and manage todo items
- ✅ Quickly retrieve today's log summary

---

## 📦 Installation

```bash
clawhub install auto-log
```

---

## 🔧 Configuration

Copy the config template and fill in your values:

```bash
cp config.example.json config.json
```

**Required fields:**
- `memory_dir`: Directory to store log files

---

## 🚀 Usage

```python
from auto_log_skill import log_event, log_task, add_todo

# Log an event
log_event("Skill packaging complete")

# Log a task
log_task("RAG memory retrieval", "✅", "Success")

# Add a todo
add_todo("Team sync at 3 PM")

# Get summary
print(get_today_summary())
```

---

## 🛠️ Required Tools

- `file_read`: Read log files
- `file_write`: Write log content

---

## 📝 Changelog

### v1.0.0 (2026-03-17)
- ✅ Initial release
- ✅ Auto daily log creation
- ✅ Event / task / todo recording
- ✅ Summary generation

---

## 🤝 Contributing

GitHub: https://github.com/openclaw/skills

---

## 📄 License

MIT License

---

**Author**: socneo  
**Last updated**: 2026-03-18
