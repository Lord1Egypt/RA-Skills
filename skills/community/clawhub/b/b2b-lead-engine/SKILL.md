---
name: b2b-lead-engine
description: "B2B商机挖掘助手。当用户说'我要卖XXX'、'帮我找客户'、'分析竞品'、'挖掘商机'时启用，自动识别竞品、挖掘潜在客户、生成个性化BD材料。支持6阶段标准化流程：配置生成→信息采集→商机识别→信息补全→BD材料生成→输出交付。"
---

# B2B商机挖掘引擎（智能获客引擎）

## Overview

这是一个完整的B2B商机挖掘技能，帮助用户从产品描述开始，完成潜在客户挖掘全流程。技能涵盖：竞品识别、竞品动态监控、竞品销售Connection挖掘、商机评分、信息补全（含性格分析）、个性化BD材料生成，最终输出标准化日报。

## 触发条件

用户输入包含以下模式时激活：
- "我要卖..."
- "帮我找客户..."
- "分析竞品..."
- "挖掘商机..."

## Workflow

### 阶段1：配置生成

收到用户产品描述后，执行以下步骤：

1. **产品分析**：识别产品核心功能和所属赛道
2. **竞品搜索**：通过联网搜索找出主要竞争对手（5-10个）
3. **目标人群推断**：确定可能的购买决策者职位
4. **关键词生成**：生成用于信息采集的搜索关键词（产品/需求/场景3类）
5. **竞品销售搜索**：搜索竞品销售人员的LinkedIn

完成后输出配置确认：

```
📋 配置确认

产品：[产品名]
赛道：[行业赛道]

已识别竞品（将监控其动态+挖掘其销售Connection）：
  ✓ 竞品1
  ✓ 竞品2
  ✓ 竞品3
  ✓ 竞品4
  ✓ 竞品5

目标决策人职位：
  ✓ 职位1
  ✓ 职位2
  ✓ 职位3

搜索关键词：
  • 关键词1
  • 关键词2
  • 关键词3

竞品销售（用于Connection挖掘）：
  • 销售1 @ 竞品1 - LinkedIn URL
  • 销售2 @ 竞品2 - LinkedIn URL

是否需要调整？[确认启动] / [修改配置]
```

等待用户确认后，继续下一步。用户可以调整竞品列表和目标人群。

### 阶段2：信息采集（依次执行两个任务）

确认配置后，依次执行以下两个信息采集任务：

**任务A：竞品动态监控**（详见"竞品动态监控"章节）
- 产品更新/新功能发布
- 融资/收购新闻
- 合作伙伴公告
- 客户案例
- 行业合作情报
- 关键人物动态
- 行业活动扫描

**任务B：竞品销售Connection挖掘**（详见"竞品销售Connection挖掘"章节）
- 访问竞品销售LinkedIn
- 提取Connection列表
- 智能筛选潜在客户

### 阶段3：商机识别与评分

合并所有渠道发现的线索，执行：
1. 线索汇总与去重
2. 排除过滤（竞争对手、已有客户）
3. 多维度评分（详见"商机评分体系"章节）
4. 按优先级排序

### 阶段4：信息补全

对评分后的商机执行：
1. 公司信息补全（官网、规模、融资、业务）
2. 决策人识别
3. 联系方式获取
4. 背景调研
5. 性格分析（详见"性格分析与画像"章节）

### 阶段5：BD材料生成

基于性格分析结果，为每个商机生成：
1. 个性化LinkedIn Connection话术（≤300字符）
2. 个性化Email开发信（≤150词）

详见"BD材料生成"和"LinkedIn BD最佳实践"章节。

### 阶段6：输出交付

生成完整日报（详见"日报输出格式"章节）。

---

## 配置生成详细指南

### 产品分析

```
分析产品描述，提取：
- 产品核心功能
- 所属行业赛道
- 目标市场（B2B/B2C，国内/海外）
- 产品差异化特点
```

### 竞品搜索

```
搜索关键词模式：
- "[产品类型] companies"
- "[产品类型] alternatives"
- "[产品类型] competitors"

输出竞品列表（5-10个）
```

### 目标人群推断

根据产品类型推断决策者：

| 产品类型 | 目标决策人 |
|----------|------------|
| 技术产品 | CTO, VP Engineering, Head of AI |
| 营销产品 | CMO, VP Marketing, Head of Growth |
| 销售产品 | VP Sales, Head of BD |
| 设计产品 | Head of Design, Creative Director |
| 通用SaaS | VP Product, COO |

### 搜索关键词生成

生成3类关键词：
- **产品关键词**：产品类型相关
- **需求关键词**：客户痛点相关
- **场景关键词**：使用场景相关

