---
name: ai-model-comparison
version: 1.0.0
description: AI 模型对比指南 - 深度对比主流模型，帮你选最合适的。适合：选型困难、成本优化。
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins: []
---

# AI 模型对比指南

主流模型深度对比，选最合适的。

## 快速选择

| 需求 | 推荐模型 | 理由 |
|------|----------|------|
| 日常对话 | DeepSeek V3 | 便宜、中文好 |
| 编程辅助 | Claude Sonnet | 代码能力强 |
| 长文档分析 | GPT-4-Turbo | 128K 上下文 |
| 免费使用 | GLM-4 | 每月 100 万 tokens |
| 推理任务 | DeepSeek R1 | 推理能力强 |
| 多模态 | GPT-4o | 图片+文字 |

## 价格对比

### 输入价格（¥/百万 tokens）

| 模型 | 价格 |
|------|------|
| DeepSeek V3 | ¥0.27 |
| GLM-4 | ¥0.1（免费额度内）|
| Claude Haiku | ¥0.7 |
| GPT-4o-mini | ¥1.75 |
| DeepSeek R1 | ¥1.35 |
| Claude Sonnet | ¥21 |
| GPT-4o | ¥18 |
| Claude Opus | ¥35 |

### 输出价格（¥/百万 tokens）

| 模型 | 价格 |
|------|------|
| DeepSeek V3 | ¥1.08 |
| GLM-4 | ¥0.1（免费额度内）|
| Claude Haiku | ¥3.5 |
| GPT-4o-mini | ¥10.5 |
| DeepSeek R1 | ¥5.4 |
| Claude Sonnet | ¥105 |
| GPT-4o | ¥108 |
| Claude Opus | ¥175 |

**结论：DeepSeek 最便宜，GLM 免费额度最大**

## 性能对比

### 编程能力

| 模型 | 评分 | 特点 |
|------|------|------|
| Claude Sonnet | ⭐⭐⭐⭐⭐ | 代码质量高，解释清晰 |
| GPT-4o | ⭐⭐⭐⭐⭐ | 综合能力强 |
| DeepSeek V3 | ⭐⭐⭐⭐ | 性价比高 |
| GLM-4 | ⭐⭐⭐⭐ | 中文代码好 |

### 中文能力

| 模型 | 评分 | 特点 |
|------|------|------|
| DeepSeek V3 | ⭐⭐⭐⭐⭐ | 国产，中文优秀 |
| GLM-4 | ⭐⭐⭐⭐⭐ | 智谱，中文优秀 |
| Claude | ⭐⭐⭐⭐ | 翻译感 |
| GPT-4o | ⭐⭐⭐⭐ | 英文原生 |

### 推理能力

| 模型 | 评分 | 特点 |
|------|------|------|
| DeepSeek R1 | ⭐⭐⭐⭐⭐ | 推理专精 |
| Claude Opus | ⭐⭐⭐⭐⭐ | 综合推理强 |
| GPT-4o | ⭐⭐⭐⭐⭐ | 综合能力强 |
| DeepSeek V3 | ⭐⭐⭐⭐ | 性价比高 |

### 长文本

| 模型 | 上下文 | 特点 |
|------|--------|------|
| GPT-4-Turbo | 128K | 支持 |
| Claude | 200K | 支持 |
| GLM-4-Long | 128K | 支持 |
| DeepSeek | 64K | 支持 |

## 免费额度对比

| 模型 | 免费额度 | 条件 |
|------|----------|------|
| GLM-4 | 100 万 tokens/月 | 新用户永久 |
| DeepSeek V3 | 10 次/天 | 注册即有 |
| Claude | $5 注册送 | 新用户 |
| GPT-4o | $5 注册送 | 新用户 |

**结论：GLM 免费额度最大**

## 场景推荐

### 个人日常

```
主模型：DeepSeek V3（便宜）
备用：GLM-4（免费额度）
```

**月成本**：¥0-10

### 编程开发

```
主模型：Claude Sonnet（代码质量高）
简单任务：DeepSeek V3（便宜）
```

**月成本**：¥50-200

### 内容创作

```
主模型：DeepSeek V3（便宜、中文好）
审核：Claude（高质量）}
```

**月成本**：¥10-50

### 企业应用

```
主模型：GPT-4o（稳定）
降级：DeepSeek V3（省钱）
```

**月成本**：¥500-5000

## 省钱策略

### 分层使用

```yaml
models:
  simple: "deepseek-chat"      # ¥0.27/百万
  normal: "glm-4"              # 免费（额度内）
  complex: "gpt-4o-mini"       # ¥1.75/百万
  critical: "claude-sonnet"    # ¥21/百万（关键任务）
```

### 自动降级

```yaml
fallback:
  - claude-sonnet
  - gpt-4o-mini
  - deepseek-chat
  - glm-4
```

### 缓存策略

```yaml
cache:
  enabled: true
  ttl: 86400  # 24 小时
  # 节省 30-50% 成本
```

## 需要帮助？

- 模型选型：¥99
- 成本优化：¥299
- 企业方案：¥999

联系：微信 yang1002378395 或 Telegram @yangster151

---
创建：2026-03-14
