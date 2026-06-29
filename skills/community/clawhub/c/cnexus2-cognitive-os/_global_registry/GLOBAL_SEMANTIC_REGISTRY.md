# Global Semantic Registry — 全局语义唯一注册表

## 职责

本注册表定义所有跨文件出现的 core concept 的唯一 owner file。不允许跨文件重新定义，只允许 reference，不允许 re-description。

## Core Concepts Registry

| 概念 | 唯一 owner | 其他文件可以 | 其他文件不可 |
|------|-----------|------------|--------------|
| recall | 01_runtime_spec/04_recall_context.md | 引用 recall 的输出、传递 recall_items | 定义 recall 的语义边界 |
| state | core_essence/04_data_model_essence.md | 读取 state 的值、传递 state 引用 | 定义 state 的更新规则、定义 state 的子结构 |
| identity | core_essence/01_identity_attractor.md | 使用 identity 作为决策参考 | 定义 identity 的含义、定义 attractor 的维度 |
| identity_coherence | core_essence/01_identity_attractor.md | 引用 identity_coherence 作为 P1 判定依据 | 定义 identity_coherence 的计算方法 |
| memory | core_essence/04_data_model_essence.md | 引用 memory 的 block、读取 block | 定义 memory 的写入策略、定义衰减规则 |
| trace | core_essence/04_data_model_essence.md | 写入 trace 条目、读取 trace_id | 定义 trace 的结构、定义 trace 的存储格式 |
| degradation | src/l2_degradation_policy.py（待建） | 使用 degradation_level 作为信号 | 定义 degradation 的级别、定义降级路径 |
| inference | src/external_inference_adapter.py（待建） | 使用 InferenceRequest/Response 作为 I/O | 定义推理引擎的调用方式、定义 prompt 结构 |
| attractor | core_essence/01_identity_attractor.md | 使用 attractor_target、计算 force | 定义 attractor 的维度、定义目标点 |
| objective_function | core_essence/05_system_objective_function.md | 使用 P1/P2/P3 优先级 | 重新定义优先级顺序 |
| error | 01_runtime_spec/08_error_codes_response.md | 使用 ErrorSignal、引用 error code | 定义误差信号格式、定义 error code |
| loop | core_essence/02_minimal_cognitive_loop.md | 引用 loop 结构 | 定义 loop 的步骤、定义步骤 |
| belief_weight | core_essence/04_data_model_essence.md | 引用 belief Block 的 importance 字段 | 重新定义 belief 的语义范围 |
| narrative | core_essence/04_data_model_essence.md | 引用 narrative Block | 重新定义 narrative 的语义边界 |
| persona | core_essence/04_data_model_essence.md | 引用 persona Block | 重新定义 persona 的语义边界 |
| emotion | core_essence/04_data_model_essence.md | 引用 emotion Block | 重新定义 emotion 的语义边界 |
| intent | core_essence/04_data_model_essence.md | 引用 intent Block | 重新定义 intent 的语义边界 |
| belief | core_essence/04_data_model_essence.md | 引用 belief Block | 重新定义 belief 的语义边界 |
| episodic | core_essence/04_data_model_essence.md | 引用 episodic Block | 重新定义 episodic 的语义边界 |
| archival | core_essence/04_data_model_essence.md | 引用 archival Block | 重新定义 archival 的语义边界 |
| reflective | core_essence/04_data_model_essence.md | 引用 reflective Block | 重新定义 reflective 的语义边界 |
| Block | core_essence/04_data_model_essence.md | 引用 Block 结构定义 | 重新定义 Block 的结构和字段 |
| State | core_essence/04_data_model_essence.md | 引用 State 结构定义 | 重新定义 State 的维度和不变量 |
| OBSERVE | core_essence/02_minimal_cognitive_loop.md | 引用 OBSERVE 步的语义角色 | 扩展 OBSERVE 的语义域 |
| COGNIZE | core_essence/02_minimal_cognitive_loop.md | 引用 COGNIZE 步的语义角色 | 扩展 COGNIZE 的语义域 |
| DECIDE | core_essence/02_minimal_cognitive_loop.md | 引用 DECIDE 步的语义角色 | 扩展 DECIDE 的语义域 |
| SPEAK | core_essence/02_minimal_cognitive_loop.md | 引用 SPEAK 步的语义角色 | 扩展 SPEAK 的语义域 |
| STORE | core_essence/02_minimal_cognitive_loop.md | 引用 STORE 步的语义角色 | 扩展 STORE 的语义域 |
| REFLECT | core_essence/02_minimal_cognitive_loop.md | 引用 REFLECT 步的语义角色 | 扩展 REFLECT 的语义域 |
| Reducer | 01_runtime_spec/01_loop_execution.md | 使用 Reducer 的输入输出 | 定义 Reducer 的执行细节 |
| Observation | 01_runtime_spec/10_reducers/observe_reducer.md | 引用 Observation 结构 | 扩展 Observation 的语义域 |
| Context | 01_runtime_spec/10_reducers/cognize_reducer.md | 引用 Context | 重新定义 Context 的组成 |
| Decision | 01_runtime_spec/10_reducers/decide_reducer.md | 引用 Decision | 重新定义 Decision 的维度 |
| Response | 01_runtime_spec/10_reducers/speak_reducer.md | 引用 Response 结构 | 扩展 Response 的语义域 |
| StoreResult | 01_runtime_spec/10_reducers/store_reducer.md | 引用 StoreResult | 扩展 StoreResult 的字段 |
| ReflectResult | 01_runtime_spec/10_reducers/reflect_reducer.md | 引用 ReflectResult | 扩展 ReflectResult 的字段 |
| EmotionSnapshot | 01_runtime_spec/02_cognitive_state.md | 引用 emotion 的三个分量 | 重新定义 emotion 分量的语义 |
| RelationshipSnapshot | 01_runtime_spec/02_cognitive_state.md | 引用 relationship 的三个分量 | 重新定义 relationship 的语义 |
| GoalSnapshot | 01_runtime_spec/02_cognitive_state.md | 引用 goal 的字段 | 重新定义 goal 的语义 |
| AttentionSnapshot | 01_runtime_spec/02_cognitive_state.md | 引用 attention 的字段 | 重新定义 attention 的语义 |
| StatusAnomalySignal | 01_runtime_spec/02_cognitive_state.md | 接收和处理异常信号 | 定义异常信号的结构和内容 |
| identity_position | 01_runtime_spec/03_identity_position.md | 引用 identity_position 的标记值 | 定义 identity_position 的计算规则 |

