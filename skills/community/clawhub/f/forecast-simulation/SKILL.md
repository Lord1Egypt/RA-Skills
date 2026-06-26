---
name: forecast-simulation
description: |
  基于已有数据进行趋势预测、目标缺口分析、What-if 模拟和耗尽/饱和预测。当用户希望了解指标的未来走势、评估目标是否可达、模拟假设场景的影响时，必须使用此 Skill。
  触发场景包括但不限于：用户提到"预测""预估""月底能到多少""能不能完成目标""还差多少""如果XX会怎样""提升10%会怎样""库存还能撑多久""按这个趋势""达标需要多少""推演""模拟""What-if""情景分析""按目前的速度""还需要多久""够不够""能不能达成""离目标还有多远""日均需要多少""按目前进度""趋势外推""预计""估算"，或用户对未来走势、目标可行性、假设场景表达了疑问时，都应使用此 Skill。
  即使用户没有直接说"预测"，只要其意图是了解"未来会怎样"或"如果改变某个条件结果会怎样"，都应触发此 Skill。例如用户说"这个月能卖到 1000 万吗""如果投放加倍呢""照这样下去年底会怎样"，都应触发。
  **触发判定关键**：用户的意图是了解**未来**的事，或模拟**假设**场景。区分方式：
  - "上月销售额多少" → metric-query（看过去）
  - "月底销售额能到多少" → forecast-simulation（看未来）
  - "销售额正常吗" → anomaly-detection（判断现在）
  - "销售额为什么跌了" → metric-attribution（解释过去）
  **与相邻 Skill 的区分**：
  - metric-query / anomaly-detection / metric-attribution 都是看过去和现在
  - forecast-simulation（本 Skill）是看未来
  **重要：本 Skill 基于历史数据做简单数学推算（趋势拟合、公式模拟），不是机器学习预测模型。推算结果应附带前提假设和不确定性说明。**
---

# 预测推演 Skill

## 执行模式

- **强模型**（Claude Opus/Sonnet, GPT-4o/5）：遵循"原则"段落，自行决定实现细节
- **标准模型**（Qwen, DeepSeek, Llama）：严格按"模板"段落执行，使用提供的代码块，不要自行改写

> 如果你不确定自己属于哪个类别，请按"标准模型"模式执行。

## 定位

本 Skill 回答的核心问题是：**"接下来会怎样？"**

它是分析链条中面向未来的一环：

```
metric-query（过去发生了什么）
anomaly-detection（现在正不正常）
metric-attribution（为什么会这样）
forecast-simulation（接下来会怎样）← 本 Skill
```

---

## 四种推演能力

| 类型 | 核心问题 | 典型场景 |
|------|---------|---------|
| **趋势外推** | 按目前趋势，未来值是多少？ | "月底销售额能到多少" |
| **目标缺口** | 能不能完成目标？差多少？ | "离 KPI 还差多远""日均需要多少" |
| **What-if 模拟** | 如果改变某个条件，结果会怎样？ | "客单价提升 10% GMV 会变多少" |
| **耗尽/饱和预测** | 按当前消耗/增长速度，还能撑/到多久？ | "库存还能卖几天""多久能回本" |

---

## 数据获取方式

本 Skill 的所有数据查询均**委派 metric-query Skill 执行**，不直接调用 Gateway API。

需要数据时，向 metric-query Skill 提供查询意图即可，例如：
- "搜索与销售额相关的指标"
- "查询 retail_amt 近30天按天展开的数据"
- "查询本月至今的累计销售额"
- "查询当前库存量"

metric-query Skill 负责 API 认证、请求构建等所有细节。本 Skill 聚焦于拿到数据后的**预测推演逻辑**。

---

## 推演类型一：趋势外推

### 适用场景

用户关心"按目前趋势往后走会怎样"：
- "这个月底销售额能到多少"
- "按这个速度年底库存周转率能改善到多少"
- "照这个趋势下个月会怎样"

### 执行步骤

**Step 1：拉历史数据**

根据预测时间跨度选择合适的历史窗口和粒度：

| 预测目标 | 历史窗口 | 时间粒度 |
|---------|---------|---------|
| 月底（剩余数天） | 近 30 天 | 按天 |
| 下个月 | 近 3-6 个月 | 按月 |
| 季度/年度 | 近 6-12 个月 | 按月 |

**委派 metric-query 查询**：查询 retail_amt 近30天按天展开的数据。

参考查询参数：
```json
{
    "metrics": ["retail_amt"],
    "dimensions": ["metric_time__day"],
    "timeConstraint": "DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -30, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")",
    "orders": [{"metric_time__day": "asc"}]
}
```

