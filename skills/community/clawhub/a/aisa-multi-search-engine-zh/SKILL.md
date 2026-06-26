---
name: aisa-multi-search-engine-zh
description: "通过一个 AISA skill 统一执行网页搜索、学术搜索、Tavily 搜索与抽取、智能搜索和类 Perplexity 深度研究。触发条件：当用户需要网页研究、学术检索、URL 抽取或多源证据汇总时使用。"
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# AISA 多源搜索引擎

## 何时使用

- 通过一个 AISA skill 统一执行网页搜索、学术搜索、Tavily 搜索与抽取、智能搜索和类 Perplexity 深度研究。触发条件：当用户需要网页研究、学术检索、URL 抽取或多源证据汇总时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 通过一个 AISA API Key 和一个 Python 客户端统一封装七种搜索模式。
- 覆盖结构化网页搜索、学术搜索、智能混合搜索、Tavily 搜索与抽取、Perplexity 深度研究以及多源综合。
- 适合研究、尽调、市场扫描和证据收集场景。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/search_client.py
```

## 示例请求

- 用多源研究比较 2026 年发布的 agent 框架。
- 检索 2024 年以来关于多模态推理的学术论文。
- 抽取一组 URL 的正文并总结重合结论。

## 说明

- 在 ClawHub 场景下，内置 Python 客户端是主要运行入口。
