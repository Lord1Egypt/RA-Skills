---
name: ai-article-detector
description: AI Article Detector - Analyze article links and score AI writing probability (0-100). 100 means 100% likely AI-generated.
---

# AI Article Detector

检测文章是否由 AI 生成，输出 0-100 的分数。

## 用途

分析任何网页文章，判断其是否由 AI 生成。基于 8 个独立维度的统计特征分析。

## 快速开始

```bash
node ai-article-detector.js "https://example.com/article"
```

## 工作原理

### 8 维度评分

1. **词汇多样性** (15%) - Type-Token Ratio
2. **句子变化** (15%) - 句子长度系数
3. **段落规律性** (12%) - 段落长度统一度
4. **AI 模板词** (18%) - 转折词频率 ⭐ 最可靠
5. **文本熵** (10%) - Shannon Entropy
6. **情感强度** (10%) - 极端词汇比例
7. **被动语态** (12%) - 被动表达占比
8. **个性化标记** (8%) - 表情符号使用

### 分数解释

- 80-100: 极高概率是 AI
- 60-79: 较高概率是 AI
- 40-59: 中等概率是 AI
- 20-39: 较低概率是 AI
- 0-19: 极低概率是 AI（人类风格）

## 特性

- ✅ 多维度分析
- ✅ 本地分析（隐私保护）
- ✅ 秒级响应
- ✅ 详细分数报告
