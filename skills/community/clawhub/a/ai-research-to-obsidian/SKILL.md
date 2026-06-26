---
name: ai-research-to-obsidian
description: 用 AI 工具（豆包/Kimi/ChatGPT）搜索问题并将结果整理保存为 Obsidian 文档。触发场景：(1) 用户要求用 AI 搜索问题 (2) 用户要求浏览器搜索并保存到 Obsidian (3) 用户说"帮我查一下"并提到保存到笔记/文档/Obsidian
---

# AI 研究保存到 Obsidian

自动化工作流：浏览器 AI 搜索 → 内容整理 → Obsidian 格式保存

## 工作流程

### 1. 打开 AI 工具

根据内容类型选择：
- **通用问题** → 豆包 (https://www.doubao.com)
- **编程/技术** → Kimi (https://kimi.moonshot.cn)
- **英文/综合** → ChatGPT (https://chat.openai.com)

```bash
browser action=open target=host url="https://www.doubao.com"
```

### 2. 输入搜索内容

在输入框输入用户的问题，点击发送。

### 3. 等待回复

快照获取回复内容。如果内容较长，向下滚动获取完整信息。

### 4. 整理为 Obsidian 格式

创建 Markdown 文件，包含：
- YAML frontmatter（date, tags）
- 标题（标注日期）
- 格式化内容（表格、列表、层级结构）
- 来源标注

### 5. 保存到 Obsidian Vault

查找 Obsidian 路径：
```bash
mdfind "kMDItemFSName == 'Obsidian'"  # 查找本地库
ls ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/  # iCloud 库
```

移动文件：
```bash
mv <源文件> <Obsidian路径>/
```

## Obsidian 文档模板

```markdown
---
date: {{DATE}}
tags: [{{TAGS}}]
---

# {{TITLE}} | {{DATE}}

> 来源：{{AI_SOURCE}}

## 核心要点

- 要点1
- 要点2

## 详细内容

### 模块1

内容...

---

*文档生成日期：{{DATE}}*
```

## 注意事项

- 优先使用豆包（中文理解最好）
- 内容过长时分多次获取
- 保持 Obsidian 格式规范（frontmatter、层级标题）
- 询问用户 Vault 路径（如果不确定）
