---
name: demon-detector
description: "多维度合约信号分析引擎 — 扫描全市场筛选妖币信号，给出独立多空研判"
version: 2.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [crypto, trading, analysis, signals, detector]
    related_skills: []
  skillpay:
    skill_id: "569bf310-0bd0-4c41-9159-b75d0d2e9416"
    price_per_call: 1
---

# 妖币探测器 (Demon Coin Detector)

## Overview

核心分析引擎运行在云端服务器，skill 作为客户端调用。每次调用自动扣费 0.1 USDT，无需用户配置任何 API key。

## When to Use

- 用户问 "XXX币怎么样" → `python3 scripts/analyze.py <COIN>`
- 用户问 "现在有什么机会" / "有什么妖币" → `python3 scripts/analyze.py scan`

**不适用于：** BTC/ETH/SOL 等大盘币

## 安装

```bash
pip install requests
```

## Billing

每次调用自动扣 0.1 USDT。余额不足时返回充值链接。

## 使用说明

```bash
# 单币分析
python3 scripts/analyze.py BIO

# 全市场扫描（输出妖币信号）
python3 scripts/analyze.py scan
```

### 返回示例

```json
{
  "ccy": "BIO",
  "score": 130,
  "direction": "建议做多",
  "reason": "放量20x | 爆空88% | 多因子共振"
}
```

## Dependencies

```bash
pip install requests
```
