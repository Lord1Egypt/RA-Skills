# Flash Thoughts 💡

> 随手记录灵感闪念，像备忘录一样简单，像日记一样有序。

**[English Version](#-english)**

---

## 这是什么？

**Flash Thoughts（闪念）** 是一个 OpenClaw 智能体技能，帮助你：

- ⚡ **快速捕捉** 转瞬即逝的想法
- 📅 **按日期存储** 每天一个文件，方便回顾
- 🔍 **简单搜索** 文本格式，grep 即可查找
- 🤖 **智能体对话** 说话就能记录，无需打开 App

## 适用场景

- 💡 突然想到一个好点子
- 📝 需要记下来但不想打断当前工作
- 📚 积累写作素材
- 🗂️ 个人知识管理

## 安装

### 方法一：手动安装

```bash
# 克隆仓库
git clone https://github.com/bosichong/flash-thoughts.git

# 复制到 OpenClaw 技能目录
cp -r flash-thoughts ~/.openclaw/workspace/skills/
```

### 方法二：使用 SkillHub/ClawHub

```bash
skillhub install flash-thoughts
```

## 使用示例

**添加闪念**：
```
用户：帮我记下来，我想为每种博客程序写一个智能体技能
智能体：记好了！📝 写入了 2026-03-20.md
```

**搜索闪念**：
```
用户：帮我找找之前关于博客的想法
智能体：找到了，3月20日的闪念：
> 博客程序智能体技能 - 为各种博客程序写智能体技能...
```

## 命令

```bash
# 添加闪念
python3 scripts/flash.py add "你的想法内容"

# 搜索关键词
python3 scripts/flash.py search "关键词"

# 显示某天的闪念
python3 scripts/flash.py show 2026-03-20

# 显示最近N天的闪念文件
python3 scripts/flash.py recent 7
```

## 文件结构

```
~/biji/闪念/
├── 2026-03-20.md
├── 2026-03-21.md
└── ...
```

每个文件：
```markdown
# 2026-03-20 闪念

---

## 10:19 - 博客程序智能体技能

想法内容...

---

## 14:32 - 另一个想法

另一个想法内容...
```

## 配置

通过环境变量自定义存储路径：

```bash
export FLASH_THOUGHTS_DIR="~/my/custom/path"
```

或直接修改 `scripts/flash.py` 中的 `FLASH_DIR` 变量。

## 依赖

- Python 3.6+
- 无外部依赖 ✨

## 为什么选择 Flash Thoughts？

| 特性 | Flash Thoughts | 备忘录 App | 笔记软件 |
|------|---------------|-----------|---------|
| 记录速度 | ⚡ 对话即记录 | 📱 打开 App | 📱 打开软件 |
| 数据所有权 | ✅ 纯文本，本地 | ❌ 云端/封闭 | ⚠️ 视情况 |
| 搜索便利 | ✅ grep/搜索 | ⚠️ 应用内 | ⚠️ 应用内 |
| 结构化 | ✅ 日期+分隔 | ❌ 扁平列表 | ⚠️ 需手动 |

## License

[MIT License](LICENSE)

---

## 🇬🇧 English

> Capture fleeting ideas instantly. Simple as a memo, organized as a journal.

**[中文版本](#flash-thoughts-)**
**[View on GitHub](https://github.com/bosichong/flash-thoughts)**

---

## What is this?

**Flash Thoughts** is an OpenClaw agent skill that helps you:

- ⚡ **Quick capture** fleeting ideas
- 📅 **Daily files** one file per day, easy to review
- 🔍 **Simple search** plain text, grep-friendly
- 🤖 **Chat to record** just speak to your agent

## Installation

### Method 1: Manual

```bash
# Clone the repo
git clone https://github.com/bosichong/flash-thoughts.git

# Copy to OpenClaw skills directory
cp -r flash-thoughts ~/.openclaw/workspace/skills/
```

### Method 2: SkillHub/ClawHub

```bash
skillhub install flash-thoughts
```

## Usage

**Add a flash thought**:
```
You: 帮我记下来，我想为每种博客程序写一个智能体技能
Agent: 记好了！📝 写入了 2026-03-20.md
```

**Search flash thoughts**:
```
You: 帮我找找之前关于博客的想法
Agent: Found in March 20:
> 博客程序智能体技能 - 为各种博客程序写智能体技能...
```

## Commands

```bash
# Add a thought
python3 scripts/flash.py add "Your idea content"

# Search by keyword
python3 scripts/flash.py search "keyword"

# Show a specific day
python3 scripts/flash.py show 2026-03-20

# List recent days
python3 scripts/flash.py recent 7
```

## File Structure

```
~/biji/闪念/
├── 2026-03-20.md
├── 2026-03-21.md
└── ...
```

Each file:
```markdown
# 2026-03-20 闪念

---

## 10:19 - Blog Agent Skills

Idea content...

---

## 14:32 - Another idea

Another idea...
```

## Configuration

Customize storage path via environment variable:

```bash
export FLASH_THOUGHTS_DIR="~/my/custom/path"
```

Or edit `FLASH_DIR` in `scripts/flash.py`.

## Dependencies

- Python 3.6+
- No external dependencies ✨

## Why Flash Thoughts?

| Feature | Flash Thoughts | Notes App | Note-taking Software |
|---------|---------------|-----------|---------------------|
| Speed | ⚡ Chat to record | 📱 Open app | 📱 Open software |
| Data ownership | ✅ Plain text, local | ❌ Cloud/proprietary | ⚠️ Varies |
| Search | ✅ grep/search | ⚠️ In-app only | ⚠️ In-app only |
| Structure | ✅ Date + dividers | ❌ Flat list | ⚠️ Manual setup |

## License

[MIT License](LICENSE)

---

## Contributing

Issues and Pull Requests are welcome!

## Author

Created by [Bosi Chong](https://github.com/bosichong)

---

If you find this useful, please consider giving it a ⭐!