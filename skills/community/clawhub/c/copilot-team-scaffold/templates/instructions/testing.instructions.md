---
applyTo: ["**/tests/**", "**/*.test.{ts,tsx}"]
description: "Use when writing or editing tests. Covers mixed TDD strategy, pytest/vitest patterns, coverage targets, and test directory structure."
---
# 测试约束

## 混合测试策略

| 模式 | 适用场景 | 示例 |
|------|----------|------|
| TDD（先写测试） | 纯逻辑、边界条件多 | 认证签名、规则引擎、Upsert |
| 边写边测 | 模式统一 REST 端点 | CRUD API |
| 实现后补测试 | AI 输出/UI 交互不确定 | OCR Worker、UI 组件 |

## 覆盖率目标

| 类别 | 后端 | 前端 |
|------|------|------|
| 核心逻辑 | ≥ 90% | — |
| API 端点 / 纯逻辑 Hooks | ≥ 80% | ≥ 80% |
| 页面组件 | — | ≥ 50% |
| 整体 | ≥ 80% | ≥ 60% |

## 通用原则

- 每个测试只测一件事
- 测试命名清晰描述场景
- 遵循 Arrange-Act-Assert 模式
- Mock 外部依赖，不 Mock 被测代码
- 测试数据与业务数据隔离
