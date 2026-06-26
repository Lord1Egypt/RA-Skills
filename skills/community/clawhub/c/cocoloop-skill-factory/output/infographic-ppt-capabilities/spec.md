# Infographic And PPT Capabilities - 统一 Spec

## 基本信息

- 名称：`infographic-ppt-capabilities`
- 目标：补齐信息图和 PPT 生成能力的正式能力定义与流程接入
- 当前阶段：文档与流程加固

## 必须满足的要求

### 要求 1

信息图需要明确区分：

- 单张位图成品
- 可编辑版式

### 要求 2

`.pptx` 需求需要明确区分：

- deck 结构
- 可编辑性
- 渲染和溢出校验

### 要求 3

信息图和 PPT 不能共用一个原子能力文档。

### 要求 4

这两项能力都要进入对应预设和主流程调研问题包。

## 输入

- 本地 `imagegen` skill
- 本地 `slides` skill
- 当前原子能力目录

## 输出

- 两份新的原子能力文档
- 更新后的预设
- 更新后的主流程和产品需求文档

## 成功标准

- `atomic-capability/` 已新增这两项能力
- `frontend_design` 与 `document_artifacts` 已能引用它们
- 主流程已能给出推荐方向
