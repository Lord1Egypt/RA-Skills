---
name: a-stock-portfolio-monitor
description: A股持仓监控助手 - 每日自动持仓报告、止损止盈提醒、实时盈亏跟踪。适合个人投资者管理多只股票持仓。
version: 1.0.0
author: 罗森
---

# A股持仓监控助手

## 功能

- ✅ **持仓实时监控** - 自动获取最新股价，计算盈亏
- ✅ **每日收盘报告** - 生成日终持仓总结
- ✅ **止损止盈提醒** - 自动检测触发条件
- ✅ **多因子选股** - 基于涨幅/量能/估值评分

## 使用方法

### 1. 配置持仓

```python
python scripts/portfolio.py add 600803 --cost 21.76 --qty 1800  # 新奥股份
python scripts/portfolio.py add 600010 --cost 3.30 --qty 15000  # 包钢股份
python scripts/portfolio.py add 600845 --cost 23.92 --qty 3000  # 宝信软件
```

### 2. 查看持仓报告

```python
python scripts/portfolio.py analyze
```

### 3. 运行选股

```python
python scripts/selector.py
```

## 数据源

- 腾讯财经API（实时行情）
- 本地持仓数据存储

## 免责声明

本工具仅供参考，不构成投资建议。投资有风险，入市需谨慎。