### 竞品销售搜索

```
对每个竞品，搜索其销售人员：
搜索语法：site:linkedin.com "[竞品名]" + "Sales" OR "BD" OR "Account Executive"

输出销售列表：
- 姓名
- 职位
- LinkedIn URL
- 负责区域
```

### 行业适配参考

| 行业 | 竞品例子 | 目标决策人 | 搜索关键词 |
|------|----------|------------|------------|
| 视频AI | Runway, Pika, Luma, Kling | VP Product, Head of AI | video generation, AI video |
| 客服SaaS | Zendesk, Intercom, Freshdesk | VP CS, Head of Support | customer support software |
| BI工具 | Tableau, PowerBI, Looker | CDO, Head of Analytics | business intelligence |
| 营销自动化 | HubSpot, Marketo, Pardot | CMO, VP Marketing | marketing automation |
| 云服务 | AWS, Azure, GCP | CTO, VP Engineering | cloud infrastructure |
| 设计工具 | Figma, Sketch, Adobe XD | Head of Design, VP Product | design tools, UI/UX |

### 业务配置文件格式 (business_config.yaml)

```yaml
business_config:
  # 基础信息
  product_name: "{产品名}"
  value_proposition: "{一句话价值主张}"
  target_persona:
    - "{目标职位1}"
    - "{目标职位2}"

  # 竞品列表
  competitors:
    - name: "{竞品1}"
      keywords:
        - "{关键词1}"
        - "{关键词2}"
      sales_people:
        - name: "{销售姓名}"
          title: "{职位}"
          linkedin: "{LinkedIn URL}"

  # 排除列表
  exclusions:
    competitors:
      - "{竞品1}"
      - "{竞品2}"

  # 搜索关键词
  search_keywords:
    product: ["{关键词}"]
    demand: ["{关键词}"]
    scenario: ["{关键词}"]
```

---

## 竞品动态监控

### 1. 竞品动态监控

对于每个竞品，执行以下搜索：

```
搜索模式：
- "[竞品名] announcement" + 时间范围
- "[竞品名] launch" + 时间范围
- "[竞品名] funding" + 时间范围
- "[竞品名] partnership" + 时间范围

搜索平台：
- Google News
- Twitter/X
- LinkedIn
- TechCrunch, VentureBeat, 36kr

提取信息类型：
- 产品更新/新功能发布
- 融资/收购新闻
- 合作伙伴公告
- 客户案例/使用者
- 价格变动
- 团队变动
```

### 2. 行业合作情报

```
搜索关键词：
- "[行业关键词] partnership"
- "[行业关键词] integration"
- "[行业关键词] collaboration"

关注点：
- 哪些公司在寻找类似解决方案
- 行业趋势和热点
- 大厂动向
- 新的应用场景
```

### 3. 关键人物追踪

```
对于每个竞品的关键人物：

检查渠道：
- LinkedIn动态
- Twitter/X动态
- 博客文章
- 演讲视频

关注内容：
- 讨论的话题
- 提到的合作伙伴
- 参加的活动
- 招聘的岗位
- 分享的观点
```

### 4. 行业活动扫描

```
搜索平台：
- lu.ma
- Eventbrite
- Meetup
- 行业会议官网

搜索关键词：
- "[行业关键词] conference"
- "[行业关键词] summit"
- "[行业关键词] meetup"

提取信息：
- 活动名称、时间、地点
- 主办方/赞助商（潜在商机）
- 参会者/演讲者列表
- 报名链接
```

### 商机信号识别

在监控过程中，识别以下商机信号：

1. **客户案例信号**：竞品公布的客户案例；客户在社交媒体提及竞品
2. **需求信号**：公司公开表达相关需求；招聘相关岗位
3. **预算信号**：最近融资的公司；扩张中的公司
4. **不满信号**：对竞品的抱怨或负面评价；寻求替代方案的帖子

### 竞品动态输出格式

**竞品动态表**：

| 竞品 | 动态类型 | 动态内容 | 来源 | 时间 | 商机信号 |
|------|----------|----------|------|------|----------|
| {竞品名} | 产品更新/融资/合作 | {具体内容} | {来源URL} | {日期} | {是否包含潜在客户信息} |

**行业合作情报表**：

| 公司A | 公司B | 合作内容 | 来源 | 时间 | 相关性 |
|-------|-------|----------|------|------|--------|
| {公司名} | {公司名} | {合作详情} | {来源URL} | {日期} | {与我们产品的相关性} |

**关键人物动态表**：

| 人物 | 公司/职位 | 动态内容 | 平台 | 时间 | 潜在价值 |
|------|-----------|----------|------|------|----------|
| {姓名} | {公司} {职位} | {动态摘要} | LinkedIn/Twitter | {日期} | {对商机挖掘的价值} |

