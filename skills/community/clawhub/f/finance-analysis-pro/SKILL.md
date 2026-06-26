---
name: finance-analysis-pro
description: 专业财务分析助手 - 财报分析、DCF估值、风险评估、行业对比、投资决策支持
metadata:
  openclaw:
    emoji: "💰"
    requires:
      pip: ["tushare>=1.2.89", "pandas>=1.5", "numpy>=1.24"]
    install:
      - id: pip-install
        kind: pip
        packages: ["tushare>=1.2.89", "pandas>=1.5", "numpy>=1.24"]
        label: "安装依赖"
keywords:
  - 财务分析
  - 股票估值
  - DCF模型
  - 风险评估
  - 投资决策
  - 财报解读
---

# 专业财务分析助手

## 功能特性

- 基础财报分析（自动重试机制）
- 财务指标计算
- DCF 估值模型
- 相对估值法
- 风险评估报告
- 行业对比分析
- 自动投资建议
- 定期分析推送
- **智能错误处理**
- **多数据源支持**

## 快速开始

```bash
pip install tushare pandas numpy
export TUSHARE_TOKEN="your_token"
```

## 财报分析

```python
import tushare as ts
import pandas as pd

pro = ts.pro_api()

def analyze_stock(ts_code):
    """基础财报分析"""
    # 获取财务指标
    indicator = pro.fina_indicator(ts_code=ts_code, period='20231231')
    
    if indicator.empty:
        return "未找到数据"
    
    data = indicator.iloc[0]
    
    return {
        'ROE': data.get('roe', 'N/A'),
        '净利率': data.get('netprofit_margin', 'N/A'),
        '毛利率': data.get('grossprofit_margin', 'N/A'),
        '资产负债率': data.get('debt_to_assets', 'N/A'),
        '营收增长': data.get('or_yoy', 'N/A'),
        '利润增长': data.get('netprofit_yoy', 'N/A')
    }

# 使用示例
result = analyze_stock('000001.SZ')
print(result)
```

### 财务指标解读

```python
def interpret_indicators(indicators):
    """解读财务指标"""
    interpretations = []
    
    # ROE 解读
    roe = indicators.get('ROE', 0)
    if roe > 20:
        interpretations.append("ROE优秀 (>20%)")
    elif roe > 15:
        interpretations.append("ROE良好 (15-20%)")
    elif roe > 10:
        interpretations.append("ROE一般 (10-15%)")
    else:
        interpretations.append("ROE偏低 (<10%)")
    
    # 净利率解读
    net_margin = indicators.get('净利率', 0)
    if net_margin > 30:
        interpretations.append("净利率优秀 (>30%)")
    elif net_margin > 15:
        interpretations.append("净利率良好 (15-30%)")
    elif net_margin > 5:
        interpretations.append("净利率一般 (5-15%)")
    else:
        interpretations.append("净利率偏低 (<5%)")
    
    # 增长率解读
    growth = indicators.get('营收增长', 0)
    if growth > 30:
        interpretations.append("高增长 (>30%)")
    elif growth > 15:
        interpretations.append("稳健增长 (15-30%)")
    elif growth > 0:
        interpretations.append("低增长 (0-15%)")
    else:
        interpretations.append("负增长")
    
    return interpretations
```

## DCF 估值模型

```python
def dcf_valuation(ts_code, assumptions=None):
    """DCF 估值模型"""
    if assumptions is None:
        assumptions = {
            'growth_rate': 0.15,  # 未来5年增长率
            'terminal_growth': 0.03,  # 永续增长率
            'wacc': 0.10,  # 加权平均资本成本
            'margin_of_safety': 0.25  # 安全边际
        }
    
    # 获取历史数据
    income = pro.income(ts_code=ts_code)
    if income.empty:
        return None
    
    latest = income.iloc[0]
    base_revenue = latest.get('revenue', 0)
    net_profit = latest.get('net_profit', 0)
    net_margin = net_profit / base_revenue if base_revenue > 0 else 0
    
    # 预测未来5年
    cash_flows = []
    for year in range(1, 6):
        revenue = base_revenue * (1 + assumptions['growth_rate']) ** year
        profit = revenue * net_margin
        cash_flows.append(profit)
    
    # 终值
    terminal_value = cash_flows[-1] * (1 + assumptions['terminal_growth']) / \
                    (assumptions['wacc'] - assumptions['terminal_growth'])
    
    # 折现
    pv_cash_flows = sum(cf / (1 + assumptions['wacc']) ** i 
                       for i, cf in enumerate(cash_flows, 1))
    pv_terminal = terminal_value / (1 + assumptions['wacc']) ** 5
    
    total_value = pv_cash_flows + pv_terminal
    
    # 应用安全边际
    safe_value = total_value * (1 - assumptions['margin_of_safety'])
    
    return {
        '公司价值': total_value,
        '安全价值': safe_value,
        '现金流预测': cash_flows,
        '终值': terminal_value,
        '假设条件': assumptions
    }
```

### 相对估值法