## 词汇升格记录

| 原词汇 | 来源 | 升格为新概念 | 注册日期 | 所属 owner |
|--------|------|-------------|---------|-----------|
| accumulated_weight | kernel.py cog_state | belief_weight（作为 belief Block 的 importance 字段） | 2026-06-22 | core_essence/04_data_model_essence.md |
| _narrative_log | kernel.py | narrative（作为 8 种 Block 类型之一） | 2026-06-22 | core_essence/04_data_model_essence.md |

## 剪除词汇记录

| 原词汇 | 来源 | 剪除原因 | 替代方案 |
|--------|------|---------|---------|
| skill | kernel.py 全局 | 不属于 L0 词汇表 | external_inference_engine |
| skill_graph | kernel.py | 旧的 skill-router 架构 | L1 DECIDE 步的策略选择 |
| skill_vectors | kernel.py | 不属于 L0 词汇表 | 由 L1 向量化实现 |
| classification | kernel.py | 不属于 L0 词汇表 | 由 L1 cognitive state 替代 |
| router_policy | kernel.py | 不属于 L0 词汇表 | L1 DECIDE 步的策略参数 |
| _influence_map | kernel.py | 违背 Loop Primacy 规则 | L1 DECIDE 步的 cross-step 影响 |
| execution_history | kernel.py | 内容由标准化 Trace 替代 | core_essence/04_data_model_essence.md Trace 定义 |
| skill_registry | kernel.py | 不属于 L0 词汇表 | L1 SPEAK 步的 external_inference_engine |

## Cross-step 共享概念管理

### "state" 的语义边界

| 出现位置 | 语义角色 | 权限 |
|---------|--------|------|
| core_essence/04_data_model_essence.md（owner） | 定义 state 的结构、不变量 | 所有关于 state 的定义必须在此 |
| 01_runtime_spec/10_reducers/cognize_reducer.md（L1） | 定义 state 中 Emotion、Attention 的更新规则 | 只读引用，不可重新定义含义 |
| 01_runtime_spec/10_reducers/decide_reducer.md（L1） | 读取 state 作为决策参考，更新 Relationship、Goal | 只读引用，不可修改 state 的 L0 结构 |
| 01_runtime_spec/10_reducers/store_reducer.md（L1） | 读取 state 作为 block importance 输入，递增 Meta | 只读引用 |
| 01_runtime_spec/10_reducers/speak_reducer.md（L1） | 读取 state 作为 prompt 组装的情感帧 | 只读引用 |

## 新增概念注册流程

如果需要引入新的跨文件概念：
1. 确认概念在当前 registry 中不存在
2. 确定其唯一 owner file
3. 注册到本 registry（包括语义边界和权限表）
4. 注册通过后，其他文件方可引用

**禁止先使用再注册。**

---

## 📜 SPEC_FREEZE PROOF v2_final

```
冻结日期: 2026-06-22 16:08 GMT+8
总文件数: 33
总规格大小: 109,215 bytes
完整性哈希 (SHA256): 4a4f011766f458d653fce2cb026345e33bad057079e9d56a4d8dea9345e881ec
```

**本目录已锁死。** 后续任何对 L0/L1 规格的修改，必须走 L3 Revision Proposal 管道。违反者触发 LAYER_VIOLATION。

