---
name: baidu-hot-real
description: 百度热搜榜实时抓取 - 直接从 top.baidu.com/board 获取真实热榜数据
version: 1.3.0
author: iph0n3
allowed-tools: web_fetch, Bash
---

# 百度热搜榜 - 真实数据版

## 技能概述

此技能直接从百度热搜官网 (`https://top.baidu.com/board`) 抓取实时热榜数据，**不使用模拟数据**。

## 核心功能

| 功能 | 说明 |
|------|------|
| **实时热搜** | 获取当前百度热搜榜 Top 50 |
| **热点标记** | 识别"热"、"新"等标记 |
| **分类标签** | 自动识别热点分类 |
| **多榜单支持** | 热搜/小说/电影/电视剧 |

## 使用方式

### 获取热搜榜

```bash
# 获取 Top 10
python3 scripts/baidu_real.py 10

# 获取 Top 50（默认）
python3 scripts/baidu_real.py

# 获取完整榜单
python3 scripts/baidu_real.py all
```

### 输出格式

```
🔥 百度热搜榜 Top 10 (2026-03-20 11:48)

1. "国家队"出手 房租最高直降 50% 🔥
2. "我熟这片草原 让我上！" 🔥
3. 春分"分"的是什么？
4. 印度新任驻华大使取了中国名字 🆕
5. 女儿弥留之际妈妈偷偷来看捂嘴忍泪 🆕
...
```

## 数据来源

- **唯一数据源**：https://top.baidu.com/board
- **更新频率**：实时（百度官方更新）
- **数据真实性**：✅ 100% 真实

## 与 baidu-hot-cn 的区别

| 特性 | baidu-hot-cn | baidu-hot-real |
|------|--------------|----------------|
| 数据源 | 百度 API（可能不可用） | 百度热搜官网 |
| 数据真实性 | ⚠️ API 不可用时返回模拟数据 | ✅ 始终真实 |
| 依赖 | Python requests | Python + web_fetch |
| 推荐度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 注意事项

- 需要网络连接访问百度
- 访问频繁可能被限流（建议间隔≥1 分钟）
- 数据格式可能随百度官网更新而变化

## 输出字段

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | int | 排名（1-50） |
| title | string | 热点标题 |
| mark | string | 标记（热/新/无） |
| link | string | 搜索链接 |
| category | string | 分类（自动识别） |
