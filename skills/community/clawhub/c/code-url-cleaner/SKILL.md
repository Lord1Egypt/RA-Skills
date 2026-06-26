# Code URL Cleaner Skill | 代码 URL 清理器技能

## Description | 描述

**English:** Automatically clean extra spaces in code and URLs, preserving necessary spaces (text, indentation). **Hook auto-registers on skill load - no manual activation needed!**

**中文:** 自动清理代码和 URL 中的多余空格，保留必要的空格（文本、缩进）。**Hook 在技能加载时自动注册 - 无需手动激活！**

---

## ✅ Auto-Activation | 自动激活

**English:** The hook automatically registers when the skill is loaded by OpenClaw. **No manual commands needed!**

**中文:** Hook 在技能被 OpenClaw 加载时自动注册。**无需手动命令！**

### How It Works | 工作原理

**English:** When you install this skill, the hook automatically activates in your OpenClaw session. All agent output is cleaned immediately.

**中文:** 安装此技能后，Hook 在 OpenClaw 会话中自动激活。所有 agent 输出立即被清理。

### Optional: Manual Activation | 可选：手动激活

**English:** If auto-activation fails, you can manually activate:

**中文:** 如果自动激活失败，可以手动激活：

```bash
python3 -c "from cleaner import register_auto_hook; register_auto_hook()"
```

---

## Problem | 问题

**English:** When generating code and URLs, extra spaces are often inserted in wrong positions, causing execution failures.

**中文:** 在生成代码和 URL 时，经常会在错误的位置插入多余空格，导致执行失败。

**Examples | 示例:**

```
❌ https://github.com/Johnserf-Seed /TikTokDownload.git
✅ https://github.com/Johnserf-Seed/TikTokDownload.git

❌ cd /tmp && git clone https://github.com/Johnserf-Seed /TikTokDownload.git
✅ cd /tmp && git clone https://github.com/Johnserf-Seed/TikTokDownload.git

❌ pip3 install -r requirements.txt  --break-system-packages
✅ pip3 install -r requirements.txt --break-system-packages
```

---

## Installation | 安装

```bash
npx clawhub@latest install code-url-cleaner
```

### That's It! | 就这样！

**English:** No further setup needed. The hook activates automatically.

**中文:** 无需进一步配置。Hook 自动激活。

---

## Usage | 使用方法

### Auto Mode (Default) | 自动模式（默认）

**English:** Once installed, all agent output is automatically cleaned. No manual calls needed.

**中文:** 安装后，所有 agent 输出自动清理，无需手动调用。

```python
# Agent output is automatically cleaned | Agent 输出自动清理
print("https://github.com/Johnserf-Seed /TikTokDownload.git")
# Output: https://github.com/Johnserf-Seed/TikTokDownload.git
```

### Manual Mode | 手动模式

```python
from cleaner import clean_text

text = "https://github.com/Johnserf-Seed /TikTokDownload.git"
cleaned = clean_text(text)
print(cleaned)
# Output: https://github.com/Johnserf-Seed/TikTokDownload.git
```

---

## Hook Implementation | Hook 实现

### How It Works | 工作原理

**English:** The skill registers an OpenClaw lifecycle hook that intercepts agent output and cleans it before display. **This happens automatically on skill load.**

**中文:** 技能注册一个 OpenClaw 生命周期钩子，拦截 agent 输出并在显示前清理。**这在技能加载时自动发生。**

### Code | 代码

```python
# cleaner.py - Auto-executed on import | 导入时自动执行
def _auto_register_hook():
    from openclaw import get_current_agent
    agent = get_current_agent()
    
    def clean_output(event, ctx):
        output = event.get('output', '')
        return {'output': clean_text(output)}
    
    agent.on('before_output', clean_output)
    return True

# Auto-register on module load | 模块加载时自动注册
_auto_register_hook()
```

---

## Rules | 规则

### Cleaned | 清理的

1. **URL Internal Spaces** | URL 内部的空格
2. **Multiple Consecutive Spaces in Commands** | 命令中的多个连续空格
3. **Path Spaces** | 路径中的空格

### Preserved | 保留的

1. **Natural Language Text** | 自然语言文本
2. **Single Space Between Arguments** | 命令参数之间的单个空格
3. **Code Indentation** | 代码缩进

---

## Testing | 测试

```bash
cd /path/to/code-url-cleaner
python3 cleaner.py --test
```

**Expected Output | 期望输出:**

```
============================================================
Code/URL Space Cleaner 测试
============================================================

✅ URL 中间有空格
✅ 命令多个空格
✅ 路径空格

============================================================
测试结果：4 通过，0 失败
============================================================

============================================================
Hook 功能测试
============================================================
Hook 状态：✅ 已激活（自动）
============================================================
```

---

## Files | 文件

| File | 文件 | Description | 描述 |
|------|------|-------------|------|
| `cleaner.py` | `cleaner.py` | Core cleaning logic + Auto-Hook | 核心清理逻辑 + 自动 Hook |
| `SKILL.md` | `SKILL.md` | This documentation | 本文档 |
| `README.md` | `README.md` | User guide | 用户指南 |
| `_meta.json` | `_meta.json` | Package metadata | 包元数据 |

---

## Version History | 版本历史

### v1.2.0 (2026-03-08)

- ✅ **Auto-hook activation** | **自动 Hook 激活**
- ✅ No manual commands needed | 无需手动命令
- ✅ Hook registers on module load | Hook 在模块加载时注册
- ✅ Backward compatible | 向后兼容

### v1.1.1 (2026-03-08)

- ✅ Fix hook activation logic | 修复 Hook 激活逻辑
- ✅ Auto-detect OpenClaw environment | 自动检测 OpenClaw 环境

### v1.1.0 (2026-03-08)

- ✅ Auto-hook feature | 自动 Hook 功能
- ✅ Hook activation command | Hook 激活命令
- ✅ Hook status check | Hook 状态检查
- ✅ Bilingual documentation | 双语文档

### v1.0.0 (2026-03-08)

- ✅ Initial release | 初始发布
- ✅ URL space cleaning | URL 空格清理
- ✅ Command space cleaning | 命令空格清理
- ✅ Path space cleaning | 路径空格清理
- ✅ 100% test coverage | 100% 测试覆盖

---

## Requirements | 依赖

- Python 3.6+ 
- OpenClaw 0.1.6+
- No external dependencies | 无外部依赖

---

## License | 许可证

MIT License | MIT 许可证

---

## Author | 作者

OpenClaw Community | OpenClaw 社区

---

## Links | 链接

- **GitHub:** https://github.com/ra1nzzz/code-url-cleaner
- **ClawHub:** https://clawhub.ai/skills/code-url-cleaner
- **Issues:** https://github.com/ra1nzzz/code-url-cleaner/issues