**即将活动表**：

| 活动名称 | 时间 | 地点 | 主办方 | 相关赞助商 | 链接 |
|----------|------|------|--------|------------|------|
| {活动名} | {日期时间} | {线上/城市} | {主办方} | {赞助商列表} | {URL} |

### 优先级标记

| 优先级 | 标准 |
|--------|------|
| 🔥 高 | 包含明确的潜在客户或商机信号 |
| ⭐ 中 | 包含行业趋势或间接线索 |
| 📋 低 | 一般性信息，供参考 |

---

## 竞品销售Connection挖掘

> 这是最核心的策略。竞品销售的Connection本质上是"已验证的潜在客户池"：
> - ✅ 竞品销售已花时间筛选过这些人
> - ✅ 这些人已被"教育"过，了解这类产品
> - ✅ 有些可能对竞品不满意，正好是机会
> - ✅ 转化率远高于冷名单

### Step 1: 获取竞品销售LinkedIn

```
方法A：从配置文件读取（如已配置 sales_people）

方法B：自动搜索
  搜索语法：site:linkedin.com "[竞品名]" + "Sales" OR "BD" OR "Account Executive"

  优先级职位：
  1. Sales Director / VP Sales
  2. Business Development Manager
  3. Account Executive
  4. Sales Manager
  5. Partnership Manager
```

### Step 2: 访问销售LinkedIn页面

```
提取信息：
- 销售姓名和职位
- 所在公司（确认是竞品）
- Connection数量
- 负责区域
- 工作经历
```

### Step 3: 提取Connection列表

```
遍历可见的Connection：
- 姓名
- 职位
- 公司
- LinkedIn URL
- 共同连接数
```

### Step 4: 智能筛选潜在客户

**职位筛选规则**：

```
匹配目标决策人职位关键词：
- VP / Vice President
- Head of
- Director of
- Chief (CTO, CMO, CPO等)
- Lead / Manager（特定领域）

示例：
- VP of Product ✅
- Head of AI ✅
- Creative Director ✅
- Software Engineer ❌
- Recruiter ❌
```

**公司筛选规则**：

```
符合目标客户画像：
- 行业匹配
- 规模匹配（员工数、融资阶段）
- 业务模式匹配

排除：
- 竞争对手员工
- 同行销售人员
- 猎头/咨询公司
```

**匹配原因分析**：

```
为每个筛选出的人分析匹配原因：
- 职位契合度：为什么这个职位可能是决策人
- 公司契合度：为什么这家公司可能有需求
- 时机信号：是否有近期需求的迹象
```

### Connection挖掘输出格式

**潜在客户列表**：

| 来源销售 | 潜在客户 | 职位 | 公司 | 匹配原因 | LinkedIn | 优先级 |
|----------|----------|------|------|----------|----------|--------|
| {销售名}@{竞品} | {姓名} | {职位} | {公司} | {为什么是潜在客户} | {URL} | 🔥/⭐/📋 |

**详细信息（每个潜在客户）**：

```yaml
潜在客户:
  姓名: {姓名}
  职位: {职位}
  公司: {公司}
  linkedin_url: {URL}

来源信息:
  来源销售: {销售名}
  竞品公司: {竞品名}
  发现时间: {日期}

匹配分析:
  职位契合: {分析}
  公司契合: {分析}
  需求信号: {分析}

优先级: {高/中/低}
优先级原因: {说明}
```

**统计汇总**：

```
📊 Connection挖掘统计

总检查销售数：{X}人
总扫描Connection数：{X}人
筛选后潜在客户：{X}人
  - 🔥 高优先级：{X}人
  - ⭐ 中优先级：{X}人
  - 📋 低优先级：{X}人

转化率：{筛选后/总扫描}%

来源分布：
  - {竞品1}：{X}人
  - {竞品2}：{X}人
```

### 隐私受限情况处理

如果竞品销售的LinkedIn设置了隐私，看不到Connection：
1. 尝试查找该竞品的其他销售
2. 关注该销售的互动（点赞、评论），从互动对象中发现线索
3. 查看该销售参加的活动，从参会者中发现线索
4. 报告限制情况，调整策略

### 注意事项

1. **合规性**：只访问公开可见的Connection信息
2. **频率控制**：避免过于频繁的访问，防止账号被限制
3. **筛选质量**：宁缺毋滥，确保每个潜在客户都有明确的匹配原因
4. **多销售覆盖**：每个竞品建议追踪2-3个销售，扩大覆盖面
5. **去重处理**：多个销售可能有相同的Connection，需要去重

---

## 商机评分体系

### 线索汇总

