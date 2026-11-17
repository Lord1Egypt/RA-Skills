# 命名规则（文件编号 = 章编号）

**核心规则：所有章节文件名使用全局连续三位数编号，不随卷重置。**

| 卷 | 章节范围 | 文件名 |
|----|---------|--------|
| 卷 1 | 第 1-30 章 | `chapter-001.md` ~ `chapter-030.md` |
| 卷 2 | 第 31-60 章 | `chapter-031.md` ~ `chapter-060.md` |
| 卷 3 | 第 61-100 章 | `chapter-061.md` ~ `chapter-100.md` |
| … | … | … |
| 卷 N | 最后一卷 | `chapter-XXX.md` |

**关键规则：**
- ❌ **禁止**每卷内从第 1 章重新开始编号（不要出现卷 1 有 1-30 章、卷 2 也有 1-30 章的情况）
- ✅ **文件名 = 章编号 = 全局连续三位数**：`chapter-001.md`（第 1 章）、`chapter-300.md`（第 300 章）
- ✅ 三位数补零：`chapter-001.md`、`chapter-030.md`、`chapter-300.md`
- ✅ 卷 1 第 1 章 = `chapter-001.md`，卷 2 第 1 章 = `chapter-031.md`（假设卷 1 有 30 章）

**目录内文件命名：**

| 文件 | 命名 |
|------|------|
| 总纲 | `03-outline/00-master-outline.md` |
| 卷级大纲 | `03-outline/vol-{N}-outline.md` |
| 章级蓝本 | `03-outline/vol-{N}/chapter-{XX}-blueprint.md` |
| 章节正文 | `04-chapters/vol-{N}/chapter-{XX}.md` |
| 卷校验报告 | `06-validation/vol-{N}-validation-report.md` |
| 全书校验报告 | `06-validation/full-book-validation-report.md` |
| 人物卡 | `references/characters/角色名.md` |
| 人物关系 | `references/character-relationships.md` |
| 存档目录 | `[小说标题]_v0/`、`[小说标题]_v1/`、`[小说标题]_v2/`…（按创建顺序递增，只读） |

> 为什么全局连续：打开 `04-chapters/` 文件夹，文件名直接告诉你写到第几章，跨卷也能一眼定位。"每卷从 1 开始"是长篇写作最常见的迷路源。
