# 00_layer_invariance_axioms — 认知分层公理系统

本文是全部 core_essence 文件的**元规则**。所有文件的设计和内容必须遵守以下三条护栏和强化规则，违反即视为系统设计违规。

---

## 一、层级定义

```
L0 = core_essence（系统本体层）     → core_essence/
L1 = runtime_spec（执行层）         → src/（代码）
L2 = stability_spec（稳定控制层）   → src/l2_*.py（待建）
L3 = 治理/演化/反馈系统集合        → src/l3_*.py（待建）
```

## 二、三条护栏（不可违反）

### 🛑 护栏 1：L0 非执行约束

L0 不允许包含任何可执行语义，包括但不限于：
- update rule（更新规则）
- state transition（状态转换）
- scoring function（评分函数）
- algorithm（算法步骤）
- control flow（控制流程）
- runtime behavior（运行时行为描述）

L0 只能定义：
- ontology（是什么）
- invariants（不能变什么）
- ordering（优先级关系）
- boundary（边界条件）

**验证方法：** L0 中的任何语句如果在不依赖 runtime 的情况下可以直接被实现为代码，则违反本护栏。

### 🛑 护栏 2：禁止运行时反向补全 L0

L1/L2/L3 runtime 产生的观测**不得**用于反向修改或补全 L0 定义。

**允许行为：**
- 生成 revision_proposal（提案）
- 提案使用 L0 词汇表，不引用 L1/L2/L3 概念
- 提案经人工确认后生效

**禁止行为：**
- 直接修改 L0 文件
- 通过 runtime 推导 L0 新语义
- 用运行数据"优化定义"
- 在 L0 中引入任何来自运行时观测的术语

### 🛑 护栏 3：跨层依赖单向图

依赖方向必须严格单向：
```
L0 ──→ L1 ──→ L2 ──→ L3 (runtime / evolution)
```

**禁止：**
- L1/L2 引用 L0 的实现细节
- runtime 推导 L0 语义
- 下层影响上层定义

## 三、强化规则

### 🔒 规则 1：L0 Vocabulary Canon

L0 中只能使用以下词汇表中的术语。任何不在词汇表中的术语，出现在 L0 文件中视为语义污染。

**L0 词汇表（权威列表）：**

| 分类 | 允许的术语 |
|------|-----------|
| 身份 | identity_attractor, identity_coherence, 认知诚实, 关系稳定性, 自我连续性, 吸引子, target_point, 下限, 牵引力 |
| 回路 | cognitive_loop, OBSERVE, COGNIZE, DECIDE, SPEAK, STORE, REFLECT, 回路不变量, 步序不可逆 |
| 接口 | POST /chat, GET /status, GET /memory, POST /reset, schema, endpoint, 响应, 请求 |
| 数据 | Block, State, Trace, persona, emotion, intent, belief, narrative, episodic, archival, reflective, importance, decay_rate, Metadata |
| 目标 | objective_function, P1, P2, P3, identity coherence, continuity, structural drift, 优先级, 冲突规则 |
| 边界 | ontology, invariant, ordering, boundary, 强制下限, 强制上限, 非执行约束 |
| 抽象推理 | external_inference_engine, 输出通道, 推理引擎（不绑定实现） |
| 演化 | revision_proposal, 提案, L0 词汇表, 翻译守卫 |
| 层间规则 | L0 Vocabulary Canon, L0 Immutability Rule, L1 Semantic Non-Authority Rule, Loop Primacy Rule, Proposal Validation Pipeline, 翻译守卫 |

### 🔒 规则 2：L0 Immutability Rule

L0 层的定义在系统生命周期中保持稳定。运行时产生的任何观测不得反向修改 L0。

**适用对象：** core_essence 目录下的所有文件。

**不可变承诺：**
- L0 文件不因运行时行为而修改
- L0 文件仅通过 revision_proposal 流程 + 人工确认而修改

### 🔒 规则 3：L1 Semantic Non-Authority Rule

L1/L2 **不得定义或重新解释 L0 概念**。L1/L2 只能对 L0 术语进行可执行化转换（operationalize），不能扩展 L0 术语的语义范围。

### 🔒 规则 4：Loop Primacy Rule

所有运行时语义必须定义为认知循环内部的一次转换。任何不能在循环迭代上下文中表达的结构都是无效的。

### 🔒 规则 5：Proposal Validation Pipeline

任何来自 L3 的 revision_proposal 必须经过以下验证才能进入人工确认：
1. 词汇表检查 — 所有术语在 L0 词汇表中
2. 语义范围检查 — 不引入 L1/L2/L3 实现概念
3. 一致性检查 — 不违反护栏 1/2/3
4. 上下游影响评估

## 四、违反处理

任一文件违反上述任意一条护栏或强化规则：
1. 标记为 **LAYER_VIOLATION**
2. 记录违规详情
3. 违规内容禁止进入 final_signoff
4. 修正后重新审查

---

*本文件在系统生命周期中保持不可修改。*