```
合并所有来源的线索：
- 竞品客户案例
- 公开表达需求的公司
- 参加行业活动的公司
- Connection挖掘的潜在客户
- 融资/扩张中的公司

去重处理：
- 按公司名称去重
- 保留信息最完整的记录
- 合并多个来源的信息
```

### 排除过滤

```
for 线索 in 所有线索:
    if 线索.公司名 in 竞争对手列表: 排除
    if 线索.公司名 in 已有客户列表: 排除
    if 线索.公司名 in 其他排除条件: 排除
    否则: 保留
```

排除记录需保留，便于后续审核。

### 评分维度与权重

| 维度 | 权重 | 评分标准（0-100） |
|------|------|-------------------|
| 需求明确度 | 30% | 是否明确表达需求/痛点 |
| 公司规模 | 20% | 员工数、融资阶段、收入 |
| 决策人可触达性 | 20% | 是否能找到联系方式 |
| 时机紧迫度 | 15% | 是否近期有项目/需求 |
| 匹配度 | 15% | 与产品的契合程度 |

### 各维度评分细则

#### 需求明确度（30%）

| 分数 | 条件 |
|------|------|
| 90-100 | 公开发帖寻求解决方案 |
| 70-89 | 正在使用竞品，有明确痛点 |
| 50-69 | 在竞品销售Connection中，职位匹配 |
| 30-49 | 参加相关活动，关注相关话题 |
| 0-29 | 仅为行业相关，需求不明确 |

#### 公司规模（20%）

| 分数 | 条件 |
|------|------|
| 90-100 | 大型企业（1000+员工）或知名品牌 |
| 70-89 | 中型企业（100-999员工）或C轮+ |
| 50-69 | 小型企业（10-99员工）或A/B轮 |
| 30-49 | 初创企业（<10员工）或种子轮 |
| 0-29 | 个人或无法判断 |

#### 决策人可触达性（20%）

| 分数 | 条件 |
|------|------|
| 90-100 | 有直接联系方式（Email+电话） |
| 70-89 | 有Email或LinkedIn可发送消息 |
| 50-69 | 仅有LinkedIn，需要Connection |
| 30-49 | 只知道公司，需要搜索决策人 |
| 0-29 | 无法找到任何联系途径 |

#### 时机紧迫度（15%）

| 分数 | 条件 |
|------|------|
| 90-100 | 明确表示近期要采购/评估 |
| 70-89 | 最近30天有相关动态 |
| 50-69 | 最近90天有相关动态 |
| 30-49 | 今年有相关动态 |
| 0-29 | 无时机信号 |

#### 匹配度（15%）

| 分数 | 条件 |
|------|------|
| 90-100 | 完美契合目标客户画像 |
| 70-89 | 大部分特征匹配 |
| 50-69 | 部分特征匹配 |
| 30-49 | 勉强相关 |
| 0-29 | 关联度低 |

### 来源加权

不同渠道的线索有基础加分：

| 来源 | 基础加分 | 原因 |
|------|----------|------|
| 🔥 竞品销售Connection | +10 | 已被竞品"教育"过 |
| ⭐ 公开表达需求 | +8 | 需求明确 |
| ⭐ 正在使用竞品 | +5 | 有预算和经验 |
| 📌 行业活动参与者 | +3 | 在关注领域 |
| 📌 最近融资公司 | +3 | 有预算 |

来源加分只能加一次（选最高的来源）。

### 最终优先级

| 优先级 | 最终得分 | 建议行动 |
|--------|----------|----------|
| 🔥 高 | ≥80分 | 今日发送Connection/Email |
| ⭐ 中 | 50-79分 | 本周跟进 |
| 📋 低 | <50分 | 加入培育列表 |

### 商机来源优先级总览

| 优先级 | 来源 |
|--------|------|
| 🔥 P0 | 竞品销售Connection挖掘 |
| ⭐ P1 | 公开表达需求的公司 |
| ⭐ P1 | 正在使用竞品的公司 |
| 📌 P2 | 参加行业活动的公司 |
| 📌 P2 | 最近融资的公司 |

### 评分输出格式

| 公司 | 联系人 | 来源 | 需求 | 规模 | 可触达 | 时机 | 匹配 | 加分 | 总分 | 优先级 |
|------|--------|------|------|------|--------|------|------|------|------|--------|
| {公司} | {姓名} | {来源} | 85 | 70 | 80 | 60 | 75 | +10 | 85 | 🔥 高 |

---

## 信息补全

### Step 1: 公司信息补全

```
数据来源：
- 公司官网
- LinkedIn公司页面
- Crunchbase
- 新闻报道

需要补全的字段：
- 公司全称
- 公司简介/主营业务
- 公司规模（员工数）
- 融资阶段/金额
- 总部位置
- 行业分类
- 关键产品/服务
```

