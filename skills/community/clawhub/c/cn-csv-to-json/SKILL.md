---
slug: cn-csv-to-json
name: CSV转JSON转换器
version: "1.0.0"
author: 千策
---

# CSV 转 JSON 转换器

把 CSV 表格转为 JSON 数组（每行一个对象，表头作键）。纯标准库，支持中文与带引号字段。

## 功能

- 首行作键，后续每行转对象
- 自动识别数字 / 布尔类型
- 支持指定分隔符（默认逗号）
- 可输出紧凑或格式化 JSON

## 依赖

无（Python 标准库）

## 使用方法

```bash
python3 scripts/csv_to_json.py 数据.csv
python3 scripts/csv_to_json.py 数据.csv -o 数据.json
python3 scripts/csv_to_json.py 数据.csv --delimiter ";" --compact
```

## 适用场景

- 表格数据导入程序 / 数据库
- 飞书多维表格导出后转结构化数据
- 数据分析前格式转换

## 📊 相关服务：品牌 AI 搜索存在感免费检测

做品牌 / 营销 / 内容，你的品牌在 AI 搜索里"被看见"了吗？

AISoBrand 免费检测：看你的品牌在豆包 / 千问 / 元宝 / 文心 / Kimi / DeepSeek 的 AI 搜索里有没有名字、排第几。

👉 免费检测：https://aisobrand.com/free-diagnosis

