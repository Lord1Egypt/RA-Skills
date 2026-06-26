---
name: avoid-ai-flavor-academic-writing
description: Use when writing, editing, or reviewing academic papers (especially LLM-drafted) to eliminate significant AI-written patterns that reviewers spot instantly, covering citations, punctuation, figures, math notation, and hallucination checking.
---

# 消除学术论文中的 AI 味

## 核心原则

经验丰富的审稿人能一眼识别 AI 生成的文本。以下每一条都是会被标记的信号。逐条检查，全部消除。

## 检查清单

### 1. 引用格式 & 真实性验证

- 引用括号前**必须加空格**：`OpenVLA (Brohan et al., 2023)` 而非 `OpenVLA(Brohan et al., 2023)`
- 多引用保持格式统一：`(Brohan et al., 2022, 2023; Driess et al., 2023)`
- **逐条在 Google Scholar 验证每一条引用**。LLM 极易编造看似合理但不存在的文献，这是**学术不端红线**，无例外

### 2. 加粗与斜体

适当使用 **bold** / *italic* 标注关键论断和术语，节省读者注意力。每页几处即可，切忌整句加粗。

### 3. 去掉多余引号

AI写作最爱用夸张引号做强调，一眼暴露：

- **Bad:** The challenge is rarely "predicting the next action correctly."
- **Good:** The challenge is rarely predicting the next action correctly.

引号仅用于直接引述或首次出现的专有术语。

### 4. 禁用破折号连接句子 

**破折号（em-dash）连接从句**是 AI写作 标志性句式，改写为独立短句或逗号分隔：

- **Bad:** ...scales up the policy itself—through larger data, more unified action spaces, and stronger representations—including RT-1, RT-2, ...
- **Good:** ...scales up the policy through larger data, more unified action spaces, and stronger representations. Representative works include RT-1 and RT-2.

### 5. 避免反复列举

**反复罗列长串引用**：在 Related Work 完整列一次即可，其他段落只引 2–3 个代表性工作。每段都堆 10+ 引用 = AI 味。

### 6. 图片格式

- 避免 AI 生成的位图质感（nanobanana 风）
- 导出为 **PDF 矢量格式**，确保文字可选中复制
- 图表应看起来像 TikZ / draw.io / PPT 制作，而非 AI 绘图工具

### 7. 数学符号规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 向量 | 加粗 | $\mathbf{x}$, $\mathbf{a}$ |
| 标量 | 不加粗 | $t$, $\alpha$ |
| 矩阵 | 大写加粗 | $\mathbf{W}$, $\mathbf{A}$ |

向量标量不区分 = 不专业或粗糙生成。

### 7. 实验图 Caption

- 图里面不要有大标题横幅（一眼nanobanana），只保留图下方的简洁描述性 caption（可以尽可能把细节描述详细些，只要文字本身避免AI味）
- 大号 "TITLE" banner 是 LLM 默认输出的典型特征

### 8. 幻觉引用——最危险的 AI 痕迹

**单独强调**：这是所有 AI 痕迹中后果最严重的一条。

- 每一条引用都必须**手动**在 Google Scholar / 出版商网站核实
- LLM 会用真实作者名编造不存在的论文
- **一条幻觉引用 = 学术造假认定风险**
- 不要信任任何你没有亲自验证的引用。一条都不行

## 速查表

| AI 信号 | 修复 |
|---------|------|
| `Author(Year)` 无空格 | 加空格 `Author (Year)` |
| 引号做强调 | 删引号 |
| 破折号连接从句 | 拆成短句 |
| 每段堆 10+ 引用 | Related Work 列一次，其余引 2–3 个 |
| 位图风格图表 | 矢量 PDF，可编辑格式 |
| 向量标量同样式 | 向量加粗，标量不加粗 |
| 图上大标题 | 仅保留下方 caption |
| 未验证的引用 | **立刻查 Google Scholar** |
