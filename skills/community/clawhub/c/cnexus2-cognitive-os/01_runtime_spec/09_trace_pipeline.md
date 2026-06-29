# 09_trace_pipeline — 溯源轨迹管道规范

**层级：L1（执行层规格）**
**依据：** L0 core_essence/04_data_model_essence.md §四

---

## 一、Trace 在循环中的位置

每个 step reducer 在完成执行后，将本次操作的摘要写入 Trace：

```
已执行 OBSERVE → 写入 one Trace entry
已执行 COGNIZE → 写入 one Trace entry
...
```

Trace 不是 state，不是 memory——它是系统执行历史的不可变记录。

## 二、Trace Entry 格式

```
TraceEntry = {
  trace_id: str,        # UUID 或 hash
  timestamp: float,     # unix 秒
  iteration: int,       # 所属迭代
  operation: str,       # "observe" / "cognize" / "decide" / "speak" / "store" / "reflect"
  status: str,          # "success" / "failed" / "degraded"
  component: str,       # 组件名称（如 "cognize_reducer"）
  duration_ms: int,     # 步耗时，单位毫秒
  error: str,           # 如果 status 不是 success，记录错误码
}
```

## 三、附加摘要

每个 reducer 可以向 Trace 附加一个可选的 summary 字段：

```
TraceEntry.summary = {}   # 可选字典，各 reducer 可以附加非标准化的摘要信息
```

summary 不用于一致性证明，仅用于人工调试。summary 的内容格式不由本文件约束。

## 四、Trace 的保留

Trace 是 append-only。写后不可修改。

Trace 保留上限为 1,000 条。超出后从最旧的开始覆盖。

1,000 条 Trace 维持至少 100 次完整循环的审计能力。

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| summary 的具体内容 | 各 reducer |
| trace 的物理存储（内存 / 文件） | 实现层 |
| 1,000 条上限的调整 | L2 配置 |
