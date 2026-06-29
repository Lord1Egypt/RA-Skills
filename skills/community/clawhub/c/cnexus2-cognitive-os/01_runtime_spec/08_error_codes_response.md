# 08_error_codes_response — 错误码与响应规范

**层级：L1（执行层规格）**

---

## 一、错误信号格式

当系统内部发生错误时，产生一个标准化的错误信号：

```
ErrorSignal = {
  code: str,        # 错误码（见下面的错误码表）
  message: str,     # 可读错误描述
  source: str,      # 产生错误的组件（step/module 名称）
  iteration: int,   # 产生错误的迭代号
  timestamp: int,   # unix timestamp
  severity: float,  # [0.0, 1.0] 严重程度
  trace: str        # 可选，debug 用trace（不在 API 响应中暴露）
}
```

## 二、错误码表

| 错误码 | 含义 | 严重度 | 所属步 |
|-------|------|--------|--------|
| OBSERVE_EMPTY | 空输入 | 0.1 | OBSERVE |
| OBSERVE_TIMEOUT | 观测超时 | 0.4 | OBSERVE |
| COGNIZE_RECALL_FAIL | recall 失败 | 0.3 | COGNIZE |
| COGNIZE_STATE_STALE | State 过期 | 0.5 | COGNIZE |
| DECIDE_IDENTITY_DEGRADED | 身份一致性低 | 0.7 | DECIDE |
| DECIDE_NO_STRATEGY | 无有效策略可执行 | 0.6 | DECIDE |
| SPEAK_INFERENCE_FAIL | 推理引擎调用失败 | 0.5 | SPEAK |
| SPEAK_DEGRADED_FALLBACK | 降级 fallback 被使用 | 0.3 | SPEAK |
| STORE_WRITE_FAIL | Block 写入失败 | 0.4 | STORE |
| STORE_OVERFLOW | Block 数超过上限 | 0.6 | STORE |
| REFLECT_SKIPPED | REFLECT 被跳过 | 0.1 | REFLECT |
| BOOT_CONFIG_MISSING | 启动配置文件缺失 | 0.9 | 系统级 |
| BOOT_MODEL_UNAVAILABLE | 推理模型不可用 | 0.8 | 系统级 |
| RUNTIME_LOOP_BREAK | 循环意外中断 | 0.9 | 系统级 |

## 三、错误的传播

错误信号的传播路径：

```
产生错误 → 错误信号 → 当前 step reducer（可处理或传递）
          → 传递给 L2 drift_monitor
          → L2 决定是否降级
```

单个 reducer 如果无法处理错误，将其原样传递给 L2。L2 不决断的情况下，系统继续执行下一步。

## 四、API 错误响应映射

| 错误码 | HTTP 场景 | API 响应格式 |
|-------|----------|-------------|
| RUNTIME_LOOP_BREAK | 系统未启动 | `{ok: false, error: "not_ready"}` |
| BOOT_CONFIG_MISSING | 启动失败 | `{ok: false, error: "boot_failed"}` |
| STORE_OVERFLOW | memory 存储满 | `{ok: true, data: {response: "...", warning: "memory_full"}}` |
| 其他运行时错误 | 单步失败不影响响应 | 正常返回，data 中包含 warning |