**Step 2：拟合趋势**

在本地用 Python 进行趋势拟合：

选择拟合方法：
- **线性回归**：适用于稳定增长/下降趋势，最常用
- **移动平均**：适用于波动较大的数据，用近 N 天均值作为未来预估
- **加权移动平均**：近期数据权重更高，适合趋势有变化的场景

**完整 Python 代码（标准模型直接复制执行）：**

```python
import numpy as np

def forecast_trend(values, remaining_days, method="linear"):
    """
    输入：
      values: list, 历史每日指标值（按时间升序）
      remaining_days: int, 需要预测的天数
      method: str, "linear"（线性回归）/ "moving_avg"（移动平均）/ "weighted_avg"（加权移动平均）
    输出：
      forecast: dict, 包含预测值和置信区间
    """
    n = len(values)
    days = np.arange(1, n + 1)

    if method == "linear":
        # 线性回归
        slope, intercept = np.polyfit(days, values, 1)
        future_days = np.arange(n + 1, n + remaining_days + 1)
        predicted = slope * future_days + intercept
        daily_forecast = float(np.mean(predicted))

    elif method == "moving_avg":
        # 简单移动平均（取最近 7 天均值）
        window = min(7, n)
        daily_forecast = float(np.mean(values[-window:]))
        predicted = [daily_forecast] * remaining_days

    elif method == "weighted_avg":
        # 加权移动平均（近期权重更高）
        window = min(14, n)
        recent = values[-window:]
        weights = np.arange(1, len(recent) + 1, dtype=float)  # 线性递增权重
        weights /= weights.sum()
        daily_forecast = float(np.average(recent, weights=weights))
        predicted = [daily_forecast] * remaining_days

    # 累计预测
    existing_total = sum(values)
    forecast_total = existing_total + sum(predicted)

    # 置信区间（基于近期波动的标准差）
    recent_std = float(np.std(values[-min(7, n):], ddof=1)) if n >= 3 else 0
    margin = recent_std * np.sqrt(remaining_days) * 1.5  # 简化的置信区间

    result = {
        "method": method,
        "daily_forecast": daily_forecast,
        "forecast_total": forecast_total,
        "lower_bound": forecast_total - margin,
        "upper_bound": forecast_total + margin,
        "existing_total": existing_total,
        "remaining_days": remaining_days,
    }

    print(f"预测方法：{method}")
    print(f"  已有累计：{existing_total:,.0f}")
    print(f"  预测日均：{daily_forecast:,.0f}")
    print(f"  月底预估：{forecast_total:,.0f}")
    print(f"  预估区间：{result['lower_bound']:,.0f} ~ {result['upper_bound']:,.0f}")

    return result

# 使用示例：
# result = forecast_trend(daily_values, remaining_days=13, method="linear")
```

**Step 3：输出预测结论**

```
📊 趋势预测：{指标名}

- 本月截至今天累计：{已有值}
- 近 7 天日均：{日均值}
- 按当前趋势，月底预估：{预估值}
- 预估区间（基于近期波动）：{下限} ~ {上限}

⚠️ 前提假设：假设未来 {N} 天延续近期趋势，不考虑大促、节假日等特殊事件。
```

### 重要：不确定性说明

趋势外推必须附带前提假设和不确定性说明，因为：
- 线性外推无法预测突变（大促、政策变化）
- 时间越远，不确定性越大
- 近期趋势可能不代表未来

---

## 推演类型二：目标缺口分析

### 适用场景

用户关心"能不能达标"：
- "这个月能完成 1800 万的目标吗"
- "距离季度 KPI 还差多少"
- "要达标每天需要卖多少"

### 执行步骤

**Step 1：获取当前进度**

**委派 metric-query 查询**：查询本月至今的累计销售额。

