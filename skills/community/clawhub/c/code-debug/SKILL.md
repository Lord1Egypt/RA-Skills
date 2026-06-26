---
name: code-debug
description: Diagnose failures in the current local codebase and produce the smallest defensible fix. Use when the user reports an error, crash, bad output, flaky behavior, failed test, or asks for root-cause analysis and a concrete repair in the workspace. Do not use for system administration or hardware troubleshooting. Chinese triggers: 报错、运行异常、崩溃、逻辑错误、定位原因、修复 bug、最小复现.
---

# 调试修复

先找根因，再动代码。

## 工作流

1. 能复现就先复现，不能复现就尽量缩小到最小场景。
2. 先判断错误类别：语法、运行时、逻辑、异步顺序、类型、边界、依赖、配置或资源处理。
3. 优先检查常见问题：off-by-one、空值处理、过期状态、竞争条件、输入假设错误、资源未释放。
4. 用代码、日志或执行结果锁定根因，不做玄学猜测。
5. 用最小安全修复解决真正的根因。
6. 非必要不夹带重构；结构太差影响修复时再单独说明。
7. 用最短可靠方式验证修复结果。

## 输出

- 根因
- 影响范围
- 最小复现场景，如果能给出
- 修复方向或补丁
- 验证方法
