---
name: cross-border-listing-optimizer
description: |-
  跨境电商AI上架与优化专家。支持Amazon、Etsy、TikTok Shop、
  Shopify等多平台商品Listing批量生成：SEO标题、五点描述、
  产品详情、关键词挖掘、A+页面文案、产品图AI提示词。
  支持批量处理（一次生成100+商品），中英文双语输出。
  触发词：跨境上架、Amazon listing、跨境电商、listing优化、产品描述生成。
agent_created: true
version: 1.0.0
display_name: "跨境上架优化器"
display_name_en: "Cross-Border Listing Optimizer"
description_zh: "跨境电商商品上架自动化，批量生成SEO优化的商品Listing"
description_en: "Automated cross-border e-commerce listing generation with SEO optimization"
visibility: "public"
allowed-tools:
  - Read
  - Write
  - WebSearch
  - WebFetch
---

# 跨境电商AI上架与优化专家

## 变现逻辑

本技能是2026年最热的被动收入路径之一。跨境电商卖家每天需要大量产品文案，
人工写一条Listing需要30-60分钟，本技能30秒生成一条，可直接出售服务或自用。

**赚钱方式**：
- 在闲鱼/淘宝接"跨境电商Listing代写"单，50-200元/条
- 自营跨境电商店铺，用本技能批量铺货
- 做Amazon/Etsy/TikTok Shop代运营服务包月

---

## 支持平台与格式

| 平台 | 标题长度 | 特点 |
|------|---------|------|
| Amazon | 200字符以内 | 关键词前置，品牌故事，A+内容 |
| Etsy | 140字符以内 | 手工感，故事性，标签系统 |
| TikTok Shop | 60字符以内 | 短平快，场景化，热门标签 |
| Shopify | 70字符以内 | SEO友好，品牌统一 |
| eBay | 80字符以内 | 核心卖点+规格参数 |

## 核心能力

### 1. 批量Listing生成

用户提供产品信息（名称/品类/卖点/目标平台）：

1. **关键词研究**：自动生成高搜索量长尾关键词（基于目标平台搜索趋势）
2. **标题优化**：按平台规则生成SEO标题
   - Amazon：品牌+核心词+特性词+场景词+规格词
   - Etsy：情感词+品类+特色+用途
   - TikTok Shop：痛点+场景+行动号召
3. **五点描述**：按平台最佳实践生成卖点列表
4. **产品描述**：详细描述含SEO关键词自然嵌入
5. **标签/关键词**：平台适配的搜索标签
6. **A+内容**：Amazon A+页面模块文案（图片提示词+描述）

### 2. 产品图AI提示词生成

为每个产品生成适配的AI绘图提示词：
- 主图（白底/场景）
- 附图（细节/使用场景/尺寸对比）
- A+模块图
- 视频脚本提示词

### 3. Listing优化（已有ASIN）

用户提供现有Listing：

1. 分析当前Listing的SEO不足
2. 检查关键词覆盖率
3. 评估标题/描述的质量
4. 对比同类目Best Seller的Listing策略
5. 输出优化建议+改写版本

---

## 使用流程

### 快速生成（单个商品）

```
用户输入："我做了一款瑜伽垫，Tpe材质，防滑，厚度6mm，
送收纳带和背包，想在Amazon上卖"

输出：
━━━━━━━━━━━━━━━━━━━━━━━━
📦 产品：TPE防滑瑜伽垫
━━━━━━━━━━━━━━━━━━━━━━━━

📌 SEO标题（Amazon）：
TOPHEUS Yoga Mat 6mm Thick TPE Non Slip
Exercise Mat with Carrying Strap & Backpack
- Eco Friendly Workout Mat for Home Gym
Pilates Running Fitness

📋 五点描述：
1. ✅ 6mm TPE环保材质...
2. ✅ 双面防滑纹理...
...

🔑 后台关键词：
yoga mat, exercise mat, non slip yoga mat,
tpe yoga mat, thick yoga mat, pilates mat,
fitness mat, home gym mat, workout mat

🎨 主图提示词：
Minimalist yoga mat on white background,
rolled and unrolled view, 6mm thickness visible,
TPE texture close up, professional product
photography, soft studio lighting, 8K
━━━━━━━━━━━━━━━━━━━━━━━━
```

### 批量生成（100+商品）

用户提供CSV/Excel：

| 产品名 | 品类 | 卖点 | 材质 | 尺寸 | 目标平台 |
|--------|------|------|------|------|---------|
| Yoga Mat | 健身 | 防滑环保 | TPE | 6mm | Amazon |
| ... | ... | ... | ... | ... | ... |

输出：批量生成含标题+描述+关键词+图片提示词的CSV文件

---

## 各平台最佳实践

### Amazon
- 标题格式：品牌 + 核心关键词 + 特性 + 规格 + 使用场景
- 五点描述：每个卖点独立，突出1-2个关键词
- A+内容：故事线 + 对比图 + 场景图
- 后台关键词：不使用重复词，不包含品牌名

### Etsy
- 标题前40字符最关键（搜索结果截断）
- 13个标签位全部填满
- 描述讲产品故事和制作过程
- 突出 handmade 和 unique

### TikTok Shop
- 标题短而有力，包含热门话题词
- 视频描述含行动号召（Link in bio/Shop now）
- 利用 Trending Hashtags
- 场景化展示产品

---

## 输出格式

- 单条：结构化Markdown报告
- 批量：CSV文件（可导入各平台后台）
- A+内容：Amazon A+ JSON格式（可选）
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
