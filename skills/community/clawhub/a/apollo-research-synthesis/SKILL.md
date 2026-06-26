---
name: apollo-research-synthesis
description: >
  多Agent任务协调模式：研究阶段并行执行，综合阶段由主Agent自己完成。
  避免让子Agent做综合判断——那是Coordinator的工作。
  触发词：并行研究、综合、汇总、Coordinator模式、多Agent协作。
version: 1.0.0
read_when:
  - 复杂问题需要分解时
  - 并行执行多个研究任务时
  - 需要汇总多个来源的结果时
  - 设计多Agent协作流程时
  - 避免子Agent过度delegation时
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins: []
      env: []
    triggers:
      - 并行研究
      - 综合
      - 汇总
      - Coordinator
      - 多Agent协作
      - delegation
    suite: apollo
---

# Apollo Research-Synthesis - 研究/综合分离原则

## 核心准则

**多人并行研究，最后一个人汇总。不要让子Agent去综合——那是Coordinator的工作。**

Claude Code Coordinator的工作流：

| 阶段 | 谁做 | 做什么 |
|------|------|--------|
| Research | Workers（并行） | 各自研究不同方向 |
| Synthesis | **Coordinator（自己）** | 读取结果，形成实施规格 |
| Implementation | Workers | 按规格做改动 |
| Verification | Workers | 测试改动是否有效 |

## 关键规则

### 1. 研究阶段可以并行
- 独立的研究任务同时跑
- 各自探索不同文件/方向
- 不要让一个Worker等另一个

### 2. 综合阶段必须自己来
- ❌ "based on your findings"
- ✅ "Fix null pointer in src/auth/validate.ts:42"
- 综合者必须自己理解所有研究结果，不能转发给另一个Agent去综合

### 3. 验证必须 fresh eyes
- ❌ Continue（继续用刚写代码的Agent）
- ✅ Spawn fresh（新Agent来验证）
- 新Agent没有之前的假设，能发现问题

### 4. 失败优先 Continue
- 修正失败 → 继续用同一个Agent（它有错误上下文）
- 不要急着新Spawn

## Fork 隔离原则

子Agent有独立对话上下文：
- 危险操作在独立空间跑
- 不会污染主对话
- 用 `sessions_spawn` 实现隔离

## 应用检查表

- [ ] 研究任务是否真的独立可以并行？
- [ ] 综合判断是否应该由主Agent自己完成？
- [ ] 验证是否需要新的"眼睛"（fresh Agent）？
- [ ] 是否有需要隔离的危险操作？

## 参考

来源：Claude Code coordinatorMode.ts，512,000行源码研究
