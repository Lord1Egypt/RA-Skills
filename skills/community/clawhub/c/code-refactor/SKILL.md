---
name: code-refactor
description: Improve readability, structure, and maintainability of the current local codebase without changing behavior. Use when the user asks to clean up code, reduce duplication, simplify control flow, rename for clarity, or reorganize logic while preserving compatibility. Do not use for feature work disguised as refactoring. Chinese triggers: 重构、优化结构、清理代码、提取重复逻辑、提高可读性、保持行为不变.
---

# 代码重构

只整理结构，不改变原有行为。

## 工作流

1. 先确认当前行为，再保证重构后行为保持一致。
2. 先指出具体问题：重复代码、命名差、函数过长、条件分支纠缠、职责不清。
3. 除非用户明确允许，否则不要破坏公共接口和调用方预期。
4. 只有在能明显降低复杂度或重复时才抽取公共逻辑或重组模块。
5. 重构时不顺手加入新业务逻辑。
6. 保留原有注释风格，除非注释已经失真。
7. 重构后验证行为未变。

## 输出

- 重构前的问题
- 重构思路
- 如何保证行为不变
- 已做验证
