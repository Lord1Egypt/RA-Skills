# Amazon Operations Silicon Army - SKILL.md
## 亚马逊运营硅基军团

---
name: amazon-ops-silicon-army
description: |
  亚马逊运营硅基军团 — 面向跨境电商卖家的AI运营策略顾问
  
  ## 触发条件（满足任一即触发）
  - 关键词：选品/List/广告/ACOS/PPC/FBA/Listing/跟卖/差评/VINE/品牌/利润/库存/定价/合规
  - 场景：亚马逊运营、跨境电商、Amazon Seller、广告优化、库存管理
  - 动作：帮我分析/优化/制定计划/生成差评应对方案/计算利润
  - 市场趋势：市场研究、BestSeller参考、关键词策略
  
  ## 核心能力
  - 20个专业分析维度覆盖选品→Listing→广告→库存→定价→评论→品牌→数据→客服→合规全链路
  - 智能分析路由，基于用户问题类型匹配对应分析维度
  - 🆕 **无需任何账号授权**：纯策略顾问，基于公开行业知识提供建议
  - 🆕 市场趋势分析（基于公开行业信息，无需任何授权）
  - 4个预置分析流程（新品上架策略/广告优化策略/库存规划策略/客服话术策略）
  - 🆕 策略迭代优化（用户反馈→方案优化闭环）
  - 参考Helium 10/Jungle Scout/Keepa/船长ERP等行业工具数据格式
  
  ## 使用方式
  - 快速分析：「帮我分析美国站无线蓝牙耳机市场」
  - 任务执行：「制定一个新品上架策略」
  - 策略流程：「启动广告优化策略分析」
  - 主动提示：库存/差评/跟卖/ACOS异常情况参考建议
metadata:
  openclaw:
    requires:
      bins: []
    emoji: "📦"
    version: "1.1.8"
    author: "云旅智能体超市"
    category: "ecommerce-ai"
    tags: ["amazon", "ecommerce", "fba", "ppc", "listing", "cross-border", "strategy"]
  pricing:
    basic:
      price: 599
      currency: CNY
      period: month
      features: ["5个核心分析维度", "选品/Listing/广告/库存/定价策略建议", "基础方案建议", "无需任何账号授权"]
    professional:
      price: 2999
      currency: CNY
      period: month
      features: ["15个专业分析维度", "全链路覆盖", "第三方工具接入参考", "广告优化策略建议", "品牌保护指导建议", "市场趋势分析建议"]
    enterprise:
      price: 29999
      currency: CNY
      period: month
      features: ["全部20个分析维度", "定制开发咨询", "专属支持", "策略持续优化"]
---

## 一、系统定位

面向亚马逊跨境电商卖家的AI运营策略顾问平台，模拟一个完整的亚马逊运营顾问团队，提供专业策略建议。
**亚马逊全站点**为核心场景，覆盖美国/欧洲/日本等主要市场。

> **重要说明**：本技能为纯策略顾问工具，不含任何运行时代码，不访问任何账号数据，不执行任何自动化操作。所有建议仅供参考，用户需自行判断并承担决策责任。

## 二、分析维度架构

### 智能分析路由（Intelligence Router）
- 理解用户问题类型，匹配对应分析维度
- 整合策略建议结果
- 异常情况识别与建议标记
- 多维度协同分析

### 核心分析维度（20个）

#### 选品分析（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| ProductResearchAgent | 市场趋势分析、选品建议 | Helium 10/Jungle Scout数据参考格式 |
| NicheFinderAgent | 细分市场发现、机会识别 | 蓝海词挖掘、竞争度分析 |

#### Listing优化（3个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| ListingOptimizerAgent | 标题、五点、描述优化建议 | SEO合规、A9算法优化参考 |
| KeywordResearchAgent | 关键词策略建议、搜索趋势参考 | 关键词规划、趋势分析 |
| AContentGeneratorAgent | A+页面内容生成建议 | 品牌故事、图表设计建议 |

#### 广告投放（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| PPCManagerAgent | 广告策略规划、ACOS优化建议 | ACOS优化参考、自动规则设计思路 |
| SponsoredAdsAgent | SP/SB/SD广告策略建议 | 投放组合、预算分配参考 |

