---
name: crypto-content-automation
version: 1.0.0
description: 加密货币自媒体运营自动化 - 热点扫描 + 内容策划 + 一键发布。支持小红书、币安Square等平台。
tags:
  - crypto
  - content
  - automation
  - xiaohongshu
  - social-media
requires:
  env: []
  bins:
    - python3
    - node
---

# Crypto Content Automation Skill

加密货币自媒体运营自动化工具，一句话完成：热点扫描 → 内容策划 → 发布

## 功能

### 1. 热点扫描
运行热点扫描脚本，获取AI/Crypto/AI+Crypto热点

### 2. 内容策划
基于热点生成深度内容策划案，包含：
- 反直觉视角
- 落地操作指南
- 风险提示

### 3. 内容发布
支持发布到：
- 小红书（需要Cookie配置）
- 币安Square（需要Cookie配置）

## 使用方法

### 热点扫描
```bash
python3 scripts/hot_topic_scanner.py
```

### 内容策划
```bash
python3 scripts/content_planning.py
```

### 查看结果
- 热点报告：`logs/hot_topics_YYYYMMDD.json`
- 策划案：`logs/content_planning_YYYYMMDD.md`

## 配置

如需发布到小红书或币安，需要配置对应平台的Cookie。

## 工作流程

1. 用户给出主题/方向
2. 执行热点扫描获取最新热点
3. 生成内容策划案
4. 撰写完整内容
5. 发布到目标平台
