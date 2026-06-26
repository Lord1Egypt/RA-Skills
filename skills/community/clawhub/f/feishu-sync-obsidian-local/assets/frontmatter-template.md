# frontmatter 模板（Generator）

> 本文件已废弃。frontmatter 规范已迁移至 vault/SYNC-RULES.md。
> 保留仅作参考。

---

## 当前使用的模板

```yaml
---
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: false
categories: []
tags: [来源/飞书同步]
feishu_doc_token: xxx
feishu_wiki: xxx
feishu_node_token: xxx
---
```

---

## 说明

- **基础字段**（Hugo FixIt）：`date`、`lastmod`、`draft`、`categories`、`tags`
- **飞书扩展字段**（无条件追加）：`feishu_doc_token`、`feishu_wiki`、`feishu_node_token`
- 如果 vault 已有其他 frontmatter 规范，优先使用已有规范，飞书字段追加
