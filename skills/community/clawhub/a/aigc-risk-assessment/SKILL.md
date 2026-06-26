# Risk Assessment - 风险评估工具

## 功能说明

提供投资组合风险评估和仓位管理建议。

## 核心功能

### 风险指标
- VaR (风险价值)
- CVaR (条件风险价值)
- 波动率
- Beta 系数
- 夏普比率

### 压力测试
- 历史情景模拟
- 极端市场测试
- 相关性断裂测试

### 仓位管理
- 凯利公式
- 风险平价
- 最大仓位建议

## 使用示例

```python
from risk_assessment import calculate_var, position_suggestion

# 计算 VaR
var_result = calculate_var(stock_code="300308", confidence=0.95)

# 仓位建议
position = position_suggestion(
    total_capital=1000000,
    risk_tolerance=0.02,
    stock_price=534.80,
    stop_loss=0.10
)
```

## 安装依赖

```bash
pip install akshare pandas numpy scipy
```
