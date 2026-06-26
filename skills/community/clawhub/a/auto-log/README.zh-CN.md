# Auto Log Skill - 日志自动记录技能

> 自动为 AI 助手创建每日日志，记录事件、任务执行和待办事项。

**版本**: v1.0 | **作者**: socneo | **分类**: productivity

📖 [English README](README.md)

---

## ✨ 功能特性

- ✅ **自动创建** — 每日自动生成日志模板
- ✅ **事件记录** — 追加重要事件到日志
- ✅ **任务追踪** — 以表格形式记录任务执行状态
- ✅ **待办管理** — 添加和管理待办事项
- ✅ **摘要生成** — 快速获取今日日志概要

---

## 📦 安装

```bash
# 方式 1: 通过 ClawHub 安装（推荐）
clawhub install auto-log

# 方式 2: 手动复制
cp -r auto_log /your/workspace/
cd /your/workspace/auto_log
cp config.example.json config.json
```

---

## 🔧 配置

编辑 `config.json`:

```json
{
  "memory_dir": "~/openclaw/workspace/memory",
  "auto_save": true,
  "format": "markdown"
}
```

| 字段 | 说明 | 默认值 |
|------|------|-------|
| `memory_dir` | 日志文件存储目录 | `~/openclaw/workspace/memory` |
| `auto_save` | 每次操作自动保存 | `true` |
| `format` | 日志格式（`markdown` / `json`） | `markdown` |

---

## 🚀 使用方法

### Python API

```python
from auto_log_skill import AutoLogSkill

skill = AutoLogSkill()
skill.create_daily_log("my-agent")
skill.append_event("RAG 技能包封装完成")
skill.append_task("技能包开发", "✅", "已完成")
skill.add_todo("下午 3 点团队同步")
print(skill.get_summary())
```

### 便捷函数

```python
from auto_log_skill import log_event, log_task, add_todo, get_today_summary

log_event("飞书 API 测试通过")
log_task("轮询机制开发", "✅", "成功")
add_todo("下午 3 点开会")
print(get_today_summary())
```

### 命令行

```bash
# 创建今日日志
python auto_log_skill.py

# 记录事件
python auto_log_skill.py event "RAG 系统配置完成"

# 获取摘要
python auto_log_skill.py summary
```

---

## 📄 许可证

MIT License

---

*最后更新: 2026-03-18*
