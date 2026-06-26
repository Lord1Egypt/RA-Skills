---
name: flash-thoughts
description: 随手记录灵感闪念。按日期存储，分隔线分隔每个想法，支持快速添加和搜索。适用于捕捉转瞬即逝的想法、灵感碎片、待办念头。/ Capture fleeting ideas instantly. Daily files, divider-separated entries, quick add and search. Perfect for fleeting thoughts, inspiration fragments, and spontaneous ideas.
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":[]},"install":[]}}
---

# Flash Thoughts - 闪念记录

随手捕捉灵感闪念，像备忘录一样简单，像日记一样有序。

## 核心理念

**闪念** = 转瞬即逝的想法 + 快速捕捉 + 简单结构

- 📅 按日期存储：每天一个文件，文件名就是日期
- 📝 分隔线分隔：每个闪念独立，互不干扰
- 🔍 方便搜索：文本格式，grep/搜索即可
- ⚡ 极简操作：说话 → 记录，不需要复杂步骤

## 使用方法

### 添加闪念

```bash
python3 scripts/flash.py add "你的想法内容"
```

智能体会自动：
1. 创建或打开今天的闪念文件
2. 添加时间戳和内容
3. 用分隔线与之前的闪念分开

### 搜索闪念

```bash
# 搜索关键词
python3 scripts/flash.py search "关键词"

# 查看某天的闪念
python3 scripts/flash.py show 2026-03-20

# 查看最近N天的闪念
python3 scripts/flash.py recent 7
```

### 配置存储路径

默认存储在 `~/notes/flash/`，可在脚本中修改 `FLASH_DIR` 变量。

## 文件结构

```
~/notes/flash/
├── 2026-03-20.md
├── 2026-03-21.md
└── ...
```

每个文件格式：
```markdown
# 2026-03-20 闪念

---

## 10:19 - 博客程序智能体技能

为各种博客程序写智能体技能...

---

## 14:32 - 闪念功能本身就是一个好想法

这个记录方式值得写成文章。
```

## 触发场景

智能体识别以下意图时自动调用：

- "帮我记下来..." / "记一个想法..."
- "我有个灵感..." / "突然想到..."
- "记到闪念里..."
- "帮我找找..." + 关键词（搜索模式）

## 依赖

- Python 3.6+
- 无外部依赖

## 为什么需要这个技能？

- 💡 灵感转瞬即逝，记录要快
- 📱 不需要打开专门的 App
- 🔗 与智能体对话即可完成记录
- 📂 文本文件，永远属于你

## 安装

```bash
# Clone 或下载到你的技能目录
git clone https://github.com/bosichong/flash-thoughts.git

# 在 OpenClaw 中，复制到技能目录
cp -r flash-thoughts ~/.openclaw/workspace/skills/
```

## 示例

**用户**：帮我记下来，我想给每种博客程序写一个智能体技能

**智能体**：记好了！📝 写入了 `2026-03-20.md`

**用户**：帮我找找之前关于博客的想法

**智能体**：找到了，3月20日的闪念：
> 博客程序智能体技能 - 为各种博客程序写智能体技能...