参考查询参数：
```json
{
    "metrics": ["mtd_val"],
    "metricDefinitions": {
        "mtd_val": {
            "refMetric": "retail_amt",
            "period": "grain_to_date 0 month of 0 day"
        }
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

**Step 2：计算缺口**

**完整 Python 代码（标准模型直接复制执行）：**

```python
def assess_target_gap(current_total, target, remaining_days, recent_daily_avg):
    """
    输入：
      current_total: float, 当前累计值
      target: float, 目标值
      remaining_days: int, 剩余天数
      recent_daily_avg: float, 近期日均值（如近7天日均）
    输出：
      assessment: dict, 包含缺口和可行性评估
    """
    gap = target - current_total
    completion_rate = current_total / target * 100 if target > 0 else 0
    required_daily = gap / remaining_days if remaining_days > 0 else float('inf')
    feasibility_ratio = required_daily / recent_daily_avg if recent_daily_avg > 0 else float('inf')

    if feasibility_ratio < 1.0:
        assessment = "✅ 按当前节奏可轻松达标"
    elif feasibility_ratio < 1.3:
        assessment = "⚠️ 需保持当前势头，有一定压力"
    else:
        assessment = "🔴 达标难度较大，需要额外措施"

    result = {
        "target": target,
        "current_total": current_total,
        "gap": gap,
        "completion_rate": completion_rate,
        "remaining_days": remaining_days,
        "required_daily": required_daily,
        "recent_daily_avg": recent_daily_avg,
        "feasibility_ratio": feasibility_ratio,
        "assessment": assessment,
    }

    print(f"🎯 目标达成分析：")
    print(f"  目标：{target:,.0f}")
    print(f"  当前进度：{current_total:,.0f}（完成 {completion_rate:.1f}%）")
    print(f"  剩余缺口：{gap:,.0f}")
    print(f"  剩余天数：{remaining_days} 天")
    print(f"  达标需日均：{required_daily:,.0f}")
    print(f"  当前日均：{recent_daily_avg:,.0f}")
    print(f"  需要当前日均的 {feasibility_ratio:.1f} 倍")
    print(f"  评估：{assessment}")

    return result

# 使用示例：
# result = assess_target_gap(8500000, 18000000, 13, 650000)
```

**Step 3：输出分析**

```
🎯 目标达成分析：{指标名}

目标：{目标值}
当前进度：{已有值}（完成 {完成率}%）
剩余缺口：{缺口值}
剩余天数：{N} 天

达标条件：日均需达到 {所需日均}
当前日均：{近期日均}
比值：需要当前日均的 {倍数} 倍

