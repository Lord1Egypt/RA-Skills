# 06_external_inference — 外部推理引擎规范

**层级：L1（执行层规格）**
**依据：** L0 core_essence/02_minimal_cognitive_loop.md（SPEAK 步）

---

## 一、SPEAK 步的职责

SPEAK 步只做一件事：**将 DECIDE 步的决策转化为自然语言输出。**

```
SPEAK: (Decision, State(t), Context) → Response
```

SPEAK 步不负责：
- 路由选择（属于 DECIDE）
- 知识图谱构建（如果有，属于外部引擎内部）
- 记忆写入（属于 STORE）

## 二、Inference Engine 接口

### 2.1 抽象推理引擎

SPEAK 步调用的 external inference engine 是一个抽象组件：

```
InferenceEngine:
  Input: (prompt_bundle, system_persona, State_snapshot)
  Output: InferenceResponse {text, metadata, confidence}
```

引擎的具体实现不固定（LLM / 模板引擎 / 固定响应）——由 SPEAK reducer 在运行时根据 degradation_level 选择。

### 2.2 Prompt 组装规则

L1 层面不定义 prompt 的精确模板（属具体实现）。但定义 **必须包含的信息**：

```
prompt_bundle 至少包含：
  1. COGNIZE 步的 Context（摘要）
  2. DECIDE 步的 Decision（策略名、置信度）
  3. 当前 State 的三个维度摘要（不作为完整 State 暴露）
```

**禁止** 在 prompt_bundle 中暴露：
- Block Store 的直接内容（只能暴露 recall_items 的摘要）
- Trace 内容
- State 的 Meta 信息（session_count / total_interactions）

## 三、降级下的 SPEAK

| degradation_level | SPEAK 行为 |
|-----------------|-----------|
| L0（正常） | 调用首选推理引擎（如 LLM） |
| L1（轻度） | 调用次要推理引擎（如本地小模型） |
| L2（中度） | 调用模板引擎（固定的 prompt 模板 + 状态填充） |
| L3（严重） | 固定响应（如 "系统正在维护中"） |

## 四、SPEAK 输出的 Response 结构

```
Response = {
  text: str,                    # 生成的输出文本
  inference_type: str,          # "llm" / "template" / "fixed"
  confidence: float,            # [0.0, 1.0] 推理引擎对输出的自评置信度
  latency_ms: int,              # 生成耗时
  metadata: {
    model_used: str,            # 实际使用的推理模型名称
    degradation_level: str,     # 当前降级级别
    token_count: int,           # 输出长度
  }
}
```

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| LLM 的具体 prompt 模板 | 实现层 |
| Degradation_level 的选择器 | L2 degradation_policy |
| 模板引擎的 fallback 链 | 实现层 |
| 推理引擎的配置（endpoint、model name） | 实现层 config |
