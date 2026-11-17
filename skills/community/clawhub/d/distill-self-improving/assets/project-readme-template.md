# <project-name>

- path: <exact-root-path>
- directory_type: <code-project|document-collection|mixed-general>
- classification_evidence: <user-statement-and-observed-evidence>
- handling_strategy: <finite-code-navigation|recursive-document-processing|mixed-boundaries|all-files-root-audit>
- version_control: <git|other|none|unknown>
- origin: <git-origin-or-empty>
- role: <verified-role-or-unknown>
- key_entries: <semicolon-separated-exact-paths>
- distillation_collections: <semicolon-separated-collection-slugs>
- collection_boundaries: <non-overlapping-boundaries-or-empty>
- last_verified: <YYYY-MM-DD>

## 职责证据

- <来自当前原文件或现场的证据；未知则写 unknown，不猜>

## 关键子目录与入口

- <exact-path> — <purpose>

## Collection 归属

- 普通代码项目的高价值文档由唯一 `<project-slug>-docs` collection 持有。
- mixed 普通模式按互不重叠的文档子树分别持有；全文件模式由根 collection 唯一持有，子树只作 group。
- project inventory 只导航关键入口和 collection，不拥有单文件结果。

## 现场复核

- 路径、origin、职责和入口均按 `last_verified` 时点记录；使用前回查当前原文件与现场。