### Step 2: 决策人识别

```
搜索语法：
site:linkedin.com "[公司名]" + "[目标职位关键词]"

目标职位关键词示例：
- VP of Product / VP Product
- Head of AI / AI Lead
- CTO / Chief Technology Officer
- Director of Business Development
- Head of Partnerships
- CMO / Chief Marketing Officer

验证决策人：
- 确认仍在该公司任职
- 确认职位与目标匹配
- 优先选择更高级别的决策人
```

### Step 3: 联系方式获取

| 方法 | 工具/渠道 | 优先级 |
|------|-----------|--------|
| Email查找工具 | Hunter.io, Snov.io, Apollo | 高 |
| 公司官网 | About/Team页面 | 中 |
| 手动搜索 | Google "[姓名] [公司] email" | 中 |
| LinkedIn | 直接联系（需要连接） | 备选 |

**Email格式推断**：

```
常见企业邮箱格式：
- firstname@company.com
- firstname.lastname@company.com
- f.lastname@company.com
- firstnamel@company.com

可通过已知员工邮箱推断格式
```

### Step 4: 背景调研

```
调研内容：
- 最近的新闻报道
- 社交媒体动态（LinkedIn、Twitter）
- 公开演讲/采访
- 发表的文章/博客

调研目的：
- 发现破冰话题
- 了解关注点
- 确认需求信号
- 评估沟通时机
```

---

## 性格分析与画像

> 目的：根据目标人的性格特征，定制最匹配的沟通风格，提高回复率。

### 分析维度

| 维度 | 分析来源 | 输出 |
|------|----------|------|
| 沟通风格 | LinkedIn发帖、评论 | 正式/轻松、简洁/详细 |
| 关注重点 | 发帖主题、互动内容 | 技术/商业/创新/效率 |
| 决策风格 | 职业背景、履历 | 数据驱动/直觉型/共识型 |
| 个人兴趣 | 分享内容、关注话题 | 用于破冰话题 |

### 分析步骤

```
Step 1: 收集LinkedIn动态
  └── 最近20条发帖/转发/评论

Step 2: 分析沟通风格
  ├── 是否使用emoji？→ 偏轻松
  ├── 帖子长度？→ 喜欢详细 vs 简洁
  └── 语气？→ 正式 vs 随意

Step 3: 分析关注重点
  ├── 发帖主题分类
  └── 互动最多的话题

Step 4: 推断决策风格
  ├── 技术背景 → 可能更重视数据和细节
  ├── 销售/BD背景 → 可能更重视ROI和效果
  └── 创意背景 → 可能更重视创新和体验

Step 5: 发现破冰话题
  └── 最近分享/讨论的非工作话题
```

### 性格画像输出示例

```yaml
性格画像:
  姓名: Mike Lee
  职位: Creative Director @ Nike

  # 沟通风格分析
  沟通风格: 轻松随意
  分析依据:
    - LinkedIn发帖经常使用emoji（🔥 💡 🎨）
    - 语气口语化，不使用商务术语
    - 帖子较短，平均100字以内

  # 关注重点分析
  关注重点: 创意、品牌、视觉storytelling
  热门话题:
    - AI与创意结合
    - 品牌视觉升级
    - 用户体验设计

  # 决策风格分析
  决策风格: 直觉型，重视创新
  分析依据:
    - 创意背景出身
    - 经常分享创新案例
    - 强调"尝试新事物"

  # 破冰话题
  破冰话题:
    - 最近分享：某AI艺术展览
    - 讨论热点：Midjourney的创意应用
    - 个人兴趣：摄影、设计

# 沟通策略建议
建议沟通策略:
  - 开场可提及他最近分享的创意案例
  - 语气轻松，可适当用emoji
  - 强调"创新"和"视觉效果"而非技术细节
  - 避免过于正式的商务用语
  - 首选话术风格：轻松创意型
```

性格分析不充分时（动态数据不足），标记"待补充"，BD材料默认使用"正式专业型"。

---

## BD材料生成

### 性格→话术映射规则

| 性格特征 | 话术调整 |
|----------|----------|
| 轻松随意 | 可用emoji、口语化、简短 |
| 正式专业 | 无emoji、商务用语、结构化 |
| 关注创新 | 强调"新"、"首创"、"突破" |
| 关注效率 | 强调数据、ROI、节省时间 |
| 关注技术 | 提及技术细节、性能指标 |
| 关注商业 | 强调商业价值、案例、客户 |
| 数据驱动 | 提供具体数字、对比数据 |
| 直觉型 | 强调愿景、可能性、趋势 |

