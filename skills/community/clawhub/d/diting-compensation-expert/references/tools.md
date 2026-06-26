# 薪酬增强工具

> 标准化工具：CSV 模板、Python 计算代码、数据缺失处理策略。

---

## 24 字段薪酬 CSV 模板

用于标准化薪酬数据采集和分析：

```csv
员工ID,姓名,部门,岗位,岗位族,职级/等级,入职日期,司龄(月),
性别,年龄,学历,工作地点,用工性质,劳动合同类型,
基本工资(月),岗位津贴(月),绩效基数(月),加班基数(月),
年度固定薪酬(年),目标年度总薪酬(年),上年度实际总薪酬(年),
最近一次调薪日期,最近一次调薪幅度(%),绩效等级
```

**字段说明**：
| 字段 | 用途 | 必填 |
|------|------|------|
| 员工ID | 唯一标识 | ✅ |
| 岗位 | 对标市场基础 | ✅ |
| 岗位族 | 分族对标 | ✅ |
| 职级/等级 | 等级分析 | ✅ |
| 司龄(月) | 司龄公平性 | ✅ |
| 性别 | 性别公平性 | 推荐 |
| 基本工资(月) | 固定薪酬分析 | ✅ |
| 年度固定薪酬(年) | 年度总固定 | ✅ |
| 目标年度总薪酬(年) | 含绩效总包 | ✅ |
| 绩效等级 | 调薪矩阵输入 | 推荐 |
| 最近一次调薪幅度(%) | 调薪趋势 | 推荐 |

---

## Python 计算工具

### 分位值计算

```python
def calculate_percentile(values, percentile):
    """计算指定分位值 (percentile: 0-100)"""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0: return None
    if n == 1: return sorted_vals[0]
    rank = (percentile / 100.0) * (n - 1)
    lower = int(rank)
    upper = lower + 1
    weight = rank - lower
    if upper >= n: return sorted_vals[-1]
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight
```

### 核心指标计算

```python
def compa_ratio(internal_salary, market_median):
    """Compa-Ratio = 实际薪酬 / 市场中位值"""
    if market_median == 0: return None
    return internal_salary / market_median

def range_penetration(salary, grade_min, grade_max):
    """压缩比 = (实际薪酬 - 等级最小值) / (等级最大值 - 等级最小值)"""
    if grade_max == grade_min: return None
    return (salary - grade_min) / (grade_max - grade_min)

def band_spread(grade_min, grade_max):
    """带宽 = (最大值 - 最小值) / 最小值 × 100%"""
    if grade_min == 0: return None
    return (grade_max - grade_min) / grade_min * 100

def overlap(low_max, high_min, high_max):
    """重叠度 = (低等级最大值 - 高等级最小值) / (高等级最大值 - 高等级最小值) × 100%"""
    if high_max == high_min: return None
    return (low_max - high_min) / (high_max - high_min) * 100
```

### 使用示例

```python
market_salaries = [15000, 18000, 20000, 22000, 25000, 28000, 30000, 32000, 35000, 40000]

P25 = calculate_percentile(market_salaries, 25)  # ~19,250
P50 = calculate_percentile(market_salaries, 50)  # ~26,500
P75 = calculate_percentile(market_salaries, 75)  # ~31,250
P90 = calculate_percentile(market_salaries, 90)  # ~36,500

CR = compa_ratio(20000, P50)  # 0.75 → 偏低
```

---

## 数据缺失处理策略

| 缺失类型 | 处理方案 | 标注要求 |
|----------|---------|---------|
| 市场数据 | 搜索最新行业报告 → 招聘平台交叉验证 → 通用估算 | 标注来源/年份/置信度降低 |
| 内部薪酬 | 请用户提供样本 → 外部推算 → 说明假设条件 | 标注"基于假设推算" |
| 绩效数据 | 退化为 CR 驱动方案 / 假设全员达标 | 说明局限性 |
| 岗位评估 | 使用市场常见岗位映射 | 需企业自行校准 |
| 福利数据 | 使用市场标准福利包估算 | 仅分析现金薪酬 |
