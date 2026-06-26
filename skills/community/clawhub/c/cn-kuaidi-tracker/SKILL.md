---
name: cn-kuaidi-tracker
description: "快递追踪助手。输入快递单号查询物流状态，自动识别快递公司。"
metadata: {"openclaw": {"emoji": "📦"}}
---

# 快递追踪助手

输入单号，查询物流状态。

## 功能
- 输入单号查询物流
- 自动识别快递公司
- 本地追踪列表管理

## 用法
```bash
python3 scripts/express_tracker.py "添加快递 SF1234567890"
python3 scripts/express_tracker.py "查 SF1234567890"
python3 scripts/express_tracker.py "查快递"
```

## 支持快递公司
顺丰、中通、圆通、韵达、申通、极兔、京东、EMS、邮政、德邦

## 数据接口
快递100公开查询接口，无需注册。

## 数据存储
本地JSON文件：`~/.qclaw/skills/cn-express-tracker/data/express.json`