### LinkedIn Connection 话术生成

**生成规则**：
- **长度**：≤ 300字符（LinkedIn硬限制）
- **个性化**：必须提到对方公司和产品
- **价值主张**：说明你能提供什么
- **性格匹配**：根据性格分析调整语气
- **无销售感**：首次连接不要直接推销

**话术结构**：
```
1. 称呼 + 表明看到对方在做什么（或破冰话题）
2. 说明你是谁、能提供什么价值
3. 提出连接请求
```

#### 风格A：轻松创意型

适用于：轻松随意、关注创新的目标人

```
Hey {Name}! 👋

{破冰话题 - 提及最近的分享/动态}

I'm {Your Name} from {Company} ({产品简述}).
We're helping creative teams like yours {核心价值}.

Would love to swap ideas!
```

**示例**：
```
Hey Mike! 👋

Loved your recent post about visual storytelling - the Nike campaign was 🔥

I'm Morgan from MiniMax (Hailuo AI video). We're helping creative teams
produce stunning video content 10x faster.

Would love to swap ideas on AI + creativity!
```

#### 风格B：正式专业型

适用于：正式专业、关注效率/数据的目标人

```
Hi {Name},

I noticed {Company} is {对方业务/近期动态}.

At {Your Company}, we help {目标客户类型} {核心价值}
{具体数据/效果}.

Would you be open to a brief conversation about {话题}?

Best regards,
{Your Name}
```

**示例**：
```
Hi Sarah,

I noticed Netflix is expanding its content production capabilities.

At MiniMax, we help media companies reduce video production time by 80%
while maintaining creative quality.

Would you be open to a brief conversation about AI-powered video workflows?

Best regards,
Morgan
```

#### 风格C：技术导向型

适用于：技术背景、关注技术细节的目标人

```
Hi {Name},

Saw {公司}正在{技术相关动态}.

I'm building {产品} at {公司} - {技术特点}.
{技术优势描述}

Would love to chat about {技术话题}.

{Your Name}
```

#### 风格D：商业价值型

适用于：商业背景、关注ROI的目标人

```
Hi {Name},

I noticed {Company}'s {业务动态}.

At {Your Company}, we've helped {客户类型} achieve {具体成果}:
• {数据1}
• {数据2}

Worth a quick chat?

{Your Name}
```

### Email 开发信生成

**生成规则**：
- **个性化**：针对对方公司定制
- **结构化**：问候 → 钩子 → 价值 → CTA
- **简洁**：不超过150词
- **性格匹配**：调整语气和重点

**Email结构**：

```
Subject: [吸引眼球的标题] - {Your Company} x {Their Company}

Hi {Name},

[开头钩子：为什么联系他们，1-2句]

[价值主张：你能帮他们做什么，3个bullet点]
• Benefit 1
• Benefit 2
• Benefit 3

[CTA：明确的下一步行动]

Best regards,
{Your Name}
{Your Title}
{Your Company}
```

**主题行模板**：

| 类型 | 模板 |
|------|------|
| 合作型 | Partnership Opportunity - {Your Company} x {Their Company} |
| 价值型 | How {Company} can {核心价值} |
| 问题型 | Quick question about {他们的业务} |
| 介绍型 | {共同联系人} suggested I reach out |
| 数据型 | {X}% improvement in {指标} - relevant for {Company}? |

**开头钩子模板**：

| 类型 | 模板 |
|------|------|
| 近期动态 | I noticed {Company} recently {动态}... |
| 行业观察 | With {行业趋势}, companies like {Company} are... |
| 共同点 | We both {共同点}... |
| 赞赏型 | I've been following {Company}'s work on {项目}... |
| 问题型 | Many {职位}s I talk to are struggling with {痛点}... |

### BD材料输出格式

```yaml
商机: {公司名} - {联系人}
优先级: {高/中/低}

# 性格匹配分析
性格类型: {轻松/正式/技术/商业}
选用风格: {风格A/B/C/D}
调整要点:
  - {调整点1}
  - {调整点2}

# LinkedIn Connection 话术
linkedin_message: |
  {生成的话术，≤300字符}

字符数: {XX}/300

# Email 开发信
email_subject: "{主题行}"
email_body: |
  {生成的Email正文}

词数: {XX}/150

# 备选版本（可选）
alt_linkedin_message: |
  {备选话术}
```

### 质量检查清单

生成每份材料后，自动检查：

**LinkedIn话术检查**：
- [ ] 长度 ≤ 300字符
- [ ] 提及对方公司名
- [ ] 包含价值主张
- [ ] 语气与性格匹配
- [ ] 无语法错误
- [ ] 有明确的连接请求

