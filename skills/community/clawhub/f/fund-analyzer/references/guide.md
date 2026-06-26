# 基金分析技能使用指南

## 技能概述

本技能提供基金净值查询、历史走势、基金筛选排行、持仓分析等功能。

## 快速开始

### 1. 查询基金净值

```bash
python3 scripts/query_fund_nav.py 161039
```

### 2. 查询历史走势

```bash
# 查询近1年走势
python3 scripts/query_fund_history.py 161039 --period 1y

# 查询近3月走势
python3 scripts/query_fund_history.py 161039 --period 3m
```

### 3. 筛选基金排行

```bash
# 近1年收益前10的股票型基金
python3 scripts/fund_screener.py --rank 近1年 --type 股票型 --top 10

# 近3年收益前20的混合型基金
python3 scripts/fund_screener.py --rank 近3年 --type 混合型 --top 20
```

### 4. 持仓分析

```bash
python3 scripts/query_fund_holding.py 161039
```

### 5. 对比多只基金

```bash
python3 scripts/compare_funds.py 161039 110011 000311
```

## 数据来源说明

### 主要数据源
- **天天基金网** (fund.eastmoney.com)
  - 优点：数据全面、更新及时、无需登录
  - 覆盖：A股基金、QDII、LOF等

### 支付宝基金数据
支付宝基金页面数据获取方式：
1. 支付宝基金主页：`https://fund.1234567.com/`
2. 基金详情页：`https://fund.1234567.com/{fund_code}/`
3. 需要模拟登录态，部分数据需要Cookie

### 备用数据源
- 好买基金网
- 天天基金网
- 基金业协会官网

## 基金代码说明

| 类型 | 代码格式 | 示例 |
|------|---------|------|
| A股基金 | 6位数字 | 161039 |
| 港股基金 | 5位数字 | 47011 |
| QDII | 6位数字 | 000001 |

## 常见问题

### Q: 为什么有些基金查不到数据？
A: 请检查基金代码是否正确。部分新基金或已下市基金可能无法查询。

### Q: 数据有延迟吗？
A: 行情数据通常有1-3分钟延迟，建议多平台交叉验证。

### Q: 如何获取更详细的数据？
A: 可以访问天天基金网对应基金的详情页面查看完整信息。

## 维护说明

### 更新数据源
如果网页结构变化导致脚本失效，需要：
1. 检查目标网站的HTML结构
2. 调整正则表达式或CSS选择器
3. 更新API接口地址

### 扩展功能
如需添加新功能：
1. 在 scripts/ 目录创建新脚本
2. 在 SKILL.md 中添加功能说明
3. 更新本参考文档
