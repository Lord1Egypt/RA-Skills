# Springer Handbook 行文布局参考

> 本文件作为 Cookbook Generator 在生成"综述 / 手册"类内容时的补充参考。与 `style-guide-oreilly.md` 配合使用：CookBook 章节偏 Problem/Solution，综述/手册章节偏 Taxonomy/Survey/Reference。

## 1. 全景图先行（Big Picture First）

Springer Handbook 每个部分开篇必有一张"领域地图"（Taxonomy / Mind Map / Classification）：

- 把整个领域分成若干个子领域/分支。
- 每个子领域标注本书对应的章节编号。
- 用箭头表示分支之间的依赖/演化关系。

在 MDX 中这对应 `ch00-overview.mdx`。该章必须包含：

- 一张总览图（mermaid mindmap / flowchart，或 drawio 架构图）。
- 一段"阅读路线"：不同背景读者推荐的章节顺序。
- 一张"章节依赖关系表"。

## 2. 分层结构（Hierarchical Organization）

典型层次：

```
Part (部分) → Chapter (章) → Section (节) → Subsection (小节)
```

每个 Part 有一张扉页图 + 一段概述，说明这一部分解决什么问题、包含哪几章、与其他 Part 的关系。

在 MDX/_meta.ts 中用 separator 模拟 Part：

```ts
export default {
  index: "🏠 首页",
  '---sep-1': { type: 'separator', title: "Part I · 基础" },
  "ch01-xxx": "1. ...",
  "ch02-xxx": "2. ...",
  '---sep-2': { type: 'separator', title: "Part II · 进阶" },
  // ...
}
```

## 3. 每章结构（Springer Handbook 模式）

综述/手册类章节推荐结构：

1. **Introduction / Motivation**：这一子领域的定义、历史、为什么重要。
2. **Background / Preliminaries**：必要的数学/概念背景（可引用前置章节）。
3. **Taxonomy / Classification**：把该子领域的方法/技术分成几类，每类一段简述，给出分类图。
4. **Detailed Methods**：逐类深入讲解原理（公式）、算法、代表性工作。
5. **Comparison / Discussion**：横向对比表（精度、速度、适用场景、前提假设）。
6. **Applications / Case Studies**：实际应用案例。
7. **Open Challenges / Future Directions**：未解决问题、研究前沿。
8. **Conclusion** + **References**。

## 4. 表格密度

Springer Handbook 的表格用于"可查阅"的参考价值。常见表格类型：

| 表类型 | 示例 |
|---|---|
| 符号表 | 数学符号、含义、首次出现章节 |
| 缩写表 | 缩写、全称、中文译名 |
| 分类对比表 | 方法名、年份、核心思想、复杂度、适用场景、代表论文 |
| 参数配置表 | 参数、类型、默认值、推荐范围、影响 |
| API 速查表 | 函数签名、功能、参数、返回值、版本 |
| 术语中英对照表 | 中文、英文、缩写、定义 |

宽表（>5 列）必须在 MDX 中用 `<div className="overflow-x-auto">` 包裹。

## 5. 公式规范

- 行内公式用 `$...$`，块级公式用 `$$...$$`（KaTeX 兼容）。
- 每个块级公式带编号（手动加 `\tag{N.M}`）。
- 公式后必须有自然语言解释每个符号的含义（尤其是首次出现时）。
- 不要堆公式不解释。公式是工具，不是目的。

## 6. 引用规范

- 关键论断、算法、数据点必须有来源。
- 格式：行内用 `[作者 年份]` 或上角标，章末"参考文献"列出完整条目。
- 论文条目格式：`作者. 标题. 会议/期刊, 年份. DOI/URL`
- 网络资料条目格式：`作者/组织. 标题. 站点名, 日期. URL (访问日期)`
- 所有来源同步到 `metadata/sources.md`。

## 7. 索引与交叉引用

- 每个术语首次出现时加粗，并在附录"术语表"中收录。
- 跨章引用必须是可点击链接：`[见第 3 章 §3.2](./ch03-xxx.mdx#32-小节标题)`。
- 图表带编号（图 N-M、表 N-M），正文中引用"如图 N-M 所示"。
- 附录包含：
  - 附录 A：API/配置速查表
  - 附录 B：术语表
  - 附录 C：符号表（如有数学公式）
  - 附录 D：图表索引
  - 附录 E：参考文献

## 8. 与 O'Reilly 风格的取舍

| 维度 | O'Reilly CookBook | Springer Handbook |
|---|---|---|
| 主驱动 | Problem/Solution | Taxonomy/Survey |
| 代码密度 | 高 | 中（多为伪代码/算法） |
| 公式密度 | 低 | 中-高 |
| 表格密度 | 中 | 高（速查） |
| 章节引入 | "你会学到…" | "本节回顾…" |
| 适合章类型 | 实操、Recipes、API 用法 | 原理、综述、对比、参考 |
| 语气 | 对话式（第二人称） | 学术式（第三人称/被动） |

同一本书中两种风格混用：

- 基础/概念/架构/综述章 → Springer Handbook 风格
- 实操/Recipes/API/调试章 → O'Reilly CookBook 风格
- 附录/速查 → Springer Handbook 风格
