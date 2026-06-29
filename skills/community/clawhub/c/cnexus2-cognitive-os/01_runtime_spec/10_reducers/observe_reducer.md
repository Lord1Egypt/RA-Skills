# observe_reducer — OBSERVE 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第一步

---

## 一、语义域

OBSERVE 步的语义域是 Observation（感知结果）。

OBSERVE 步不涉及：认知理解（COGNIZE 域）、策略选择（DECIDE 域）、输出（SPEAK 域）、Block 操作（STORE 域）。

## 二、Reduer 签名

```
OBSERVE: (raw_input: str, State.meta) → (Observation)
```

## 三、转移规则

```
规则 1：将原始输入标准化
  normalized = raw_input.strip().lower()

规则 2：检测空输入
  if raw_input.strip() == "":
    Observation.type = "empty_observation"
    跳过后续所有认知步骤 → 直接进入 STORE

规则 3：非空输入的类型判定
  Observation.type = "text_input"  (当前只支持文本输入)

规则 4：不可绕过
  OBSERVE 在任何状态下都必须执行。无豁免。
```

## 四、Observantion 结构

```
Observation = {
  type: str,           # "text_input" / "empty_observation"
  raw: str,            # 原始输入
  normalized: str,     # 标准化后的输入（小写、去空白）
  is_empty: bool,      # 是否是空输入
  timestamp: float,    # 接收时间（unix 秒）
}
```

## 五、State 影响

**OBSERVE 步不修改 State 的任何维度。**

OBSERVE 只产生 Observation，不更新 emotion/relationship/goal/attention/meta。

## 六、Trace 记录

```
TraceEntry(operation="observe", status=..., duration_ms=...)
summary: {observation_type, char_length}
```
