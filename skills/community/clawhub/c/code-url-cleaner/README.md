# Code URL Cleaner | 代码 URL 清理器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 4/4](https://img.shields.io/badge/tests-4/4-green.svg)](https://github.com/ra1nzzz/code-url-cleaner)
[![Version: 1.2.0](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://clawhub.ai/skills/code-url-cleaner)

Automatically clean extra spaces in code and URLs. **Auto-activates on install!**
自动清理代码和 URL 中的多余空格。**安装后自动激活！**

---

## ✅ Auto-Activation | 自动激活

**English:** The hook automatically registers when the skill is loaded by OpenClaw. **No manual commands needed!**

**中文:** Hook 在技能被 OpenClaw 加载时自动注册。**无需手动命令！**

### Quick Start | 快速开始

```bash
# Step 1: Install | 安装
npx clawhub@latest install code-url-cleaner

# Step 2: Done! | 完成！
# Hook is automatically activated | Hook 自动激活
```

**That's it! All agent output is now auto-cleaned!**
**就这样！所有 agent 输出现在自动清理！**

---

## 📖 Usage | 使用方法

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

# Clean URL | 清理 URL
text = clean_text("https://github.com/Johnserf-Seed /TikTokDownload.git")
# Output: https://github.com/Johnserf-Seed/TikTokDownload.git

# Clean command | 清理命令
text = clean_text("pip3 install -r requirements.txt  --break-system-packages")
# Output: pip3 install -r requirements.txt --break-system-packages

# Clean path | 清理路径
text = clean_text("cd /Users/yitao/.openclaw /workspace")
# Output: cd /Users/yitao/.openclaw/workspace
```

---

## ✨ Features | 功能

| Feature | 功能 | Before | After |
|---------|------|--------|-------|
| URL Cleaning | URL 清理 | `https://example.com/ test` | `https://example.com/test` |
| Command Cleaning | 命令清理 | `git clone  https://...` | `git clone https://...` |
| Path Cleaning | 路径清理 | `/Users/yitao/ .openclaw` | `/Users/yitao/.openclaw` |
| **Auto-Hook** | **自动 Hook** | **Manual calls** | **Automatic!** |

---

## 🧪 Testing | 测试

```bash
cd /path/to/code-url-cleaner
python3 cleaner.py --test
```

**Test Results | 测试结果:**
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

## 📝 Rules | 清理规则

### What Gets Cleaned | 清理什么

1. **URL Internal Spaces** | URL 内部的空格
   - ❌ `https://github.com/user /repo`
   - ✅ `https://github.com/user/repo`

2. **Multiple Command Spaces** | 命令中的多个空格
   - ❌ `git  clone  https://...`
   - ✅ `git clone https://...`

3. **Path Spaces** | 路径中的空格
   - ❌ `/Users/yitao/ .openclaw`
   - ✅ `/Users/yitao/.openclaw`

### What Gets Preserved | 保留什么

1. **Natural Language Text** | 自然语言文本
2. **Single Space Between Arguments** | 命令参数之间的单个空格
3. **Code Indentation** | 代码缩进

---

## 🔧 Hook Implementation | Hook 实现

### How It Works | 工作原理

**English:** The skill registers an OpenClaw lifecycle hook that intercepts agent output and cleans it before display. **This happens automatically on skill load.**

**中文:** 技能注册一个 OpenClaw 生命周期钩子，拦截 agent 输出并在显示前清理。**这在技能加载时自动发生。**

### Activation Flow | 激活流程

```
1. Install skill | 安装技能
   ↓
2. Skill loaded by OpenClaw | OpenClaw 加载技能
   ↓
3. Hook auto-registers | Hook 自动注册
   ↓
4. All output auto-cleaned | 所有输出自动清理
```

**No manual commands needed!**
**无需手动命令！**

### Code Example | 代码示例

```python
# In cleaner.py - Auto-executed on import | 导入时自动执行
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

## 📦 Files | 文件结构

```
code-url-cleaner/
├── cleaner.py      # Core cleaning logic + Auto-Hook | 核心清理逻辑 + 自动 Hook
├── SKILL.md        # Skill documentation | 技能文档
├── README.md       # This file | 本文件
├── _meta.json      # Package metadata | 包元数据
└── .gitignore      # Git ignore rules | Git 忽略规则
```

---

## 🎯 Use Cases | 使用场景

1. **AI Agent Output** | AI Agent 输出
   - ✅ Auto-clean code snippets | 自动清理代码片段
   - ✅ Auto-clean URLs in responses | 自动清理回复中的 URL
   - ✅ Auto-clean shell commands | 自动清理 shell 命令

2. **Script Generation** | 脚本生成
   - ✅ Clean generated commands | 清理生成的命令
   - ✅ Clean file paths | 清理文件路径

3. **Documentation** | 文档生成
   - ✅ Clean markdown code blocks | 清理 markdown 代码块
   - ✅ Clean inline code | 清理内联代码

---

## 📄 License | 许可证

MIT License - See LICENSE file for details.
MIT 许可证 - 详见 LICENSE 文件。

---

## 🤝 Contributing | 贡献

1. Fork the repository | Fork 仓库
2. Create a feature branch | 创建功能分支
3. Commit your changes | 提交更改
4. Push to the branch | 推送到分支
5. Open a Pull Request | 打开 Pull Request

---

## 📞 Support | 支持

- GitHub Issues: https://github.com/ra1nzzz/code-url-cleaner/issues
- ClawHub: https://clawhub.ai/skills/code-url-cleaner

---

**Version | 版本:** 1.2.0  
**Author | 作者:** OpenClaw Community  
**Created | 创建日期:** 2026-03-08  
**Updated | 更新日期:** 2026-03-08  
**Auto-Activation | 自动激活:** ✅ Yes | 是
