---
created: 2026-04-10
updated: 2026-04-10
sources:
  - "sources/attention-is-all-you-need.pdf"
tags:
  - "AI/ML"
  - "架构"
  - "NLP"
status: "active"
---

# Transformer

一种完全基于注意力机制的序列转换架构，取代了 RNN/CNN 成为现代 NLP 和生成式 AI 的基础。——[[NLP 架构演进]]

## 核心要点

- **注意力即一切**：完全用 [[Self-Attention]] 替代循环和卷积
- **并行计算**：相比 RNN 的顺序处理，可完全并行化
- **长距离依赖**：直接建模任意位置之间的关系
- **可扩展性**：是 [[GPT]]、[[BERT]] 等后续模型的基础

## 架构组成

### Encoder-Decoder 结构

原始 Transformer 采用编码器-解码器设计：
- **Encoder**：6 层相同层，每层 = [[Multi-Head Attention]] + 前馈网络
- **Decoder**：6 层相同层，带掩码注意力防止看到未来信息

### 关键组件

| 组件 | 作用 |
|-----|-----|
| [[Self-Attention]] | 计算序列中每个位置与其他所有位置的关联 |
| [[Multi-Head Attention]] | 并行执行多组注意力，捕获不同子空间信息 |
| [[Positional Encoding]] | 注入位置信息（因为注意力本身是无序的） |
| [[Layer Normalization]] | 稳定训练，加速收敛 |
| [[Residual Connection]] | 缓解梯度消失，支持深层网络 |

## 性能特点

- **训练速度**：在 8 块 P100 上，小模型训练 12 小时，大模型 3.5 天
- **翻译质量**：WMT 2014 英德翻译 BLEU 28.4，超越所有现有模型
- **泛化能力**：成功迁移到其他任务（摘要、问答等）

## 影响与衍生

Transformer 架构催生了整个模型家族：

- **Encoder-only**：[[BERT]]、[[RoBERTa]] —— 理解任务
- **Decoder-only**：[[GPT]] 系列、[[LLaMA]] —— 生成任务
- **Encoder-Decoder**：[[T5]]、[[BART]] —— 翻译和摘要

## 相关页面

- [[Self-Attention]] — 核心机制详解
- [[Multi-Head Attention]] — 多头注意力实现
- [[Positional Encoding]] — 位置编码方法
- [[GPT]] — Decoder-only 的后续发展
- [[BERT]] — Encoder-only 的代表
- [[NLP 架构演进]] — RNN → Transformer → ?

## 来源

- [Attention Is All You Need](../sources/attention-is-all-you-need.pdf) (Vaswani et al., 2017)

## 变更日志

- 2026-04-10: 初始创建，从论文中提取核心要点
