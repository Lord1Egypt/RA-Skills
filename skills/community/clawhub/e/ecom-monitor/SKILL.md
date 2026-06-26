---
name: ecom-monitor
description: 电商数据分析助手 - 导入和管理商品价格数据，生成竞品分析报表，设置价格/库存预警。适用于竞品价格追踪、库存管理、销售报表生成。
---

# Ecom Monitor - 电商数据分析助手

## 核心功能

本技能提供电商数据管理和竞品分析能力：

1. **价格管理** - 导入和管理商品价格数据，追踪历史变化
2. **库存管理** - 记录库存状态，设置缺货/补货预警
3. **报表生成** - 自动生成价格对比表、趋势分析图
4. **竞品分析** - 多店铺数据对比，定价建议
5. **预警通知** - 价格异常/库存变化时发送提醒

## 适用场景

- 管理竞品价格数据（淘宝/京东/亚马逊等）
- 追踪 SKU 库存变化
- 生成价格报表和趋势分析
- 分析竞品定价策略
- 发现市场机会

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 导入价格数据

```bash
python3 scripts/import_prices.py --input products.csv --output data/prices.json
```

### 3. 生成价格报表

```bash
python3 scripts/generate_report.py --input data/prices.json --output report.html
```

### 4. 设置价格预警

```bash
python3 scripts/send_alert.py --config config/alerts.json --test
```

### 5. 配置定时任务

```bash
python3 scripts/setup_cron.py --install --interval 60
```

## 配置说明

### 基础配置 (config/config.json)

```json
{
  "monitor_interval": 3600,
  "output_dir": "data",
  "alert_channels": ["email", "wechat"]
}
```

### 预警配置 (config/alerts.json)

```json
{
  "price_alerts": [
    {
      "product_id": "123456",
      "condition": "price_drop",
      "threshold": 10
    }
  ],
  "stock_alerts": [
    {
      "product_id": "123456",
      "condition": "low_stock",
      "threshold": 50
    }
  ]
}
```

## 脚本说明

### scripts/import_prices.py
导入商品价格数据，支持 CSV/JSON 格式

### scripts/price_history.py
管理历史价格数据，生成趋势分析

### scripts/generate_report.py
生成可视化价格报表（HTML）

### scripts/generate_chart_report.py
生成带交互式图表的趋势报表

### scripts/check_stock.py
检查和管理库存状态

### scripts/send_alert.py
发送价格/库存预警通知

### scripts/setup_cron.py
配置定时任务（自动化监控）

### scripts/competitor_analysis.py
竞品分析引擎，定价建议

### scripts/product_recommender.py
选品推荐引擎，发现潜力商品

## 数据目录结构

```
ecom-monitor/
├── data/
│   ├── prices.json          # 价格数据
│   ├── history.json         # 历史数据
│   └── reports/             # 生成的报表
├── config/
│   ├── config.json          # 主配置
│   ├── alerts.json          # 预警配置
│   └── products.csv         # 商品列表
└── logs/
    └── monitor.log          # 运行日志
```

## 注意事项

1. **数据安全** - 本地存储数据，不上传第三方
2. **隐私保护** - 仅处理用户提供的数据
3. **合规使用** - 遵守相关平台数据使用政策

## 扩展开发

添加新数据源：

1. 在 `scripts/` 创建新的数据导入脚本
2. 统一数据格式到标准 JSON 格式
3. 更新配置支持新平台

---

_版本：1.0.0 | 最后更新：2026-03-13_
