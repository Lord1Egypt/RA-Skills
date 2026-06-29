# 04_degradation_policy — 降级策略规格

**层级：L2（稳定性控制层）**

---

## 一、降级级别定义

| 级别 | 名称 | 含义 | 切换方向 |
|------|------|------|---------|
| L0 | 正常 | 全部 6 步完全执行 | — |
| L1 | 轻度 | 单组件精度降低，结构不变 | DOWN / UP |
| L2 | 中度 | 功能简化，部分步骤模板化 | DOWN / UP |
| L3 | 严重 | REFUGE 模式，仅保留基础功能 | DOWN / UP |
| （结构冻结）| 极端 | 保留 persona + archival，其余归档 | 仅 DOWN（不可逆） |

每一级的降级路径必须满足**单向收敛**——降级时 Step 的功能简化只能越来越宽松（切换具体推理引擎、使用缓存或固定文本），永远不会让系统状态变得更脆弱。

## 二、各级降级的行为变化

### 2.1 L0 → L1（轻度降级）

| 步 | 行为变化 |
|----|---------|
| OBSERVE | 不变 |
| COGNIZE | Emotion/Attention 变化步长上限减半（之前 §2.1 的 δ 各减 50%） |
| DECIDE | 仅保留"SPEAK"和"RECALL"两种策略选项 |
| SPEAK | 优先选次要推理引擎（本地小模型），非首选 LLM |
| STORE | 写入所有 Block，但不执行合并（避免合并出错） |
| REFLECT | 跳过来自 COGNIZE 的复杂反思，只写 narrative summary |

### 2.2 L1 → L2（中度降级）

| 步 | 行为变化 |
|----|---------|
| OBSERVE | 不变 |
| COGNIZE | 不更新 Emotion/Attention（使用上一轮值） |
| DECIDE | 仅保留"SPEAK"策略 |
| SPEAK | 调用模板引擎（基于当前 State 维度的固定模板） |
| STORE | 写入 emotion + episodic，跳写其他类型 |
| REFLECT | 跳过 |

### 2.3 L2 → L3（严重降级 / REFUGE）

| 步 | 行为变化 |
|----|---------|
| OBSERVE | 不变（必须） |
| COGNIZE | 不更新任何 State 维度 |
| DECIDE | 始终选择 "REPAIR" |
| SPEAK | 固定响应文本 |
| STORE | 写入 emotion + episodic（必须） |
| REFLECT | 跳过 |

### 2.4 结构冻结（极端降级，不可逆）

```
1. 所有 Block 除 persona 和 archival 外，全部归档到 ARCHIVE 状态
2. State 冻结到当前值
3. Trace 全部清空（保留 1 条：记录结构冻结事件）
4. 系统进入最小存活模式：
   OBSERVE + STORE（必须）
   COGNIZE 仅检查 persona 状态
   DECIDE = IDLE
   SPEAK = 固定文本
   REFLECT = 跳过
```

## 三、Re-arm（重新激活）条件

| 当前降级级别 | 可回到的级别 | 条件 |
|-------------|------------|------|
| L1 | L0（正常） | 异常信号连续 2 轮未出现 |
| L2 | L1 | L0 断言集全部通过 + 异常信号 1 轮未出现 |
| L3（REFUGE）| L2 | L0 断言集全部通过 + 连续 2 轮无异常 |
| 冻结 | 无法回退 | 不可逆 |

## 四、Degradation 信号格式

Degradation 信号作为只读引用传给各层：

```
DegradationSignal = {
  level: str,            # "L0"/"L1"/"L2"/"L3"
  active_since: float,   # 进入当前级别的时间
  reason: str,           # 触发降级的原因简述
  previous_level: str,   # 上一级
  iterations_in_level: int,  # 在当前级别维持的轮数
  rearm_eligible: bool,  # 是否满足重新激活条件
}
```

**DegradationSignal 的语义边界：**
- L1 各 reducer 可以**读取** degradation_level 来调整行为
- L0 文件**不可**引用 degradation（L0 对运行时降级无感）
- L3 文件可以**读取** degradation history 作为反馈输入

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 各 step 内部的具体降级实现 | 各 reducer |
| REFUGE 模式的外部调度 | L3 失败分析 |
| 降级调用的引擎配置（model 名/endpoint 等） | 实现层配置文件 |
