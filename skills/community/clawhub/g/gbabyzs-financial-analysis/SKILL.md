# Financial Analysis - 财务分析工具

## 功能说明

提供上市公司财务分析功能，包括估值指标、财务健康度评估等。

## 核心功能

### 估值指标
- PE (市盈率)
- PB (市净率)
- PS (市销率)
- PEG (市盈率相对盈利增长比率)

### 盈利能力
- ROE (净资产收益率)
- ROA (总资产收益率)
- 毛利率
- 净利率

### 财务健康度
- 资产负债率
- 流动比率
- 速动比率
- 利息保障倍数

### 估值模型
- DCF (现金流折现)
- 相对估值法
- DDN (股利折现)

## 使用示例

```python
from financial_analysis import calculate_pe, calculate_roe, dcf_valuation

# 计算 PE
pe_data = calculate_pe(stock_code="300308")

# 计算 ROE
roe_data = calculate_roe(stock_code="300308")

# DCF 估值
dcf_result = dcf_valuation(stock_code="300308", growth_rate=0.2, discount_rate=0.1)
```

## 安装依赖

```bash
pip install akshare pandas numpy
```

## 数据源

- AkShare 财务数据
- 东方财富 API

## 注意事项

- 财务数据有季度延迟
- DCF 模型对参数敏感
- 建议结合行业对比
