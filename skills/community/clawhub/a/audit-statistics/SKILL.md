# audit-statistics

> 统计学方法在审计实践中的应用指南。帮助审计人员在实际审计项目中选择合适的统计方法、执行分析、解读结果。

---

## 使用场景

当审计项目涉及以下需求时使用本技能：

- 审计抽样方案设计
- 数据异常检测与风险识别
- 实质性分析程序
- 总体金额推断
- 趋势分析与预测

---

## 一、抽样方法速查

### 1. 随机抽样（Simple Random Sampling）
```
每个样本被选中的概率相等
适用：样本量较小、总体较为同质
优点：最基础的抽样方法，结果可直接推断总体
缺点：样本量要求较大才能保证精度
```

### 2. 分层抽样（Stratified Sampling）
```
将总体按某一特征分层（金额区间/业务类型/风险等级）
每层独立抽样，层内可随机或PPS
适用：总体内部差异大，如按账龄或金额分层
优点：提高样本代表性，减少方差
缺点：需要明确的分层变量
```

### 3. 货币单元抽样 MUS（Monetary Unit Sampling）
```
以"元"为抽样单元，金额越大被抽中概率越高
适用：应收账款、应付账款、存货等账面价值较大科目
优点：自然聚焦高风险大额项目
缺点：零余额项目不会被抽中；不适合低价值总体
```

### 4. 属性抽样（Attribute Sampling）
```
测试内部控制是否存在/有效（符合=1，不符合=0）
适用：内控测试样本量确定
公式：n = (Z² × p × (1-p)) / E²
Z = 置信系数（95%→1.96），p = 预期偏差率，E = 可容忍偏差率
```

### 5. 变量抽样（Variable Sampling）
```
推断总体金额错报范围
常用方法：
- 估计均值法（temporal mean estimation）
- 差异估计法（difference estimation）
- 比率估计法（ratio estimation）
适用：存货、固定资产等需要推断真实价值的科目
```

### 6. PPS抽样（Probability Proportional to Size）
```
按项目金额占总体金额的比例确定抽样权重
与MUS类似，但记录抽样而非货币单元
适用：大额项目优先的实质性测试
```

---

## 二、数据分析技术

### Benford 定律
```
数字首位分布规律（自然产生的数据）
首位数字 d出现概率：P(d) = log₁₀(1 + 1/d)

检测步骤：
1. 提取数据首位数字
2. 统计实际分布频率
3. 与理论值比较（卡方检验/K-S检验）
4. 偏差过大→可能存在数据造假或人为修饰

适合检验：销售金额、费用报销、采购订单、发票号
```

### 离群值检测
```
1. 3σ原则：超出均值±3个标准差 → 离群点
2. IQR四分位距：< Q1-1.5×IQR 或 > Q3+1.5×IQR → 离群点
3. Z-score：|Z| > 2.5 或 3 → 离群点
4. 箱线图可视化

适用：大额异常交易、疑似截值（round-number）数据
```

### 相关性 & 回归
```
目的：发现科目间不合理的逻辑关系
举例：
- 收入增长率 vs 应收账款增长率（正常应相近）
- 水电费 vs 生产量（应有正相关）
- 运费 vs 销售额（应有正相关）

审计应用：构建期望值模型，解释不了的差异→进一步追查
```

---

## 三、分析性复核步骤

```
Step 1: 确定分析目标
  → 识别可能存在错报的领域

Step 2: 建立预期值
  → 行业基准 / 上期数据 / 预算数据 / 运营逻辑

Step 3: 计算实际值与预期值的差异
  → 差异金额 = |实际 - 预期|
  → 差异率 = 差异 / 预期

Step 4: 统计显著性判断
  → 差异率 > 可容忍差异率 → 需追查
  → F检验/t检验判断差异是否显著

Step 5: 记录分析结论
  → 差异可解释（正常经营原因）→ 风险低
  → 差异无法解释 → 扩大测试范围
```

---

## 四、实质性测试中的统计应用

### 截止测试（Cut-off Testing）
```
检查结账日前后N天的交易
统计方法：按日期分布检验是否有"人为调整"迹象
（如：12月31日集中确认收入、12月31日后大量退货）
```

### 期后事项检查
```
统计检查结账日后2个月内的大额调整凭证
异常值检测：如果存在某类调整集中发生 → 关注管理层估计变更
```

---

## 五、Python 实现示例

```python
import pandas as pd
import numpy as np
from scipy import stats

# Benford定律检验
def benford_test(data, col):
    observed = data[col].dropna().astype(str).str[0].astype(int)
    observed = observed[observed.between(1, 9)]
    observed_counts = observed.value_counts().sort_index()
    expected = [np.log10(1 + 1/d) for d in range(1, 10)]
    chi2, p = stats.chisquare(observed_counts.values, f_exp=[e*len(observed) for e in expected])
    return chi2, p

# 离群值检测（IQR）
def detect_outliers_iqr(series, k=1.5):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return series[(series < lower) | (series > upper)]

# 分层抽样
def stratified_sample(df, stratify_col, sample_size, weight_col=None):
    strata = df.groupby(stratify_col)
    if weight_col:
        # PPS within each stratum
        sampled = strata.apply(lambda x: x.sample(n=min(len(x), max(1, int(sample_size * x[weight_col].sum() / df[weight_col].sum()))), random_state=42))
    else:
        sampled = strata.apply(lambda x: x.sample(frac=sample_size/len(df), random_state=42))
    return sampled.reset_index(drop=True)
```

---

## 六、抽样方案设计checklist

```
□ 明确审计目标（内控测试 OR 实质性测试）
□ 定义总体范围（科目/期间/业务线）
□ 确定抽样单元
□ 选择抽样方法（MUS / 分层 / 属性等）
□ 计算样本量
□ 随机选号（随机数表或Excel RAND）
□ 执行抽样
□ 评价样本结果（偏差率 / 错报金额）
□ 推断总体结论
□ 记录抽样程序，留存文件
```

---

## 相关标准

- ISA 530：Audit Sampling（审计抽样）
- ISA 520：Analytical Procedures（分析性复核）
- PCAOB AS2315：Audit Sampling