**Email检查**：
- [ ] 主题行吸引眼球
- [ ] 开头个性化
- [ ] 包含3个价值点
- [ ] CTA明确简单
- [ ] 总词数 ≤ 150
- [ ] 语气与性格匹配
- [ ] 无语法错误

---

## LinkedIn BD最佳实践

### 适用场景

- 向潜在客户发送LinkedIn Connection请求
- 编写个性化的开发信
- B2B销售的初次触达
- 建立行业人脉

### Connection 请求最佳实践

#### 基础规则

1. **字符限制**：≤ 300字符（LinkedIn硬限制）
2. **个性化**：必须体现你了解对方
3. **价值导向**：说明连接对双方的价值
4. **无销售感**：首次连接不要直接推销

#### 开头方式

| 方式 | 示例 | 适用场景 |
|------|------|----------|
| 提及动态 | "Loved your post about..." | 对方活跃发帖 |
| 提及公司 | "I noticed {Company} is..." | 公司有新闻 |
| 共同连接 | "{Name} suggested I connect..." | 有共同人脉 |
| 行业话题 | "Fellow {行业} professional..." | 同行业 |
| 活动相关 | "Saw you're speaking at..." | 参加同一活动 |

#### 结尾方式

| 方式 | 示例 |
|------|------|
| 交流型 | "Would love to exchange ideas." |
| 学习型 | "Would love to learn from your experience." |
| 合作型 | "Would love to explore potential synergies." |
| 简洁型 | "Let's connect!" |

#### 示例库

**示例1：看到对方发帖**
```
Hi Sarah! Your recent post on AI in marketing really resonated.
I'm Morgan from MiniMax - we're building tools that help marketers
create video content at scale. Would love to connect and exchange ideas!
```

**示例2：提及公司动态**
```
Hi Mike, I noticed Acme is expanding into video content.
At MiniMax, we help companies like yours produce professional videos
10x faster with AI. Would love to connect!
```

**示例3：共同连接**
```
Hi Lisa, David Chen suggested I reach out. I'm working on AI video
generation at MiniMax - David mentioned you might be interested in
what we're building. Would love to connect!
```

**示例4：同一活动**
```
Hi Tom! Saw you're attending AI Summit next week. I'll be there too -
speaking about AI in content creation. Would love to connect beforehand
and maybe grab coffee at the event!
```

### Email 开发信最佳实践

#### 主题行技巧

**好的主题行**：
- "Quick question about {公司}的{业务}"
- "{共同联系人} suggested I reach out"
- "Idea for {公司}'s {挑战}"
- "{X}% improvement in {指标} - relevant?"

**避免的主题行**：
- "Partnership opportunity!!!!"（太销售）
- "Hi"（太模糊）
- 全大写字母
- 过多emoji

#### 开头钩子技巧

**有效钩子**：
```
I noticed {Company} recently announced {新闻}...
With {行业趋势}, companies like {Company} are facing {挑战}...
{共同联系人} mentioned you're looking into {话题}...
I've been following {Company}'s work on {项目} - impressive...
```

**无效钩子**：
```
I hope this email finds you well... （老套）
I'm reaching out to introduce... （太直接）
We are a leading provider of... （以自己为中心）
```

#### CTA技巧

**好的CTA**：
```
Would you be open to a quick 15-min call this week?
Do you have 15 minutes on [具体日期] to chat?
Reply with your availability and I'll send a calendar invite.
```

**避免的CTA**：
```
Let me know when you're free.（太模糊）
Can we schedule a demo?（太直接）
Please reply ASAP.（太急迫）
```

### 跟进策略

#### 跟进节奏

| 触点 | 时间 | 渠道 | 内容 |
|------|------|------|------|
| 1 | Day 0 | LinkedIn | Connection请求 |
| 2 | Day 3 | Email | 开发信 |
| 3 | Day 7 | LinkedIn | 如未连接，评论对方帖子 |
| 4 | Day 10 | Email | 跟进邮件（提供新价值） |
| 5 | Day 14 | LinkedIn | 再次发送Connection |

#### 跟进邮件模板

```
Subject: Re: [原主题]

Hi {Name},

Following up on my previous email.

I wanted to share {新的价值点/案例/内容} that might be relevant
given {公司}的{业务/挑战}.

Worth a quick chat?

Best,
{Your Name}
```

### 最佳发送时间

| 时间 | 效果 |
|------|------|
| 周二-周四 上午9-11点 | 最佳 |
| 周一 上午10点后 | 良好 |
| 周五 上午 | 可以 |
| 周末 | 避免 |
| 节假日前后 | 避免 |

### A/B测试建议

建议定期测试以下变量：

