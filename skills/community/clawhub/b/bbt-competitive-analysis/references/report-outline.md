---
title: Competitive Analysis Report Outline
source: .docs/竞品分析/BUBBLETREE儿童枕市场机会分析报告.pdf
---

# Competitive Analysis Report Outline

This file defines the fixed report structure. The generator must preserve the section order and heading hierarchy.

## Cover Section

- Report title: `{brand_or_project}{category}市场机会分析报告`
- Reporter: default `自动分析任务`
- Analysis date: report generation date
- Data source: product list + reviews + QA + any additional connected metrics

## Executive Summary

Must include:

- one summary paragraph
- a `关键发现` table
- `核心建议` text

The `关键发现` table should keep these default rows:

- 市场机会
- 材质趋势
- 最大痛点
- 竞品短板
- 你们优势

## 第一部分：数据概览

### 1.1 分析样本

Table fields:

- 数据类型
- 数量
- 说明

Suggested rows:

- 竞品样本
- 买家评论
- 买家问答
- 其他指标

### 1.2 样本品牌销售排名

Table fields:

- 排名
- 品牌
- 指标值
- 占比

Notes:

- If sales revenue is unavailable, degrade this section to `商品数排名`.
- The `指标值` header may be replaced with `商品数` or another available metric.

## 第二部分：品牌维度深度分析

### 2.1 核心竞品品牌矩阵

Table fields:

- 品牌
- 指标值
- 占比
- 商品数
- 定位
- 核心功能
- 差异化标签

### 2.2 品牌定位分类

Table fields:

- 定位类型
- 代表品牌
- 核心特点
- 机会分析

### 2.3 各品牌价格带分布

Table fields:

- 品牌
- 主价格带
- 价格策略

Notes:

- If price is unavailable, keep the section and mark it as `未采集价格字段`.

### 2.4 品牌打法总结

Table fields:

- 打法
- 代表品牌
- 你们的应对

### 2.5 竞争空白点

Table fields:

- 空白点
- 机会等级
- 说明

## 第三部分：功能趋势分析

### 3.1 竞品功能词频

Table fields:

- 功能
- 出现次数
- 占比
- 备注

### 3.2 洞察

- Output 3 to 5 short insight bullets.

## 第四部分：价格带分析

Table fields:

- 价格带
- 竞争状况
- 机会评估

Notes:

- If price is unavailable, output placeholder conclusions and data-gap notes.

## 第五部分：用户需求洞察

### 5.1 用户需求排名

Table fields:

- 排序
- 需求
- 频次
- 占比

### 5.2 用户痛点

Table fields:

- 排序
- 痛点
- 频次
- 严重程度

### 5.3 购买决策障碍

Table fields:

- 问题类型
- 频次
- 占比

## 第六部分：BUBBLETREE机会分析

### 6.1 竞争优势

Table fields:

- 你们的优势
- 对应用户需求
- 匹配度

### 6.2 差异化机会

Table fields:

- 差异化维度
- 竞品现状
- 你们机会
- 强度

### 6.3 产品机会

Must include:

- `产品定义建议`
- `SKU建议` 表
- `核心卖点` 列表

`SKU建议` table fields:

- SKU
- 定价
- 目标年龄
- 规格

## 第七部分：行动计划

### 7.1 产品开发

Table fields:

- 阶段
- 行动
- 时间
- 负责人

### 7.2 上市准备

Table fields:

- 阶段
- 行动
- 时间
- 渠道

### 7.3 预期目标

Table fields:

- 指标
- 3个月目标
- 6个月目标

## 第八部分：风险与建议

### 8.1 潜在风险

Table fields:

- 风险
- 概率
- 影响
- 应对

### 8.2 风险控制建议

- Output 3 to 5 short control suggestions.

## Appendix

Must include:

- 分析方法
- 数据来源

## Generation Constraints

- Heading hierarchy must match this template.
- Metric labels in tables may change, but whole sections must not be removed.
- When data is missing, preserve the structure and explain the reason instead of silently omitting sections.
