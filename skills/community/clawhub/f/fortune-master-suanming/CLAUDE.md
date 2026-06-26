# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# CLAUDE.md - fortune-master-suanming

八字命理专业分析技能。

## 项目概述

fortune-master-suanming 是一个专业的八字/四柱命理分析系统，专注于提供基于传统命理典籍的专业分析。系统整合了《渊海子平》《三命通会》《子平真诠》《滴天髓》《穷通宝鉴》《神峰通考》等经典理论，为用户提供全面细致的八字分析。

## 核心功能

- 日主旺衰分析（得令/得地/得势评分）
- 调候分析（穷通宝鉴）
- 格局分析（真假 + 层次评分）
- 十神配置分析
- 用神选取（调候 + 扶抑）
- 地支藏干详解
- 合冲刑害分析
- 气势流通判断
- 大运流年整合
- 具体年份 8 维度分析

## 项目架构

### 主要文件结构
```
fortune-master-suanming/
├── SKILL.md                     # 主技能说明
├── README.md                    # 项目说明
├── _meta.json                   # 项目元数据
├── CHANGELOG.md                 # 更新日志
├── CLAUDE.md                    # Claude 专用指南
├── references/                  # 29 个八字框架文件
│   ├── bazi-framework.md        # 八字基础框架
│   ├── bazi-classics-framework.md # 八字经典框架
│   ├── bazi-detailed-framework.md # 八字详细框架
│   ├── bazi-xiangfa-framework.md  # 八字象法框架
│   ├── bazi-deep-analysis-guide.md # 八字深度分析指南
│   ├── classic-books-integration.md # 经典著作整合
│   ├── classic-citation-framework.md # 经典引用规范
│   ├── reasoning-explanation-framework.md # 推理说明框架
│   ├── wuxiang-shengke-framework.md # 五行生克刑冲合害
│   ├── dizhi-canggan-framework.md   # 地支藏干详解
│   ├── tiangan-xingchong-framework.md # 天干刑冲克害
│   ├── dayun-liunian-framework.md   # 大运流年详解
│   ├── shensha-framework.md         # 神煞详解
│   ├── liuqin-framework.md          # 六亲关系
│   ├── geju-analysis-framework.md   # 格局分析
│   ├── geju-yingtui-framework.md    # 格局应事
│   ├── comprehensive-analysis-framework.md # 综合分析框架
│   ├── comprehensive-inference-framework.md # 综合推断框架
│   ├── annual-detailed-analysis-v2.md # 年度详细分析（具体年份版）
│   ├── case-studies-framework.md    # 案例库
│   ├── terminology-glossary.md      # 术语词典
│   ├── faq.md                     # 常见问题
│   ├── intake-and-routing.md        # 分流规则
│   ├── safety-and-ethics.md         # 安全伦理
│   ├── output-templates.md          # 输出模板
│   ├── output-templates-v3.md       # v3 输出模板
│   ├── quick-reference.md           # 快速查询表
│   └── xiangfa-analysis-framework.md # 象法分析
```

## 资料完整度分级

系统根据用户提供信息的完整性分为四个级别：

### S 级：高精度素材
- 完整出生信息（年月日时 + 出生地 + 性别）
- 已排好的八字四柱
- 完整命盘截图
- 启动深度精读模式，整合所有分析框架

### A 级：结构化资料
- 出生年月日时（无出生地或性别）
- 双方出生资料用于合盘
- 标准版解读

### B 级：半完整资料
- 出生年月日，没有精确时间/地点
- 星座、属相、年龄段、关系背景
- 轻量版框架，重点讲趋势

### C 级：问题导向，无核心资料
- "帮我算一下"、"看我运势"
- 象征版框架，轻量解读
- 提示用户补充资料

## 分析模块

### 基础分析（8 个模块）
1. 日主旺衰分析 - 得令/得地/得势评分
2. 调候分析 - 穷通宝鉴调候用神
3. 八字格局分析 - 真假 + 层次评分
4. 十神配置分析 - 力量百分比
5. 用神喜神忌神选取 - 调候 + 扶抑
6. 地支藏干详解 - 透干/通根
7. 干支合冲刑害绝分析 - 五合/六合/六冲/相刑/六害
8. 气势流通与清浊判断 - 流通性/清纯度/有情度

### 大运流年（2 个模块）
9. 大运排盘与整合 - 起运 + 大运评分
10. 大运流年整合分析 - 配合判断 + 节点分析

### 具体年份分析（8 维度）
11. 婚姻感情 - 具体哪几年容易结婚/波动
12. 财运 - 具体哪几年赚钱顺利/破财
13. 健康状况 - 具体哪几年身体好/需注意
14. 人际贵人 - 具体哪几年贵人旺/小人多
15. 居住搬迁 - 具体哪几年容易搬迁/稳定
16. 官司是非 - 具体哪年是非多/少
17. 福禄寿数 - 具体哪年福厚/福减
18. 大运流年吉凶 - 具体哪几年上升/压力/节点

### 增强功能（3 个）
19. 经典著作引用 - 八字经典（原文 + 白话 + 应用）
20. 推理说明 - 每个结论说明为什么（规则 + 原局 + 推导）
21. 象法分析 - 干支象/十神象/宫位象/刑冲合害象

## 输出格式

S级深度分析包含15-18个模块的详细报告，包括：
- 四柱排盘表格
- 五行生克深度分析
- 地支藏干详解
- 天干刑冲克害
- 格局分析
- 十神深度解读
- 神煞分析
- 六亲关系
- 日柱深度解读
- 分领域深度解读
- 大运流年详解
- 象法直断
- 开运调理建议
- 点醒的话

## 安全边界

严格遵守以下边界：
- 不可替代医疗、法律、财务、投资专业判断
- 不可恐吓式下结论（如"血光之灾"、"必离婚"等）
- 不可声称能破解诅咒、消灾包成功
- 不可利用玄学操控、威胁、PUA用户

## 使用方式

```
用 fortune-master-suanming 帮我算八字 S 级
我是 1990 年 5 月 15 日上午 10 点出生，男，出生地北京市
```

## 版本

1.0.0

## 分析原则

1. 每个结论都说明为什么（推理过程 + 经典依据）
2. 引用八字经典原文 + 白话解释 + 实际应用
3. 具体年份分析（哪一年 + 具体事件 + 建议）
4. 严格安全边界（不恐吓、不替代专业建议）