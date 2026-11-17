---
type: reference
audience: skill-self
---

# Obsidian 适配说明

> 本文档在用户使用 Obsidian、或询问 Quill 如何与 Obsidian 协作时加载。

## Frontmatter 兼容

Quill 所有文件使用标准 YAML frontmatter，键名为英文标识符（`type`、`status`、`created`、`updated`、`description`、`title`、`slug`、`date`、`tags`、`series`、`word-count`）。`date` 是文章发布日/项目日期；`created`/`updated` 是笔记创建与最后修改时间（Obsidian 核心属性）。
Dataview / Bases 插件可直接读取这些字段做查询。建议在 Obsidian 设置中启用"属性"视图，可视化编辑元数据。

## 链接规范

- 文章内部文件互链：`[[claim]]`、`[[evidence]]`、`[[audience]]`、`[[style]]`、`[[ai-draft]]`、`[[_index]]`（同目录短名即可）
- 与 Vault 内其他笔记关联：`[[笔记标题]]`
- 精确到标题 / 段落：`[[笔记#标题]]`、`[[笔记^block-id]]`
- 外部链接：`[文字](url)`

## Dataview 查询示例

在任意 MOC 或 `_index.md` 中粘贴，自动汇总 `40-Writing/` 下所有文章状态：

```dataview
TABLE status, word-count, series
FROM "40-Writing"
WHERE type = "index"
SORT date DESC
```

## 与写作插件的共存

Quill 用 `_index.md`（`_` 前缀保证在文件夹中排在最顶部）作为文章入口，不使用 `_project.json`，因此不与 Obsidian 社区写作插件冲突。

## Agent Client 协作

Obsidian 的 Agent Client 插件通过 ACP 协议连接本地 AI Agent。
Quill 作为标准 Skill 安装在 Agent 的 skills 目录后，可在 Agent Client 中直接被调用——用户在 Obsidian 里说"帮我建一篇关于 X 的文章"，Agent 即触发 Quill 的创建流程（由模型直接写文件，不跑脚本）。


