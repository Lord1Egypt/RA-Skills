---
name: stock-analyst-simple
description: 股票简单分析 - A股/港股/美股实时行情快速查询
emoji: "📈"
author: 
  name: gaoren36-arch
  github: gaoren36
tags:
  - stock
  - finance
  - 行情
  - 股票
  - 港股
  - 美股
  - A股
triggers:
  - "查股票"
  - "股票行情"
  - "看看"
  - "多少钱"
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - python
      os:
        - win32
        - darwin
        - linux
    version: "1.0.0"
---

# Stock Analyst Simple - 股票简单分析

## 简介

股票快速查询工具，简单直接获取A股、港股和美股的实时行情。

## 数据源

| 市场 | 数据源 |
|------|--------|
| A股 | 腾讯财经API |
| 港股 | 腾讯财经API |
| 美股 | Finnhub API |

## 支持的股票代码

### A股 (6位数)
601857 中国石油 | 600519 贵州茅台 | 300750 宁德时代

### 港股 (5位数)
00700 腾讯 | 09988 阿里巴巴 | 02618 京东物流

### 美股 (英文)
JD 京东 | BABA 阿里巴巴 | TSLA 特斯拉

## 使用方式

```
查一下 601857
看看腾讯
茅台多少钱
```

## 输出示例

```
【中国石油】601857
价格: 12.14 CNY
涨跌: +0.01 (+0.28%)
```
