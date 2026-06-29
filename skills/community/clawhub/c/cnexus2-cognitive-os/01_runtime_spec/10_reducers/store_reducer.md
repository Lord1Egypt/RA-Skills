# store_reducer — STORE 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第五步

---

## 一、语义域

STORE 步的语义域是 StoreResult（存储确认）。

STORE 步只做一件事：将本轮交互的关键信息写入 Block Store。

STORE 步不可以：
- 修改 State 的任何维度（但可以递增 Meta.total_interactions）
- 修改 Decision
- 调用外部推理引擎

## 二、Reduer 签名

```
STORE: (Response, State(t) snapshot, iteration_meta) → (StoreResult)
```

## 三、转移规则

```
规则 1：始终执行——L0 不变量
  即使在 IDLE 模式或降级模式，STORE 步也必须执行
  无法写入时（存储满/故障），在 store_result 中标记 failed，但不阻止下一步

规则 2：每轮至少写入一条 Block
  至少写入 emotion label（覆盖写最新一条）和 episodic label（追加一条）
  共 2 条 Block

规则 3：emotion Block
  label = "emotion", content = State.Emotion 的三个分量的当前值
  覆盖写：只保留最新一条 emotion Block
  decay_rate = 0.30（快速淘汰）

规则 4：episodic Block
  label = "episodic", content = 本轮的输入-输出摘要
  decay_rate = 0.20
  每轮添加一条，不超过上限

规则 5：intent Block
  不符合以下条件的 Block 不写入：
  - 当前 active_intent 与前一轮 intent 不同时
  - 当前 intent 标签首次出现
  label = "intent", content = intent 描述 + 触发时间
  decay_rate = 0.15

规则 6：archival Block
  由 DECIDE 步标记或 L3 反馈触发写入
  label = "archival", content = 高价值事实
  decay_rate = 0.01

规则 7：reflective Block
  不在 STORE 步写入 | reflective Block 由 REFLECT 步生成
  在 REFLECT 步的 reducer 中写入（参见 reflect_reducer）

规则 8：batch 写入
  STORE 步将所有 Block 写入统一通过 Block Store 接口（batch 模式）
  单个 Block 写入失败不影响其他 Block
```

## 四、StoreResult 结构

```
StoreResult = {
  blocks_written: {       # 每种类型的写入数量
    emotion: int,
    episodic: int,
    intent: int,
    archival: int,
  },
  total_blocks: int,      # 写入后的 Block Store 总条数
  failed_writes: list,    # 写入失败的 block_id（如果有）
  decay_activated: bool,  # 本轮是否触发衰减
  eviction_triggered: bool, # 本轮是否触发淘汰
  timestamp: float,
}
```

## 五、State 影响

**STORE 步更新的 State 维度：**
- Meta.total_interactions（递增 1）

**STORE 步不修改其他 State 维度。**

## 六、衰减触发

STORE 步每次执行后（即在递增完 total_interactions 后）被动触发衰减。

衰减不对本轮写入的 Block 立即生效。衰减应用于所有已有 Block（including 本轮新写入的，从下一轮 starts）。

## 七、Trace 记录

```
TraceEntry(operation="store", status=..., duration_ms=..., summary={blocks_written, total_blocks, eviction, decay})
```
