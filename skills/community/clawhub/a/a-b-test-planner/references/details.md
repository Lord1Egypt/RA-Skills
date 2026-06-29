# a-b-test-planner 详细参考

## 一、样本量计算详解

### 核心公式
```
n = (Zα/2 + Zβ)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₂ - p₁)²

简化版（当p₁≈p₂时）：
n = 16 × p × (1-p) / δ²

其中：
- p₁: 对照组转化率
- p₂: 实验组转化率  
- δ = |p₂ - p₁|: 最小可检测效应(MDE)
- Zα/2: 置信水平Z值（双尾）
- Zβ: 统计功效Z值
```

### Z值速查表
| 置信水平 | α | Zα/2 |
|----------|------|------|
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.960 |
| 99% | 0.01 | 2.576 |

| 统计功效 | β | Zβ |
|----------|------|------|
| 80% | 0.20 | 0.842 |
| 85% | 0.15 | 1.036 |
| 90% | 0.10 | 1.282 |
| 95% | 0.05 | 1.645 |

### 实际计算示例

**场景1：电商购买按钮优化**
```
已知：
- 当前点击率：3%
- 预期提升：3% → 3.6%（提升20%）
- 置信水平：95%
- 统计功效：80%

计算：
p = 0.03, δ = 0.006
n = 16 × 0.03 × 0.97 / 0.006²
n = 16 × 0.0291 / 0.000036
n = 12,933

总样本量 = 2 × 12,933 = 25,866
```

**场景2：注册流程优化**
```
已知：
- 当前注册率：5%
- 最低可检测提升：5% → 5.5%（相对提升10%）
- 置信水平：95%
- 功效：90%

计算：
p = 0.05, δ = 0.005
n = 16 × 0.05 × 0.95 / 0.005²
n = 16 × 0.0475 / 0.000025
n = 30,400

总样本量 = 2 × 30,400 = 60,800
```

---

## 二、常见场景测试设计模板

### 场景1：电商首页改版

```yaml
测试名称：首页新版布局AB测试
测试ID：EXP_2024_001

假设陈述：
- 原假设(H0)：新版首页转化率 ≤ 旧版首页转化率
- 备择假设(H1)：新版首页转化率 > 旧版首页转化率
- 单尾检验，α=0.05

核心指标：
- 主指标：商品点击率（CTR）
- 次指标：加购率、支付转化率、GMV

护栏指标：
- 页面加载时间不增加超过200ms
- 技术错误率 < 0.1%
- 用户满意度评分不下降

流量分配：
- 实验组A（新版）：50%
- 对照组B（旧版）：50%
- 分流单位：user_id（登录用户）
- 分流方式：哈希取模

样本量估算：
- 基线转化率：8%
- MDE：10%（相对提升）
- 计算样本量：39,228/组
- 预估测试周期：14天（日均3,000UV/组）

触发条件：
- 用户：当日首次访问
- 设备：PC/App/H5
- 地域：全量

分流规则：
- 新用户：随机分流
- 老用户：保持一致性
```

### 场景2：App推送文案优化

```yaml
测试名称：推送文案A/B测试
测试ID：PUSH_2024_015

变量设计：
- A组（控制）："您有1张优惠券待使用"
- B组（实验1）："限时24h！您的优惠券即将过期"
- C组（实验2）："【专属福利】点击领取专属优惠券"

关键参数：
- 样本量/组：50,000
- 测试周期：7天
- 分流方式：device_id
- 分流比例：33%/33%/33%

评估指标：
- 主指标：推送打开率
- 次指标：App活跃率、转化率
- 护栏指标：卸载率、退订率

数据埋点：
- push_sent：推送发送
- push_open：推送打开
- app_active：App活跃
- purchase_complete：完成购买
```

---

## 三、统计分析代码

### Python实现