评估：
- {倍数 < 1.0}  → ✅ 按当前节奏可轻松达标
- {1.0 ≤ 倍数 < 1.3} → ⚠️ 需要保持当前势头，有一定压力
- {倍数 ≥ 1.3} → 🔴 达标难度较大，需要额外措施
```

### 目标值的来源

- 用户直接给出（"目标是 1800 万"）→ 直接使用
- 对话中提到过 → 从对话上下文中提取
- 用户没给 → 询问用户，或用去年同期作为参考基线

---

## 推演类型三：What-if 模拟

### 适用场景

用户想模拟"改变某个条件会怎样"：
- "如果客单价提升 10%，GMV 会变多少"
- "如果 UV 翻倍但转化率降一半呢"
- "降价 15% 对销售额的影响"

### 执行步骤

**Step 1：确定因子公式**

What-if 模拟依赖业务因子公式。与 metric-attribution 的因子拆解共享相同的公式知识，但方向相反：

| | metric-attribution | forecast-simulation |
|---|---|---|
| 方向 | 已知结果 → 找原因 | 假设原因 → 算结果 |
| 问法 | "GMV 为什么跌了" | "如果客单价涨 10% GMV 变多少" |
| 输入 | 结果指标的变化 | 因子的假设变化 |
| 输出 | 各因子的贡献度 | 结果指标的预估值 |

常用公式（与 metric-attribution 一致）：

| 复合指标 | 公式 |
|---------|------|
| GMV / 销售额 | UV × 转化率 × 客单价 |
| 销售额 | 购买人数 × 客单价 |
| 利润 | 收入 - 成本 |
| 利润率 | 利润 / 收入 |

**Step 2：获取当前各因子值**

**委派 metric-query 搜索指标**：关键词=UV,转化率,客单价

**委派 metric-query 查询**：查询 visitor_cnt、buyer_cnt、AOV 等因子在上月的值。

参考查询参数：
```json
{
    "metrics": ["visitor_cnt", "buyer_cnt", "AOV"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"
}
```

如果转化率等没有直接指标，metric-query Skill 可用 metricDefinitions + expr 计算。

**Step 3：模拟计算**

```python
# 当前值
uv = 100000
cvr = 0.032
aov = 680
gmv = uv * cvr * aov  # = 2,176,000

# 用户假设：客单价提升 10%
new_aov = aov * 1.10   # = 748
new_gmv = uv * cvr * new_aov  # = 2,393,600

delta = new_gmv - gmv          # = 217,600
delta_pct = delta / gmv        # = 10%
```

**Step 4：输出模拟结果**

```
🔮 What-if 模拟：客单价提升 10%

基础公式：GMV = UV × 转化率 × 客单价

            当前值        模拟值       变化
UV          100,000      100,000      不变
转化率       3.2%         3.2%        不变
客单价       ¥680         ¥748        +10%
─────────────────────────────────────────
GMV         ¥217.6万     ¥239.4万     +10%（+¥21.8万）

⚠️ 前提假设：假设提升客单价不会影响 UV 和转化率。
实际中，提价可能导致转化率下降，净效果可能小于模拟值。
```

### 多因子联动模拟

用户可能想同时改变多个因子（"UV 翻倍但转化率降一半"）：

```python
new_uv = uv * 2.0      # UV 翻倍
new_cvr = cvr * 0.5     # 转化率降一半
new_aov = aov           # 客单价不变
new_gmv = new_uv * new_cvr * new_aov  # 结果不变
```

**注意**：多因子联动时必须在输出中明确所有假设条件，避免用户只记住结论忘了前提。

---

## 推演类型四：耗尽/饱和预测

### 适用场景

用户关心"按当前速度，资源还能支撑多久"：
- "库存还能撑几天"
- "按这个消耗速度预算什么时候花完"
- "按目前增速多久能达到 XX 用户量"

### 执行步骤

**Step 1：获取当前存量和消耗速率**

**委派 metric-query 查询**：查询当前库存量。

参考查询参数：
```json
{
    "metrics": ["inventory_qty"],
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

**委派 metric-query 查询**：查询近 14 天日均消耗量。

参考查询参数：
```json
{
    "metrics": ["daily_consumption"],
    "metricDefinitions": {
        "daily_consumption": {
            "refMetric": "sales_qty",
            "period": "to_date -13 day of 0 day",
            "preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]
        }
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

**Step 2：计算**

```python
current_stock = 12400    # 当前库存
daily_consumption = 580  # 日均消耗

days_remaining = current_stock / daily_consumption  # ≈ 21.4 天
depletion_date = today + timedelta(days=int(days_remaining))
```

**Step 3：输出**

```
📦 库存耗尽预测

当前库存：12,400 件
近 14 天日均消耗：580 件/天
预计可用天数：约 21 天
预计耗尽日期：4 月 8 日前后

⚠️ 如果消耗速度加快（如大促），耗尽会提前。
按近 7 天日均（620 件/天）计算，可用天数缩短至约 20 天。
```

---

## 通用原则

### 前提假设必须透明

每一个推演结果都必须附带前提假设。用户需要知道"这个预测是在什么条件下成立的"，才能判断是否可信。

常见需要声明的前提：
- "假设未来延续近期趋势"
- "假设没有大促、节假日等特殊事件"
- "假设改变 X 不会影响 Y"（What-if 模拟中因子独立性假设）
- "基于近 N 天数据推算"

### 不要给出虚假的精确度

推演结果本身带有不确定性，不要输出过于精确的数字给用户错误的信心。

- ❌ "月底预估销售额为 15,263,847.32 元"
- ✅ "月底预估销售额约 1,520-1,530 万"

### 适时给出区间而非点估计

在趋势外推中，如果近期数据波动较大，给出预估区间比单个点估计更有价值：

```python
# 用近期波动的标准差构建区间
forecast_low = forecast - 1.5 * std
forecast_high = forecast + 1.5 * std
```

### 知道自己的边界

本 Skill 做的是简单的数学推算，不是统计预测模型。对于以下场景应诚实说明局限性：

- 存在明显季节性 → "建议参考去年同期数据辅助判断"
- 即将有大促/节假日 → "近期有特殊事件，纯趋势外推可能失准"
- 预测周期过长（>3个月）→ "长期预测不确定性大，建议定期更新"

---

## 常见错误模式

**❌ 不说前提假设**：给了一个预测数字但没解释"基于什么条件推出来的"。用户无法判断可信度。

**❌ 虚假精度**：推算结果精确到个位数。简单外推不具备这种精度，应当用"约"或给出区间。

**❌ 因子独立性假设不告知**：What-if 模拟中说"客单价提升 10% GMV 增 10%"，但没提"假设转化率不受影响"。实际中提价几乎一定会影响转化率。

**❌ 用过短的历史做长期预测**：拿 7 天数据预测全年走势。历史窗口应与预测跨度匹配。

**❌ 忽略季节性**：用淡季数据外推旺季，或反过来。如果用户的业务有季节性，应提醒用户。

**❌ 拿到的因子公式不对**：What-if 模拟中用了错误的业务公式。因子公式必须与用户确认，或从 metric-attribution 的已有知识中复用。

**❌ 在本 Skill 中做归因**：用户问"如果 XX 会怎样"时顺便分析了"为什么现在 XX 不好"。归因是 metric-attribution 的事，本 Skill 只做"假设→推算"。