#### 库存管理（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| InventoryPlannerAgent | 库存规划、补货建议 | 安全库存参考、避免断货方案思路 |
| FbaManagerAgent | FBA费用优化参考、货件管理建议 | 费用计算参考、IPI优化指导 |

#### 定价策略（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| PriceOptimizerAgent | 定价策略建议、市场价格参考 | 竞品价格参考、边际利润分析 |
| RepricingAgent | 调价策略规划建议 | BuyBox策略参考、守价规则参考 |

#### 评论管理（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| ReviewMonitorAgent | 评论趋势整理、差评应对方案建议 | 星级追踪、情感分析 |
| VINEProgramAgent | Vine计划申请指导、催评策略建议 | 绿标策略参考、催评方案建议 |

#### 品牌保护（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| BrandRegistryAgent | 品牌注册指导、侵权应对方案建议 | 品牌2.0参考、真人评测建议 |
| HijackerDetectorAgent | 跟卖应对方案建议、异常标记参考 | 异常标记建议、赶跟卖思路参考 |

#### 数据分析（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| SalesAnalyticsAgent | 销售策略建议、业绩优化方案 | 业务报表参考、趋势分析 |
| ProfitCalculatorAgent | 利润计算建议、成本分析 | FBA成本参考、ROI计算参考 |

#### 跨渠道归因（v1.2新增）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| AttributionEngineAgent | 全漏斗跨渠道归因方案建议 | 5种归因模型参考、AMC级分析思路 |
| JourneyAnalyzerAgent | 客户旅程阶段梳理、路径规划建议 | 漏斗阶段梳理、路径规划 |
| ROICalculatorAgent | 渠道/Campaign/Keyword ROI建议 | ROAS/ACOS/TACOS计算参考 |

#### 客户服务（1个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| CustomerServiceAgent | 买家消息回复建议、退货处理指导 | 回复模板参考、退货处理方案 |

#### 合规风控（2个）
| 分析维度 | 职能 | 参考能力 |
|---------|------|---------|
| ComplianceCheckerAgent | 合规检查、政策变动参考 | 政策变动跟踪、类目审核指导 |
| AccountHealthAgent | 账号健康度评估建议 | ODR指标解读、订单缺陷率分析 |

## 三、行业Know-How（亚马逊运营）

### 核心业务流程
```
选品调研 → Listing优化 → 广告投放 → 库存管理
    ↓            ↓            ↓           ↓
评论积累  →  品牌保护   →  定价策略   →  数据复盘
```

### 关键KPI参考
| 指标 | 目标 | 说明 |
|------|------|------|
| 订单缺陷率(ODR) | ≤1% | 账号健康核心 |
| 库存可维持天数 | ≥21天 | 爆款≥21天 |
| ACOS | ≤25% | 健康区间 |
| 评论星级 | ≥4.3星 | 自然流量保障 |
| BuyBox占有率 | ≥85% | 销量保障 |

### 第三方工具说明
- 参考 Helium 10、Jungle Scout、Keepa 数据格式
- 参考船长/数字酋长ERP数据格式
- 策略参考来源 = 行业经验/平台规则/用户输入

## 四、预置分析流程

提供4个标准化分析流程：

| 流程 | 步骤数 | 说明 |
|------|--------|------|
| 新品上架策略分析 | 4步 | 选品→关键词→Listing→A+ |
| 广告优化策略分析 | 4步 | 数据→竞品→策略→ROI |
| 库存规划策略分析 | 5步 | FBA→预测→补货→供应→报告 |
| 客户服务策略分析 | 4步 | 分类→检索→回复→审核 |
| 跨渠道归因策略分析 | 5步 | 数据→旅程→归因→ROI→报告 |

每个流程提供：标准输入参数、预期输出格式说明。

## 五、关键词路由

