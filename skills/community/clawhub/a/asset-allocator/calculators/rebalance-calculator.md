# 再平衡计算器

> 计算再平衡调整金额

---

## 核心公式

### 偏离度计算
```
偏离度 = |当前比例 - 目标比例|
```

### 调整阈值
```
偏离度 > 5% → 需要调整
```

### 调整金额计算
```
调整金额 = 总资产 × (当前比例 - 目标比例)
```

**正数**：卖出  
**负数**：买入

---

## 计算示例

### 示例 1：年度再平衡

**目标配置**：
- 股票：60%
- 债券：40%

**当前配置**（1 年后）：
- 股票：70%（上涨）
- 债券：30%

**总资产**：100 万

**计算**：
```
股票偏离度 = |70% - 60%| = 10% > 5% → 需要调整

股票调整金额 = 100 万 × (70% - 60%) = 10 万
→ 卖出 10 万股票

债券调整金额 = 100 万 × (30% - 40%) = -10 万
→ 买入 10 万债券
```

**操作**：
- 卖出 10 万股票
- 买入 10 万债券

---

### 示例 2：多资产再平衡

**目标配置**：
- 国内股票：40%
- 国际股票：20%
- 债券：30%
- 现金：5%
- 另类：5%

**当前配置**：
- 国内股票：45%（+5%）
- 国际股票：18%（-2%）
- 债券：28%（-2%）
- 现金：5%（0%）
- 另类：4%（-1%）

**总资产**：100 万

**计算**：
```
国内股票：100 万 × (45% - 40%) = +5 万 → 卖出 5 万
国际股票：100 万 × (18% - 20%) = -2 万 → 买入 2 万
债券：100 万 × (28% - 30%) = -2 万 → 买入 2 万
另类：100 万 × (4% - 5%) = -1 万 → 买入 1 万

合计：卖出 5 万，买入 5 万（平衡）
```

---

## Python 计算脚本

```python
def calculate_rebalance(target_allocation, current_allocation, total_assets):
    """
    计算再平衡调整
    
    Args:
        target_allocation: dict, 目标配置 {'stocks': 0.6, 'bonds': 0.4}
        current_allocation: dict, 当前配置
        total_assets: float, 总资产
    
    Returns:
        list: 调整操作列表
    """
    adjustments = []
    
    for asset_class in target_allocation:
        target = target_allocation[asset_class]
        current = current_allocation.get(asset_class, 0)
        
        deviation = current - target
        amount = total_assets * deviation
        
        if abs(deviation) > 0.05:  # 5% 阈值
            action = '卖出' if amount > 0 else '买入'
            adjustments.append({
                'asset': asset_class,
                'action': action,
                'amount': abs(amount),
                'deviation': deviation * 100
            })
    
    return adjustments


# 使用示例
target = {'stocks': 0.6, 'bonds': 0.4}
current = {'stocks': 0.7, 'bonds': 0.3}
assets = 1000000

adjustments = calculate_rebalance(target, current, assets)
for adj in adjustments:
    print(f"{adj['asset']}: {adj['action']} {adj['amount']:,.0f}元 (偏离{adj['deviation']:.1f}%)")
```

---

## Excel 公式

### 偏离度计算
```excel
=ABS(当前比例单元格 - 目标比例单元格)
```

### 调整金额计算
```excel
=总资产单元格 * (当前比例单元格 - 目标比例单元格)
```

### 条件格式（突出显示>5%）
```excel
=ABS(当前比例单元格 - 目标比例单元格) > 0.05
```

---

## 再平衡策略

### 策略 1：定期再平衡
- **频率**：每年 1 次（建议年初或生日）
- **优点**：简单规律，易执行
- **缺点**：可能错过最佳时机

### 策略 2：阈值再平衡
- **触发**：偏离>5%
- **优点**：及时纠正
- **缺点**：可能频繁交易

### 策略 3：混合再平衡（推荐）
- **频率**：每季度检查
- **触发**：偏离>5%
- **优点**：平衡灵活性和纪律

---

## 注意事项

1. **税收考虑**：卖出盈利资产可能产生资本利得税
2. **交易成本**：频繁调整增加交易费用
3. **心理因素**：卖出上涨资产可能不舒服
4. **新资金利用**：用新投入资金调整，减少卖出

---

*再平衡是强制低买高卖的纪律工具。*
