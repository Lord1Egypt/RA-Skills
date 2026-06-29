---
name: "EC Price Monitor Lite"
description: "免费版：多平台电商价格监控，支持淘宝/拼多多基础价格搜索"
version: "1.1.0"
slug: "ec-price-monitor-pro"
tags:
  - ecommerce
  - price-monitor
  - free
trigger:
  - command: "监控价格 [关键词]"
requirements:
  - python3
---

# EC Price Monitor Lite (免费版)

多平台电商价格监控工具，支持手动搜索比价。

## 功能（Lite 版）

- ✅ 淘宝 / 拼多多 价格搜索
- ✅ 手动对比（输入关键词即可）
- ✅ 基础价格报告输出
- ❌ 京东平台（Pro 版支持）
- ❌ 定时自动执行（Pro 版支持）
- ❌ 价差自动推送（Pro 版支持）
- ❌ 价格历史追踪（Pro 版支持）

## 安装

```bash
clawhub skill install ec-price-monitor-pro
```

## 使用方法

```
监控价格 AirPods Pro 2
```

## 升级到 Pro 版

如需完整功能，请安装 Pro 版：

```bash
clawhub skill install ec-price-monitor-pro-plus
```

## 文件结构

```
scripts/
  price_monitor_lite.py    # Lite 版搜索脚本
references/
  config.yaml              # 商品配置
```
