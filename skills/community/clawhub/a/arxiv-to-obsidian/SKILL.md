---
name: arxiv-to-obsidian
description: 当用户要求获取 arXiv 最新 AI 论文、整理今日论文摘要、生成 AI 论文日报、把 arXiv 论文写入 Obsidian、同步文献到今日日记时，使用此 skill。默认来源是 `https://export.arxiv.org/rss/cs.AI`，默认目标是 Obsidian 中的 `402论文资料` 下的今日笔记。
---

# arxiv-to-obsidian

把 arXiv `cs.AI` RSS 中最新发布的 10 篇论文翻译成中文，并追加到 Obsidian 的今日笔记。

## Scope

严格按下面的任务执行：

1. 从 `https://export.arxiv.org/rss/cs.AI` 获取 RSS。
2. 解析每篇论文的 `title`、`abstract`、`link`、`published date`。
3. 按发布时间倒序排序，只保留最新 10 篇。
4. 把 `title` 和 `abstract` 翻译成简体中文。
5. 生成 Markdown 表格，摘要不得截断。
6. 使用 Obsidian CLI 路径写入，不要直接操作文件系统。

## Obsidian Rule

如果宿主环境提供专门的 `obsidian-cli` skill，优先调用那个 skill。
如果宿主环境没有该 skill，就直接调用 `obsidian` 命令。
无论哪种情况，都禁止直接读写 vault 文件系统路径。

## Target Note Convention

为避免“今日日记”和“402论文资料”之间的歧义，默认把目标笔记解释为：

`402论文资料/YYYY-MM-DD.md`

只有在用户明确给出其他笔记路径时，才覆盖这个默认路径。

## Required Write Flow

1. 先确认 `obsidian` CLI 可用，且目标 vault 存在。
2. 先检查 `402论文资料` 是否存在。
3. 如果文件夹不存在，只能通过 Obsidian CLI 创建引导文件再删除的方式来创建文件夹；不要直接在文件系统里建目录。
4. 如果今日笔记已存在，使用 append 在文末追加内容。
5. 如果今日笔记不存在，使用 create 新建笔记，并把整段内容作为初始正文。

## Table Format

输出表格必须使用这个表头：

```markdown
| 标题（中文） | 摘要（中文） | 原文链接 | 发布日期 |
| ------ | ------ | ---- | ---- |
```

每篇论文一行，摘要不得截断，原文链接保留原始 URL。

## Append Block

追加到笔记末尾的内容必须是：

```markdown
## 今日AI论文

| 标题（中文） | 摘要（中文） | 原文链接 | 发布日期 |
| ------ | ------ | ---- | ---- |
| ... | ... | ... | ... |
```

## Failure Handling

1. 如果 RSS 获取失败，停止并报告失败原因，不要写入空内容。
2. 如果翻译失败，停止并报告失败原因，不要写入半成品。
3. 如果 Obsidian CLI 不可用、vault 不存在、append/create 失败，停止并报告具体失败步骤。
4. 不要在失败时直接改写本地 markdown 文件兜底。

## Helpful Local Tools

如果需要更稳定地解析 RSS 或批量翻译，可以使用：

- `scripts/parser.py`
- `scripts/translator.py`
- `scripts/fetch-arxiv.sh`

这些脚本也必须通过 Obsidian CLI 完成写入，不得直接写 vault 文件。
