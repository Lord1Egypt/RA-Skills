# Infographic And PPT Capabilities - 参考分析

## 分析对象

- `/Users/tanshow/.codex/skills/.system/imagegen/SKILL.md`
- `/Users/tanshow/.codex/skills/slides/SKILL.md`

## 1. imagegen

### 值得复用的能力

- 已把信息图归入明确 use case
- 适合单张传播型视觉成品
- 对图像风格、画幅和提示词结构有成熟约束

### 不适合直接泛化的地方

- 长文本和复杂表格不适合完全交给图像生成
- 高编辑性不是它的强项

## 2. slides

### 值得复用的能力

- 明确要求输出 `.pptx` 和源 `.js`
- 明确要求渲染、溢出和字体校验
- 明确优先保持 PowerPoint 可编辑性

### 不适合直接泛化的地方

- 不适合把它当成单张海报或图片生成器
- 信息不足时，不能直接跳过 deck 结构设计

## 汇总结论

信息图和 PPT 共享“视觉表达”这一层，但执行面完全不同。

- 信息图更偏单张位图成品，优先 `imagegen`
- PPT 更偏可编辑交付物，优先 `slides`

所以它们应该是两份独立原子能力，而不是一个合并能力。