1. **主题行**：提问式 vs 陈述式
2. **开头**：提及动态 vs 提及公司
3. **价值点数量**：2个 vs 3个
4. **CTA**：具体时间 vs 开放时间
5. **长度**：简短 vs 详细
6. **语气**：正式 vs 轻松

追踪指标：
- LinkedIn连接接受率
- Email打开率
- Email回复率
- 会议预约率

---

## 标准化商机字段（15字段）

| 分类 | 字段名 | 说明 | 必填 |
|------|--------|------|------|
| 公司 | company_name | 公司名称 | ✅ |
| 公司 | company_description | 公司简介 | ✅ |
| 联系人 | contact_name | 决策人姓名 | ✅ |
| 联系人 | contact_title | 职位 | ✅ |
| 联系人 | linkedin_url | LinkedIn链接 | ✅ |
| 联系人 | email | 工作邮箱 | ✅ |
| 联系人 | phone | 电话 | ⚪ |
| 联系人 | personality_profile | 性格画像 | ⚪ |
| 商机 | source | 商机来源 | ✅ |
| 商机 | source_detail | 来源详情 | ⚪ |
| 商机 | opportunity_type | 商机类型 | ✅ |
| 商机 | priority | 优先级 | ✅ |
| 商机 | match_reason | 匹配原因 | ✅ |
| BD材料 | connection_message | LinkedIn话术 | ✅ |
| BD材料 | email_draft | Email草稿 | ✅ |

完整商机信息格式：

```yaml
# 公司信息
company_name: "{公司名称}"
company_description: "{公司简介/主营业务}"

# 联系人信息
contact_name: "{决策人姓名}"
contact_title: "{职位}"
linkedin_url: "{LinkedIn个人页面链接}"
email: "{工作邮箱}"
phone: "{电话}"  # 可选

# 性格画像
personality_profile:
  沟通风格: "{正式/轻松/简洁/详细}"
  关注重点: "{技术/商业/创新/效率}"
  决策风格: "{数据驱动/直觉型/共识型}"
  破冰话题: "{具体话题}"
  建议策略: "{个性化沟通建议}"

# 商机信息
source: "{商机来源}"
source_detail: "{来源详情}"
opportunity_type: "{商机类型}"
priority: "{高/中/低}"
match_reason: "{为什么是潜在客户}"

# BD材料
connection_message: "{LinkedIn话术}"
email_draft: "{Email草稿}"
```

---

## 日报输出格式

```markdown
# {产品名} 商机挖掘日报 - {日期}

## 📊 概览
| 指标 | 数量 |
|------|------|
| 竞品动态 | {X}条 |
| 企业合作情报 | {X}条 |
| 关键人物动态 | {X}条 |
| ✨ Connection挖掘 | {X}人 |
| **潜在商机合计** | **{X}个** |

## 1. 竞品动态
[竞品动态表格]

## 2. ✨ 竞品销售Connection挖掘
[Connection挖掘表格]

## 3. 潜在商机汇总
[15字段商机表格，按优先级排序]

## 4. 下一步行动建议
- 🔥 高优先级商机：建议今日发送Connection Request
- ⭐ 中优先级商机：建议本周跟进
- 📋 低优先级商机：加入培育列表
```

---

## 常见错误避免

### LinkedIn错误
- ❌ 直接推销产品
- ❌ 复制粘贴通用消息
- ❌ 超过300字符
- ❌ 没有说明为什么要连接
- ❌ 语法/拼写错误

### Email错误
- ❌ 主题行太长（显示不全）
- ❌ 正文太长（没人读完）
- ❌ 没有个性化开头
- ❌ 价值点不具体
- ❌ CTA不明确
- ❌ 附件过多
- ❌ 发送时间不当（周末/深夜）

### 流程错误
- ❌ 不确认配置就开始采集
- ❌ 忽略排除列表导致联系竞争对手
- ❌ 使用通用BD模板而不根据性格定制
- ❌ 商机信息不完整就生成BD材料
- ❌ 输出时不按优先级排序

---

## 注意事项

1. 每次执行前确认配置，用户可以调整竞品列表和目标人群
2. 优先使用竞品销售Connection挖掘渠道，这是质量最高的线索来源
3. 所有BD材料必须个性化，根据性格分析调整沟通风格
4. 确保所有商机包含完整15字段
5. 输出时按优先级排序，高优先级商机优先处理
6. 确保搜索时间范围准确，避免重复信息
7. 对每条信息标注原始来源URL
8. 重点关注商机信号，不只是新闻汇总
9. 评分要有明确依据，避免主观臆断
10. 每份BD材料必须高度个性化，禁止使用通用模板
11. CTA要简单易执行（15分钟电话，而非长会议）
12. 中文联系人可以生成中英双语版本
