# 偏差驱动感知调度

## 核心思想

Agent不需要固定间隔轮询环境。应该像生物一样：**平静时少感知，变化时多感知，异常时立即感知。**

## 调度逻辑

```python
def compute_urgency(current_state, previous_state, time_since_last):
    urgency = 0
    if time_since_last > 3600: urgency += 1      # 基础频率
    if state_transition(current_state, previous_state): urgency += 5
    if anomaly_detected(current_state): urgency += 3
    if random() < 0.05: urgency += 1              # 随机探索
    return urgency

def should_perceive(urgency, threshold=3):
    return urgency >= threshold
```

## 状态转换检测

语义层面的变化，不是简单阈值：

- 时间转换：dawn→day, day→dusk, dusk→night
- 天气转换：clear→cloudy, dry→rain
- 活动转换：quiet→active, active→quiet

## 异常检测

基于历史基线的统计异常：

- 声音异常：RMS > 基线10x
- 亮度异常：偏离同时段均值2σ
- 时间异常：不该活跃的时段出现活动

## 实测数据

| 调度策略 | 感知次数/天 | 有价值比例 | 同质化率 |
|----------|-------------|------------|----------|
| 固定每小时 | 24 | 15% | 42% |
| 偏差驱动 | 16 | 35% | 38% |
| 偏差驱动+转换点优先 | 18 | 40% | 36% |

偏差驱动减少33%感知调用，有价值比例提升133%。

## 踩坑

### urgency初始值设为2
转换点urgency=2 < threshold=3，所有转换点被跳过。违反"转换点偏好0.85"。修正为5后恢复。

教训：**参数选择不能靠直觉，要跟偏好系统对齐验证**。

### 感知跳过率46%
系统过保守。权衡：宁可多感知（成本可控）也不要漏感知（信息不可逆）。

### 深夜异常误报
凌晨2-4点的声音异常几乎都是噪音。加入时段权重后深夜urgency打折。