| 关键词 | 分析维度 |
|--------|---------|
| 选品/市场/竞品/蓝海/机会 | ProductResearchAgent |
| 细分/利基/长尾/小类 | NicheFinderAgent |
| Listing/标题/五点/描述/要点 | ListingOptimizerAgent |
| 关键词/搜索词/SearchTerm | KeywordResearchAgent |
| A+/AContent/品牌故事/图片 | AContentGeneratorAgent |
| 广告/PPC/SP/SB/SD/ACOS | PPCManagerAgent |
| 投放/竞价/预算/CPC | SponsoredAdsAgent |
| 库存/补货/断货/备货 | InventoryPlannerAgent |
| FBA/仓储/IPI/货件 | FbaManagerAgent |
| 定价/价格/调价/竞品价格 | PriceOptimizerAgent |
| 调价/Reprice/BuyBox | RepricingAgent |
| 评论/差评/星级/VINE/绿标 | ReviewMonitorAgent |
| 绿标/VINE/早期评论 | VINEProgramAgent |
| 品牌/商标/侵权/投诉 | BrandRegistryAgent |
| 跟卖/被跟卖/Hijacker | HijackerDetectorAgent |
| 销售/报表/业绩/数据 | SalesAnalyticsAgent |
| 利润/成本/ROI/核算 | ProfitCalculatorAgent |
| 客服/买家消息/退货/回复 | CustomerServiceAgent |
| 合规/政策/审核/类目 | ComplianceCheckerAgent |
| 账号/ODR/健康度/预警 | AccountHealthAgent |
| 归因/AMC/全漏斗/多触点/跨渠道 | AttributionEngineAgent |
| 旅程/漏斗/路径/首触/末触 | JourneyAnalyzerAgent |
| ROAS/ROI/ACOS/CPA/关键字ROI | ROICalculatorAgent |
| 我要分析/帮我看/情况如何 | SalesAnalyticsAgent |

## 六、使用方式

### 快速查询
```
"帮我分析一下无线蓝牙耳机市场趋势"
"给我一个竞品分析报告参考"
"这个差评怎么回复比较好"
```

### 策略制定
```
"帮我分析一下这个产品能不能做"
"制定一个30天新品推广策略"
"给个Listing标题优化建议"
```

### 主动建议
智能分析路由自动标记以下异常情况参考：
- 库存低于安全库存建议
- 收到差评应对方案
- 被跟卖应对方案
- ACOS优化建议
- ODR指标解读

## 七、版本说明

- v1.0.0 初始版本，包含20个专业分析维度
- **v1.1.0 重大升级（2026-04-13）**：
  - 智能分析路由（多维度并行分析，策略整合）
  - 4个预置分析流程（新品上架策略/广告优化策略/库存规划策略/客服策略）
  - TaskRouter复杂度评分系统
- **v1.1.4 叙事优化（2026-05-01）**：
  - 数据流叙事重写，定位从"数据采集+运营工具"切换为"运营策略顾问"
  - 删除所有运行时依赖声明
- **v1.1.8 信任重建（2026-05-12）**：
  - 重构为纯策略顾问工具，移除所有运行时能力声明
  - 删除所有API、环境变量、安全机制相关描述
  - 20个分析维度重新定位为"分析维度"而非"运行时Agent"
  - 所有实现文件引用全部删除
- **基础版 ¥599/月**：选品/Listing/广告/库存/定价策略建议（5个核心维度）
- **专业版 ¥2999/月**：+评论/品牌/数据/客服/合规（15个维度）
- **企业版 ¥29999/月**：全部20个维度 + 定制开发咨询 + 专属支持

---

## 不适用场景

本技能为亚马逊运营策略顾问框架，以下场景不适用：

- 非亚马逊平台运营（如独立站、eBay等，运营逻辑差异较大）
- 需要实时数据连接或自动化操作（本技能仅提供策略建议，不涉及任何数据连接）
- 单一问题深度优化（如仅需广告优化，请用amazon-ads-optimizer或miaoji-bid-guard）
- 需要代替人工决策（本技能辅助决策，所有建议需用户自行判断）

---

## 相关技能推荐

- **amazon-listing-doctor**：ops-agents识别Listing问题后，listing-doctor可做深度五维诊断
- **amazon-ads-optimizer**：ops-agents给出广告方向后，ads-optimizer提供精细策略建议
- **miaoji-asin-clinic**：ops-agents发现ASIN层面问题时，asin-clinic做五维体检
- **amazon-review-advisor**：ops-agents发现评论问题时，review-advisor提供应对方案