# 01_failure_analysis — 失败分析器规格

**层级：L3（治理/演化/反馈系统）**
**输入源：** Trace pipeline + L2 degradation history
**权限：** 只读 Trace、只读 L2 信号——**无直接修改当前运行状态的权限**

---

## 一、职责

失败分析器是一个**历史报告生成器**。

它定期（每 N 轮迭代，N=建议周期为 5-10 轮）扫描 Trace pipeline 的最近记录，生成失败模式报告。

**失败分析器不能修改任何正在运行的组件。** 它产生的报告只作为 L3 反馈控制器的输入。

## 二、分析的维度

### 2.1 失败频率分析

| 指标 | 计算方式 | 输出 |
|------|---------|------|
| 总失败率 | failed Trace 数 / 总 Trace 数 | 百分比 |
| 各步失败率 | 按 operation 分组 | observe/cognize/decide/speak/store/reflect 各自的失败率 |
| 连续失败轮数 | 连续迭代中到少一个 step failed | max(cur_streak), avg streak length |

### 2.2 失败模式检测

```
对于每个失败 TraceEntry，提取其 error code：
  对相同 error code 做 Clustering（按时间窗口分组）
  输出：error_code → {count, time_range, avg_duration_ms, possible_cause}
  对应 01_runtime_spec/08_error_codes_response.md 的错误码表
```

### 2.3 降级效率分析

```
比较降级前后的指标变化：
  - 进入降级前的最后 5 轮 vs 降级期间的 5 轮的 State 震荡频率
  - 降级级别越深，State 震荡率是否下降
  - REFUGE 模式的恢复时间（从进入到退出）
  
  输出：degradation_efficiency = 震荡率下降 / 降级级别深度
```

## 三、FailureReport 结构

```
FailureReport = {
  analysis_period: (int, int),  # (from_iteration, to_iteration)
  total_iterations: int,
  total_traces: int,
  failure_analysis: {
    overall_failure_rate: float,          # [0.0, 1.0]
    per_step_failure_rate: dict,          # {step_name: rate}
    consecutive_failure_max: int,
    consecutive_failure_avg: float,
  },
  pattern_analysis: list[{
    error_code: str,
    count: int,
    time_window: (int, int),
    avg_duration_ms: float,
    possible_cause: str,                # 基于 Trace 的上一步/上一步的上下游推断
    recommended_action: str,
  }],
  degradation_analysis: {
    triggered_count: int,
    avg_recovery_time: int,              # 降级到恢复的迭代轮数
    efficiency: float,                   # [0.0, 1.0]
    recommendation: str,
  },
  timestamp: float,
}
```

## 四、冷隔离

```
失败分析器强制执行冷隔离：
  - 不提供对 State 的写访问
  - 不提供对 Block Store 的写访问
  - 不提供对 L1 runtime reducer 状态的直接访问
  - 不调用外部推理引擎
  
  失败分析器的结果只写入两个地方：
    1. Trace pipeline（作为分析器自己的 Trace entry）
    2. 写入 feedback_controller（下一轮输入）
```

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 反馈控制器的决策逻辑 | 07_feedback_runtime_controller |
| Trace 的存储实现 | 实现层 |
| 分析周期 N 的具体值 | L3 配置 |
| possible_cause 的推理规则 | L3 实现细节 |
