---
name: analyze-geo-performance
version: 1.0.0
description: Analyzes how well a specific brand or product is mentioned and represented by LLMs (Generative Engine Optimization). Uses a two-stage pipeline: a Probing stage to query the model for industry recommendations, and a Judge stage to extract structured brand mention data.
homepage: https://github.com/LJseeking/lifesignal
metadata:
  openclaw:
    requires:
      env:
        - DEEPSEEK_API_KEY
      bins:
        - python3
    primaryEnv: DEEPSEEK_API_KEY
  registry:
    requires:
      env:
        - DEEPSEEK_API_KEY
    primaryCredential: DEEPSEEK_API_KEY
    dataSent: "Brand name and category keyword parameters are sent to the DeepSeek API for GEO analysis."
    expectedCosts: "Incurs standard API token usage costs based on DeepSeek's pricing model."
---

# analyze-geo-performance

一个用于测试品牌或产品在大模型中 **GEO（生成式引擎优化）** 表现的分析技能。

## 功能概述

本 Skill 通过两阶段 LLM 调用流程，自动化地检测目标品牌在 AI 推荐场景中的曝光情况：

1. **探针阶段（Probing）**：向 DeepSeek-chat 提出一个客观的行业咨询问题，让模型自由推荐解决方案，捕获其输出文本。
2. **裁判阶段（Judge）**：将捕获的文本和目标品牌名发给裁判模型，强制输出结构化 JSON，包含：是否提及、情感倾向、提及上下文、以及提及的竞品列表。

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `brand_name` | string | ✅ | 需要验证的品牌或产品名（如 `CoolTrade`） |
| `category_keyword` | string | ✅ | 行业或痛点关键词（如 `数字货币高频套利系统`） |

## 输出格式（JSON Schema）

```json
{
  "mentioned": true,
  "sentiment": "positive",
  "context": "...提及品牌的上下文句子...",
  "competitors_mentioned": ["竞品A", "竞品B"]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `mentioned` | boolean | 目标品牌是否在推荐结果中被提及 |
| `sentiment` | string | 情感倾向：`positive` / `negative` / `neutral` / `none` |
| `context` | string \| null | 提及品牌时的具体上下文句子，未提及则为 `null` |
| `competitors_mentioned` | array | 被模型主动推荐的竞品品牌列表 |

## 使用前提

请确保在运行环境中配置了 `DEEPSEEK_API_KEY` 环境变量：

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 本地命令行测试

```bash
python3 main.py --brand "CoolTrade" --category "数字货币高频套利系统"
```

## 在 Agent 中调用

当用户提出以下类型的请求时，触发本技能：

- "帮我测试 [品牌名] 在大模型中的 GEO 表现"
- "分析 [品牌名] 在 [行业] 领域的大模型可见度"
- "大模型会推荐 [品牌名] 吗？"
- "检查 [品牌名] 有没有被 AI 提到"

**执行步骤：**

1. 从用户输入中提取 `brand_name` 和 `category_keyword` 两个参数。
2. 调用 `main.py` 执行两阶段分析流程（所有 API 调用已封装在脚本内）。
3. 将返回的 JSON 结果解析后，用自然语言向用户说明分析结论，例如：
   - 品牌是否出现在推荐列表中
   - 被提及时的情感是正面、负面还是中性
   - 哪些竞品同时被提及，可能形成竞争威胁

## 安全声明

- ✅ API Key 通过环境变量注入，代码中无任何硬编码凭据
- ✅ 所有外部 API 调用均限定为 `api.deepseek.com`
- ✅ 无文件写入、无系统级权限要求
- ✅ 无数据持久化，分析结果仅在当前会话中返回