```python
import numpy as np
from scipy import stats

def calculate_sample_size(p1, mde, alpha=0.05, power=0.8):
    """
    计算A/B测试样本量
    
    参数:
        p1: 基线转化率
        mde: 最小可检测效应（绝对值或相对值）
        alpha: 显著性水平
        power: 统计功效
    返回:
        每组所需样本量
    """
    # 计算Z值
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    # 如果mde是相对值，转换为绝对值
    if 0 < mde < 1:  # 可能是相对值
        p2 = p1 * (1 + mde) if mde < 1 else p1 + mde
        if p2 < 1:  # 确认是相对提升
            mde = abs(p2 - p1)
    
    # 计算样本量
    p2 = p1 + mde
    n = ((z_alpha + z_beta)**2 * 
         (p1*(1-p1) + p2*(1-p2))) / mde**2
    
    return int(np.ceil(n))


def ab_test_analysis(n1, conversions1, n2, conversions2):
    """
    A/B测试结果分析
    
    参数:
        n1, n2: 两组样本量
        conversions1, conversions2: 两组转化数
    
    返回:
        统计显著性、置信区间、功效分析
    """
    p1 = conversions1 / n1
    p2 = conversions2 / n2
    
    # Z检验
    p_pool = (conversions1 + conversions2) / (n1 + n2)
    se = np.sqrt(p_pool * (1-p_pool) * (1/n1 + 1/n2))
    z_stat = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # 置信区间
    se_diff = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    ci_lower = (p2 - p1) - 1.96 * se_diff
    ci_upper = (p2 - p1) + 1.96 * se_diff
    
    # 相对提升
    lift = (p2 - p1) / p1 * 100 if p1 > 0 else 0
    
    return {
        'p1': p1, 'p2': p2,
        'lift': f'{lift:.2f}%',
        'z_stat': z_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'ci_95': (ci_lower, ci_upper),
        'ci_95_pct': (f'{ci_lower*100:.2f}%', f'{ci_upper*100:.2f}%')
    }


# 使用示例
if __name__ == '__main__':
    # 计算样本量
    n_per_group = calculate_sample_size(p1=0.05, mde=0.005, alpha=0.05, power=0.8)
    print(f'每组所需样本量: {n_per_group}')
    
    # 分析结果
    result = ab_test_analysis(
        n1=10000, conversions1=500,  # 对照组
        n2=10000, conversions2=580    # 实验组
    )
    print(f'对照组转化率: {result["p1"]:.4f}')
    print(f'实验组转化率: {result["p2"]:.4f}')
    print(f'相对提升: {result["lift"]}')
    print(f'P值: {result["p_value"]:.4f}')
    print(f'95%置信区间: {result["ci_95_pct"]}')
    print(f'统计显著: {result["significant"]}')
```

### R实现

```r
library(pwr)

# 样本量计算
pwr.2p.test(
  h = ES.h(p1 = 0.05, p2 = 0.055),  # 效应量
  sig.level = 0.05,
  power = 0.8,
  alternative = "greater"
)

# 结果分析
prop.test(
  x = c(500, 580),  # 转化数
  n = c(10000, 10000),  # 样本量
  alternative = "greater"
)
```

---

## 四、测试决策树

```
开始测试
    │
    ├─ 是否有足够样本量？
    │   ├─ 否 → 延长测试周期或降低MDE
    │   └─ 是 ↓
    │
    ├─ 测试周期是否满足？
    │   ├─ 否 → 继续等待数据收集
    │   └─ 是 ↓
    │
    ├─ 主指标是否显著提升？(p < 0.05)
    │   ├─ 是 ↓
    │   └─ 否 → 检查次指标/放弃测试
    │
    ├─ 护栏指标是否达标？
    │   ├─ 否 → 排查问题/修改方案
    │   └─ 是 ↓
    │
    └─ 发布实验组！
```

---

## 五、多重比较修正

### Bonferroni 修正
```python
def bonferroni_correction(p_values, alpha=0.05):
    """
    Bonferroni多重比较修正
    适用场景：保守检验，指标较少时
    """
    k = len(p_values)
    adjusted_alpha = alpha / k
    significant = [p < adjusted_alpha for p in p_values]
    return significant, adjusted_alpha
```

### Benjamini-Hochberg 修正
```python
from scipy.stats import false_discovery_control

def bh_correction(p_values, fdr=0.05):
    """
    BH修正，控制假阳性率(FDR)
    适用场景：多个指标同时检验
    """
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    
    # 计算临界值
    critical_values = (np.arange(n) + 1) / n * fdr
    
    # 找到最大k使p[k] <= critical[k]
    valid = sorted_p <= critical_values
    if not valid.any():
        return [False] * n, None
    
    k = np.where(valid)[0][-1]
    threshold = critical_values[k]
    
    significant = [p <= threshold for p in p_values]
    return significant, threshold
```

---

## 六、常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 效果波动大 | 样本量不足/周期太短 | 增加样本/延长周期 |
| 周末效果差异 | 用户行为周期差异 | 至少覆盖1个完整周期 |
| 新旧用户差异 | 用户分层差异 | 分层分析/新老分组测试 |
| 显著性伪象 | 多重检验膨胀 | 修正p值/减少指标 |
| 业务不显著但统计显著 | 提升太小无业务价值 | 提高MDE/评估ROI |

---

## 七、测试Checklist

**上线前检查**：
- [ ] 假设清晰可证伪
- [ ] 样本量已计算
- [ ] 分流策略确定
- [ ] 埋点方案验收
- [ ] 护栏指标定义
- [ ] 最小测试周期确定

**下线后分析**：
- [ ] 数据完整性验证
- [ ] 分流均匀性检验
- [ ] 主指标显著性
- [ ] 护栏指标合规
- [ ] 次指标方向
- [ ] 结论与建议
