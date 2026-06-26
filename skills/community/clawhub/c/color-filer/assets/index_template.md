---
tags: [index, folder-structure]
created: 自动生成
---

# 📂 目录索引

> 本页由 `folder-organizer` 技能自动生成，展示目录结构概览。
> 最后更新时间：{{date}}

---

## 📊 统计摘要

| 项目 | 数值 |
|------|--------|
| 总文件数 | {{total_files}} |
| 总目录数 | {{total_dirs}} |
| 最大深度 | {{max_depth}} 层 |

---

## 📋 文件类型分布

{{#each file_types}}
### {{type}}

| 序号 | 文件名 | 大小 |
|------|--------|------|
{{#each files}}
| {{@index}} | [[{{name}}]] | {{size}} |
{{/each}}
{{/each}}

---

## 💡 整理建议

{{#if has_issues}}
### ⚠️ 发现的问题

{{#each issues}}
- {{issue}}
{{/each}}

### 优化建议

{{#each suggestions}}
1. {{suggestion}}
{{/each}}
{{/if}}

---

## 🗂️ 目录结构树

```
{{tree_structure}}
```

---

*此索引由 `folder-organizer` 技能自动维护*