```python
def relative_valuation(ts_code, industry_pe=15, industry_pb=1.5):
    """相对估值法"""
    # 获取基本面数据
    basic = pro.stock_basic(ts_code=ts_code, fields='ts_code,name,industry,market_cap')
    indicator = pro.fina_indicator(ts_code=ts_code, period='20231231')
    income = pro.income(ts_code=ts_code, period='20231231')
    
    if basic.empty or indicator.empty or income.empty:
        return None
    
    data = indicator.iloc[0]
    income_data = income.iloc[0]
    
    # 计算 EPS
    shares = data.get('total_share', 0)
    eps = income_data.get('net_profit', 0) / shares if shares > 0 else 0
    
    # 计算 BPS
    bvps = data.get('bvps', 0)
    
    # PE 估值
    pe_value = eps * industry_pe
    
    # PB 估值
    pb_value = bvps * industry_pb
    
    return {
        'EPS': eps,
        'BPS': bvps,
        'PE估值': pe_value,
        'PB估值': pb_value,
        '综合估值': (pe_value + pb_value) / 2,
        '行业PE': industry_pe,
        '行业PB': industry_pb
    }
```

### 风险评估报告

```python
def risk_assessment(ts_code):
    """风险评估"""
    indicator = pro.fina_indicator(ts_code=ts_code, period='20231231')
    balance = pro.balancesheet(ts_code=ts_code, period='20231231')
    
    if indicator.empty or balance.empty:
        return None
    
    ind = indicator.iloc[0]
    bal = balance.iloc[0]
    
    risks = []
    score = 100
    
    # 偿债能力
    debt_ratio = ind.get('debt_to_assets', 0)
    if debt_ratio > 70:
        risks.append("⚠️ 资产负债率过高 (>70%)")
        score -= 20
    elif debt_ratio > 50:
        risks.append("⚡ 资产负债率偏高 (50-70%)")
        score -= 10
    
    # 盈利能力
    roe = ind.get('roe', 0)
    if roe < 5:
        risks.append("⚠️ ROE过低 (<5%)")
        score -= 15
    elif roe < 10:
        risks.append("⚡ ROE偏低 (5-10%)")
        score -= 5
    
    # 成长性
    growth = ind.get('or_yoy', 0)
    if growth < 0:
        risks.append("⚠️ 营收负增长")
        score -= 15
    elif growth < 10:
        risks.append("⚡ 增长放缓 (<10%)")
        score -= 5
    
    # 现金流
    ocf = ind.get('ocf_to_profit', 0)
    if ocf < 0.8:
        risks.append("⚠️ 现金流质量差")
        score -= 10
    
    # 评级
    if score >= 80:
        rating = "⭐⭐⭐⭐⭐ 低风险"
    elif score >= 60:
        rating = "⭐⭐⭐⭐ 中低风险"
    elif score >= 40:
        rating = "⭐⭐⭐ 中等风险"
    elif score >= 20:
        rating = "⭐⭐ 中高风险"
    else:
        rating = "⭐ 高风险"
    
    return {
        '风险评分': score,
        '风险评级': rating,
        '风险提示': risks,
        '关键指标': {
            '资产负债率': debt_ratio,
            'ROE': roe,
            '营收增长': growth,
            '现金流/利润': ocf
        }
    }
```

### 行业对比分析

```python
def industry_analysis(ts_code, top_n=10):
    """行业对比分析"""
    # 获取公司信息
    stock = pro.stock_basic(ts_code=ts_code, fields='ts_code,name,industry')
    if stock.empty:
        return None
    
    industry = stock.iloc[0]['industry']
    
    # 获取同行业公司
    peers = pro.stock_basic(industry=industry, list_status='L',
                           fields='ts_code,name,market_cap')
    
    if peers.empty:
        return None
    
    peers = peers.sort_values('market_cap', ascending=False).head(top_n)
    
    results = []
    for _, peer in peers.iterrows():
        try:
            ind = pro.fina_indicator(ts_code=peer['ts_code'], period='20231231')
            if not ind.empty:
                results.append({
                    '代码': peer['ts_code'],
                    '名称': peer['name'],
                    '市值(亿)': peer['market_cap'] / 100000000,
                    'ROE': ind.iloc[0].get('roe', None),
                    '净利率': ind.iloc[0].get('netprofit_margin', None),
                    '营收增长': ind.iloc[0].get('or_yoy', None)
                })
        except:
            continue
    
    df = pd.DataFrame(results)
    
    # 计算行业平均
    avg_metrics = {
        '行业平均ROE': df['ROE'].mean(),
        '行业平均净利率': df['净利率'].mean(),
        '行业平均增长': df['营收增长'].mean()
    }
    
    return {
        '行业': industry,
        '对比公司': df,
        '行业平均': avg_metrics
    }
```

## 使用示例

```bash
# 财报分析
python scripts/finance_analysis.py analyze --stock 000001.SZ

# DCF 估值
python scripts/finance_analysis.py valuation --stock 600519.SH --method dcf

# 风险评估
python scripts/finance_analysis.py risk --stock 000001.SZ

# 行业对比
python scripts/finance_analysis.py industry --stock 600519.SH
```

## 风险提示

1. 估值模型基于假设，实际结果可能差异较大
2. 财务数据存在滞后性
3. 投资有风险，决策需谨慎
