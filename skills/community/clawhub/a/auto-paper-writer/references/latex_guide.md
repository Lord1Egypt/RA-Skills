# LaTeX 学术论文写作指南

## 论文结构规范

### Abstract（摘要）
- **长度**：150-250 词
- **内容**：
  1. 研究问题（1句）
  2. 现有方法不足（1-2句）
  3. 本文解决方案（1-2句）
  4. 主要创新点（2-3句）
  5. 实验效果（1-2句）
- **避免**：缩写、引用、公式

### Introduction（引言）
结构：
1. **背景**：领域重要性（1段）
2. **问题**：现有挑战（1-2段）
3. **现有工作**：相关方法及不足（1-2段）
4. **本文贡献**（明确列出 3-5 条）：
   - 提出 XXX 方法
   - 解决 XXX 问题
   - 达到 XXX 效果
5. **论文结构**：后续章节说明

### Related Work（相关工作）
- 按**方法类型**分类，不是按时间顺序
- 每类工作：总结 + 指出不足
- 与本文方法对比（可在 Introduction 或单独段落）

### Proposed Method（方法）
- **自顶向下**：先概述框架，再详细介绍各模块
- 使用**图表**辅助说明
- **公式**要有解释，不要堆砌
- 明确与现有工作的区别

### Experiments（实验）
1. **数据集**：介绍实验使用的数据集
2. **基线**：对比的现有方法
3. **设置**：超参数、训练细节
4. **结果**：主要指标表格 + 必要图表
5. **分析**：消融实验、复杂度分析

### Conclusion（结论）
- 总结本文工作（3-5句）
- 承认局限性
- 指出未来方向

## 语言规范

### 常用表达

**研究动机**：
- "Despite the remarkable performance of..."
- "However, existing methods still suffer from..."
- "A key challenge in this field is..."

**本文贡献**：
- "We propose a novel framework called..."
- "The main contributions are threefold:"
- "Extensive experiments show that..."

**实验结论**：
- "Our method outperforms state-of-the-art by X%"
- "Specifically, we observe that..."

### 避免的表达
- "We will show..." → "We show"
- "In this paper, we propose..." → "We propose"（已在前文说明）
- 主观强调："obviously", "clearly", "undoubtedly"

## 常见错误

1. **公式换行**：等号对齐，`\\` 换行
2. **引用格式**：`\cite{key}` 不是 `[[1]]`
3. **图表标题**：Table 在上方，Figure 在下方
4. **参考文献**：检查会议/期刊名称缩写
