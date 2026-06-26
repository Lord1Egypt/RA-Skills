---
name: amazon-push-score
description: >-
  Use when user needs Amazon push score calculation and optimization strategy.
  Use when generating A9 algorithm optimization plans for Amazon listings.
  Use when evaluating Amazon listing performance metrics and traffic tier classification.
  Use when user mentions "推送分", "流量池", "A9算法", "亚马逊权重", "CTR优化", "CVR优化".
homepage: https://cloudtrip.ai
license: MIT-0
version: "1.0.6"
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、推送算法、流量池分级"
    - name: instructions
      tokens: 5000
      loaded: trigger
      description: "推送分计算、4维权重体系、流量池分级、优化策略建议"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "优化案例、行业基准值、A9算法参考"
  resource_paths:
    - references/*.md
metadata:
  openclaw:
    homepage: https://cloudtrip.ai
    requires:
      bins: []
    emoji: "📊"
    version: "1.0.6"
    author: "云旅智能体超市"
    category: "ecommerce-ai"
    tags: ["amazon", "push-score", "a9", "ctr", "cvr", "流量池", "推送分", "A9算法", "权重优化", "运营策略"]
pricing:
  - name: Starter
    price: 49
    currency: CNY
    period: month
    features:
      - 推送分计算
      - 流量池等级判定
      - 基础优化建议
  - name: Professional
    price: 199
    currency: CNY
    period: month
    features:
      - 全维度推送分诊断
      - 4维权重优化方案
      - 行业基准值参考
      - A9算法策略建议
  - name: Enterprise
    price: 999
    currency: CNY
    period: month
    features:
      - 私有部署
      - 行业定制
      - 批量SKU分析
      - 专属运营顾问
triggers:
  - "推送分"
  - "流量池"
  - "A9算法"
  - "亚马逊权重"
  - "CTR优化"
  - "CVR优化"
  - "运营等级"
  - "流量分级"
  - "亚马逊排名"
  - "推送算法"
---

# 📊 亚马逊推送分计算与流量池分级系统

## ⚡ 极简输入，全量输出

用户只需提供4个指标，系统自动输出推送权重分、运营等级和优化建议：

```
输入格式：CTR(%) + CVR(%) + 7天增速 + 账号健康分(0-1)
示例：1.2 + 14 + 4 + 0.96
```

收到输入后，自动计算推送分，判定流量池等级，生成针对性优化方案。

## 简介

基于亚马逊A9算法权重分析的推送评分系统。通过4维权重体系（CTR×0.2 + CVR×0.4 + 7天增速×0.2 + 账号健康分×0.2），量化评估Listing的流量获取能力，并生成对应等级的优化策略。

**核心能力：推送分计算 | 流量池分级 | 优化策略生成 | A9算法参考**

## 效果数据

| 指标 | 传统经验判断 | 推送分量化评估 |
|------|------------|--------------|
| 诊断周期 | 2-4周试错 | 5秒出分 |
| 优化方向 | 靠感觉 | 4维精准定位 |
| 流量提升 | 不确定 | 维度优化后显著提升 |
| 运营效率 | 人均管理20SKU | 人均管理100+SKU |

## 四维权重体系

### 权重分配
| 维度 | 权重 | 含义 | 行业优秀值 |
|------|------|------|-----------|
| CTR（点击率） | 20% | 用户匹配度 | 2-3% |
| CVR（转化率） | 40% | 产品信任度（最高权重） | 10-15% |
| 7天增速 | 20% | 用户认可度 | 3-5 |
| 账号健康分 | 20% | 合规安全度 | 0.95+ |

### 为什么CVR权重最高？
亚马逊A9算法的核心逻辑：**让用户买到最满意的产品**。转化率直接反映产品-需求匹配度，是算法最看重的信号。CVR每提升1%，推送分上浮约2.7分。

## 流量池分级

| 等级 | 分数区间 | 流量特征 | 运营建议 |
|------|---------|---------|---------|
| A+ 黄金流量池 | ≥90分 | 优先曝光，首页展示 | 维持优势，扩品复制 |
| A 优质流量池 | 75-89分 | 稳定加权，Top3展示 | 提升CVR冲击A+ |
| B 基础流量池 | 60-74分 | 正常分发，需优化 | 重点突破短板维度 |
| C 低权重池 | <60分 | 流量受限，需关注 | 全面诊断，逐项修复 |

## 推送分计算公式

```
推送分 = (归一化CTR × 0.20 + 归一化CVR × 0.40 + 归一化增速 × 0.20 + 健康分 × 0.20) × 100

归一化CTR = min(CTR / 3, 1)      # 基准：行业优秀CTR≈3%
归一化CVR = min(CVR / 15, 1)     # 基准：行业优秀CVR≈15%
归一化增速 = min(增速 / 5, 1)    # 基准：健康增速≈5
归一化健康分 = 账号健康分（0-1）
```

### 计算示例
输入：CTR=1.2%, CVR=14%, 7天增速=4, 健康分=0.96
- 归一化CTR = 1.2/3 = 0.40
- 归一化CVR = 14/15 = 0.93
- 归一化增速 = 4/5 = 0.80
- 推送分 = (0.40×0.20 + 0.93×0.40 + 0.80×0.20 + 0.96×0.20) × 100 = 80.40
- **等级：A 优质流量池｜稳定加权**

## 优化策略矩阵

### CTR优化（权重20%）
- 主图A/B测试（提升点击率最快的方式）
- 标题关键词前置
- 价格竞争力参考
- Coupon/Prime标识优化

### CVR优化（权重40%，ROI最高）
- 五点描述突出核心卖点
- A+Content增强信任感
- 评价星级管理（≥4.3星）
- Q&A预埋高频问题
- 变体覆盖策略

### 7天增速优化（权重20%）
- 新品期流量加速策略
- 站外引流配合
- 广告预算阶梯递增
- 促销节奏控制

### 账号健康分优化（权重20%）
- ODR（订单缺陷率）<1%
- 迟发率<4%
- 退货率管控
- 合规经营保障

## 行业基准值参考

| 类目 | 优秀CTR | 优秀CVR | 健康增速 |
|------|---------|---------|---------|
| 3C电子 | 2.5% | 12% | 3 |
| 家居日用 | 3.0% | 15% | 4 |
| 服饰箱包 | 2.0% | 10% | 5 |
| 美妆个护 | 3.5% | 18% | 4 |
| 宠物用品 | 2.8% | 14% | 4 |
| 户外运动 | 2.2% | 11% | 3 |

## 常见误区

| 误区 | 真相 |
|------|------|
| "广告花得多=推送分高" | 广告只贡献7天增速（20%），CVR（40%）才是核心 |
| "价格越低推送分越高" | 低价可能拉低CVR（退货多），反而降分 |
| "只要星级高就够了" | 星级只影响CVR的一部分，4维均衡才能拿高分 |
| "老品推送分一定高" | 7天增速权重20%，老品增速放缓会被新品超越 |
| "Listing优化一次就行" | 推送分是动态的，需要持续维护4维指标 |

## Verification

After completing amazon-push-score workflow:
- [ ] 4个输入指标已获取（CTR/CVR/增速/健康分）
- [ ] 推送分计算结果合理（0-100区间）
- [ ] 流量池等级判定准确
- [ ] 优化建议针对得分最低的维度
- [ ] 行业基准值对比已完成
- [ ] 优化策略可执行、有优先级

---

## 不适用场景

本技能专注于亚马逊A9算法推送评分系统，以下场景不适用：

- 非亚马逊平台的流量评分（各平台算法差异较大）
- 需要实时算法数据（本技能基于用户提供的指标做评估，不连接任何平台数据）
- 广告出价策略（请用amazon-ads-optimizer或miaoji-bid-guard）
- Listing文案优化（请用amazon-listing-doctor）

---

## 相关技能推荐

- **amazon-listing-doctor**：push-score识别CTR/CVR短板后，listing-doctor帮助优化文案提升转化
- **amazon-ads-optimizer**：push-score识别流量问题后，ads-optimizer帮助优化广告策略
- **miaoji-asin-clinic**：push-score是快速评分，asin-clinic是深度诊断，两者互补
- **amazon-rufus-optimizer**：推送评分不含Rufus维度，rufus-optimizer补充AI导购优化