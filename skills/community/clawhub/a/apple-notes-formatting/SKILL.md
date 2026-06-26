---
name: "apple-notes-formatting"
description: "Use when the user wants to beautify, restructure, or rewrite content into an Apple Notes-friendly note, especially article summaries, knowledge cards, topic research notes, study notes, or long Chinese notes that need clear Title/Heading/Subheading/Body hierarchy, restrained bolding, semantic highlight colors, and deliberate use of lists, tables, quotes, code style, and note links."
---

# Apple Notes Formatting

用于把原始材料、草稿或已有笔记，整理成适合 Apple Notes 长期保存、检索、折叠和复用的格式。

## 何时使用

- 用户要“改成 Apple Notes 风格”“整理成备忘录格式”“做一版更适合 Apple Notes 的笔记”
- 用户想把文章总结、知识卡片、主题研究、课程笔记、会议笔记或零散草稿重排成更清楚的结构
- 用户明确询问 `Title` / `Heading` / `Subheading` / `Body`、加粗、高亮、列表、表格、引用、等宽文本、链接该怎么用
- 用户希望输出“可直接粘贴进 Apple Notes”的笔记草稿，或先要一版带样式标注的排版方案

如果用户没有提供内容材料，就先请对方给出原文、草稿、链接、截图转写内容，或至少说明笔记主题与用途。

## 默认工作流

1. 先判断笔记类型：
   - 单篇文章总结
   - 长期知识卡片
   - 主题研究 / 项目研究
   - 其他结构化笔记
2. 为整条笔记确定一个可检索的 `Title`：
   - 只出现一次
   - 放在最上面
   - 写成“主题 + 结论 / 对象”
3. 先搭骨架，再写内容：
   - 需要长期维护或模块较多时，用 `Heading`
   - 一个模块下存在固定维度时，用 `Subheading`
   - 其余解释都放 `Body`
4. 处理重点：
   - 加粗只给必须扫到的结论、关键词、关键判断和动作
   - 高亮只表达标签，不表达情绪
5. 选择块级结构：
   - `Checklist` 用于核对或待办
   - `Numbered List` 用于顺序、步骤、因果链
   - `Bullet List` 用于并列信息
   - `Table` 用于固定字段采集或并列对比
   - `Block Quote` 用于保留关键原话
   - `Monospaced` 用于代码、命令、API、字段名
   - 链接用于把单条笔记接入知识网络
6. 输出前做一次“不过度装饰”检查：
   - 不堆标题
   - 不滥用粗体
   - 不滥用颜色
   - 不把所有内容都塞进表格

## 输出方式

默认输出为“Apple Notes 样式标注版”，方便用户直接套用段落样式。使用以下标记：

- `[Title]`
- `[Heading]`
- `[Subheading]`
- `[Body]`
- `[Highlight: Yellow]`
- `[Highlight: Red]`
- `[Highlight: Green]`
- `[Highlight: Blue]`
- `[Checklist]`
- `[Numbered List]`
- `[Bullet List]`
- `[Table]`
- `[Quote]`
- `[Monospaced]`
- `[Link]`

如果用户明确要求“只给可直接粘贴的纯内容”，就去掉这些标签，只保留清晰结构和必要的加粗。

## 输出要求

- 默认用中文写，语言简洁、判断明确，不写空泛套话
- 不为了“看起来整齐”制造层级；每一层都要有管理价值
- 正文一段只讲一个点；连续 4 到 5 段无层级正文时，主动补结构
- 一屏里通常只保留 1 到 3 个加粗点
- 颜色数量要少，让颜色承担“分类”而不是“装饰”
- 引用只保留最关键的一两句，引用下方补一句判断
- 如果内容更适合连续论证，就不要强行改成表格
- 如果未来会继续补资料，优先设计可折叠的 `Heading` / `Subheading`
- 如果用户给的是碎片材料，先完成去重、归并、压缩，再排版

## 常用模板

严格排版时，先读取 [references/apple-notes-style-guide.md](references/apple-notes-style-guide.md)。默认优先使用以下模板之一：

1. 文章总结
   - `Title`
   - `Heading`: 核心问题 / 核心观点 / 关键逻辑 / 我的判断 / 可行动点
2. 知识卡片
   - `Title`
   - `Heading`: 这是什么 / 为什么重要 / 适用边界 / 我的判断 / 相关链接
3. 主题研究
   - `Title`
   - `Heading`: 研究问题 / 现状 / 关键分歧 / 我的判断 / 下一步 / 延伸阅读

## 质量检查

输出前快速自检：

- `Title` 是否具体到能在搜索里一眼看懂
- 长笔记是否用了可折叠的一级模块
- 二级结构是否只出现在可复用维度里
- 是否把加粗控制在真正的重点上
- 是否只给“核心结论 / 风险 / 动作 / 待验证”上色
- 列表、表格、引用、代码样式是否各司其职
- 是否补上了最值得继续追踪的相关链接