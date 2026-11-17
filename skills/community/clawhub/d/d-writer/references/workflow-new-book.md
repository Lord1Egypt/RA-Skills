# 模式 A：创建新书

## 触发时机

一句灵感 / 书名 / 题材，或要求写一本新小说。

## 步骤

1. **确定项目根目录与书 id**：默认使用 `books/<slug>/`，除非用户给出不同路径。避免覆盖已有书籍目录。
2. **创建目录结构**：按 `references/templates.md` 创建。
3. **写 `book.json`**：书名、语言、题材、状态 `outlining`、目标章数、目标单章字数、`schemaVersion`、`skillVersion`、时间戳。
4. **根据用户灵感写 `author_intent.md`**：保留用户的任何确切要求，包含不可妥协项。
5. **写 `story_frame.md` 为有密度的散文**，而非干清单：
   - 主题与基调
   - 前台故事 / 背景故事
   - 核心冲突与对手
   - 世界法则与感官质地
   - 具体的终局目标（须可外部验证，不能只是"变得更强"或"复仇"）
6. **写 `volume_map.md`**：
   - 弧线 / 卷结构与情感曲线
   - 钩子种子 / 回报承诺图
   - 按目标篇幅安排章节节拍或弧线节拍
   - 节奏原则
7. **为每个重要角色写一份角色档案**：写稳定属性（功能、欲望、恐惧、秘密、言行指纹、长期弧线），并在「物理数据时间线」「逻辑数据时间线」写入**出场基线行**（出场章、各物理维度当前值、体型/外貌快照、各逻辑维度当前值）。**两套时间线的列名分别与 `book_rules.md`「物理数据维度」「逻辑数据维度」声明完全一致**——不声明的列（如仙侠题材的三围）不要出现在表格里。易漂移的"当前状态"归入 `current_state.md`。**落盘前自查**：角色卡的「canon 数字锚点」表与卡内散文区、数据时间线中出现的硬数字（年龄 / 日期 / 尺寸 / 数量）一致，不允许"卡内散文说 A、锚点表说 B"。
8. **写 `book_rules.md` / `pending_hooks.md` / `current_state.md`**，以及一张空的 `chapter_summaries.md`。
9. **写 `style_guide.md`**：语言风格、高疲劳词清单、体裁爽点类型、视角约定、章首承接与章末断章约定（速查见 templates.md，技法库见 `references/chapter-craft.md`）。
10. **保存 `story/snapshots/0000/` 作为第 0 章快照**（含 `manifest.json`）。
11. **注入仪表盘**：把 `assets/dashboard.html` 复制到书文件夹（仅此一次，之后不再重写）。
12. 若用户要求立刻写正文，以模式 B 推进第一章。

## 相关文档

- 文件职责与兼容命名：`references/file-contract.md`
- 全部基础文件模板：`references/templates.md`
- 双层质量门禁：`references/audit-dimensions.md`
