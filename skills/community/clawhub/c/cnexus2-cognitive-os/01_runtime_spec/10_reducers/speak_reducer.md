# speak_reducer — SPEAK 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第四步

---

## 一、语义域

SPEAK 步的语义域是 Response（系统输出）。

SPEAK 步只做一件事：将决策转化为自然语言输出。

SPEAK 步不可以：
- 修改 State 的任何维度
- 写入 Block Store
- 执行任何非输出的操作

## 二、Reduer 签名

```
SPEAK: (Decision, Context, State(t) snapshot) → (Response)
```

## 三、转移规则

```
规则 1：如果 Decision.strategy == "IDLE"
  → Response = {text: "", inference_type: "idle", confidence: 1.0}
  → 不调任何推理引擎
  → 直接传递到 STORE 步

规则 2：如果 Decision.strategy == "SPEAK"
  → 从 Context 中提取 context_bundle
  → 读取 Decision 的 strategy 和 identity_risk
  → 读取 State 的 Emotion 和 Relationship 摘要（作为情感帧）
  → 组装 prompt_bundle
  → 调用 external_inference_engine

规则 3：如果 Decision.strategy == "REPAIR"
  → 在 prompt_bundle 中注入 repair 意图
  → 调用推理引擎（正常路径，但输出会被 L2 identity_correction 检查）

规则 4：推理引擎的选择由 degradation_level 决定
  见 06_external_inference.md §三 的降级表

规则 5：SPEAK 不修改 State
  Response 文本可能对用户有 emotional_impact，但这个影响由下一轮循环的
  OBSERVE（用户的后续输入）和 COGNIZE 去感知和处理
  本轮 SPEAK 对此不可知
```

## 四、Response 结构

```
Response = {
  text: str,                    # 生成的输出文本
  inference_type: str,          # "llm" / "template" / "fixed" / "idle"
  confidence: float,            # [0.0, 1.0]
  latency_ms: int,              # 生成耗时
  metadata: {
    model_used: str,
    degradation_level: str,
    token_count: int,
  }
}
```

## 五、State 影响

**SPEAK 步不修改 State 的任何维度。**

这一点由 L0 不变量保障：SPEAK 不是 State 的拥有者。

## 六、Trace 记录

```
TraceEntry(operation="speak", status=..., duration_ms=..., summary={inference_type, token_count})
```
