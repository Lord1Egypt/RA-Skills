# B2B SEO KPI Framework & Reporting

## 指标体系设计原则

B2B SEO 的 KPI 体系与 B2C 有本质区别：
- **转化周期长**：从点击到成交可能 3-6 个月，须设计中间转化指标
- **流量质量 > 流量数量**：100 个精准访客胜过 10000 个泛流量
- **多触点归因**：B2B 买家通常经历多次搜索才转化

## 三层指标架构

### L1 — 商业成果指标 (Monthly Review)

| 指标 | 定义 | 数据源 | 目标设定 |
|------|------|--------|----------|
| Organic Revenue / Pipeline | 自然搜索直接或间接贡献的营收/商机金额 | CRM + GA4 | 环比 +15% |
| Organic Leads / MQLs | 自然搜索带来的线索/市场合格线索 | CRM, UTM 追踪 | 环比 +10% |
| Demo/Trial Requests | Demo 预约/试用申请数（来自自然搜索） | CRM 表单 | 环比 +10% |
| Organic Assisted Conversions | 自然搜索在转化路径中参与（非最后点击） | GA4 转化路径 | 首次建立基线 |
| Brand Search Volume | 品牌词搜索量变化 | GSC, SEMrush | 环比 +5% |

### L2 — 流量与排名指标 (Weekly Review)

| 指标 | 定义 | 数据源 |
|------|------|--------|
| Organic Sessions | 自然搜索会话数 | GA4 / GSC |
| Organic Users | 自然搜索独立用户数 | GA4 |
| Avg SERP Position | 所有追踪关键词平均排名 | SEMrush / Ahrefs |
| Keywords in Top 3 / Top 10 / Top 20 | 各排名区间的关键词数量 | 排名追踪工具 |
| Non-Brand Organic Traffic | 去品牌词后的自然搜索流量 | GSC（排除品牌词） |
| Click-Through Rate (CTR) | 搜索结果中点击率（按位置归一化） | GSC |
| New vs Returning Users | 新用户/回访用户比例 | GA4 |
| Pages per Session | 平均每次会话浏览页数 | GA4 |
| Avg Session Duration | 平均会话时长 | GA4 |

### L3 — 执行与健康指标 (Daily/Real-time)

| 指标 | 定义 | 数据源 |
|------|------|--------|
| Indexed Pages | 已被 Google 收录的页面数 | GSC Index Coverage |
| Crawl Errors | 抓取错误数（404/500/重定向错误等） | GSC Crawl Stats |
| Core Web Vitals Score | LCP/INP/CLS 评分 | GSC / PageSpeed Insights |
| Duplicate Title Tags | 重复 Title 的页面数 | Screaming Frog |
| Duplicate Meta Descriptions | 重复 Meta Description 的页面数 | Screaming Frog |
| Broken Internal Links | 损坏的内链数 | Screaming Frog |
| Missing Alt Text | 缺少 Alt 属性的图片数 | Screaming Frog |
| Orphan Pages | 无入链的孤立页面数 | Crawl analysis |
| Content Freshness Score | 超过 12 个月未更新的重要页面数 | CMS audit |
| New Content Published | 本周/本月新发布内容数 | CMS |

## B2B 特有转化漏斗指标

```
[Organic Traffic]
    ↓ [Engagement Rate: >60%]
[Engaged Visitors]
    ↓ [Micro-conversion Rate: >3%]
[Content Downloads / Newsletter Subs]
    ↓ [Lead Conversion Rate: >5%]
[MQLs / Demo Requests]
    ↓ [SQL Rate: >20%]
[Sales Accepted Leads]
    ↓ [Close Rate: >20%]
[Revenue]
```

### 微转化指标 (Micro-Conversions)

B2B SEO 必须关注微转化，因为这些是长周期转化的中间信号：

| 微转化事件 | 衡量标准 | 目标 |
|-----------|----------|------|
| 白皮书/报告下载 | 下载量 | 建立邮件线索库 |
| 案例研究查看 | 页面深度浏览 | 购买意向信号 |
| 定价页访问 | 定价页 PV | 高意向信号 |
| Demo 视频观看 | 视频完播率 | 产品兴趣信号 |
| 联系表单开始填写 | 表单交互 | 转化意向 |
| 博客订阅 | 新订阅数 | 长期培育 |
| 产品对比页浏览 | PV + 停留时间 | 决策阶段信号 |

## 归因模型

B2B SEO 应采用多点归因而非最后点击归因：

| 模型 | 适用场景 |
|------|----------|
| 首次点击归因 | 衡量 SEO 在引入新用户中的价值 |
| 线性归因 | 衡量 SEO 在整体转化路径中的持续贡献 |
| 时间衰减归因 | 衡量 SEO 在购买决策后期的助推作用 |
| 数据驱动归因 | 使用机器学习综合考虑所有触点（GA4 支持） |

## 汇报节奏

| 频率 | 受众 | 重点 | 报告形式 |
|------|------|------|----------|
| 周报 | 营销团队 | 执行进度、排名波动、技术警报 | 简短邮件 / Slack |
| 月报 | 营销总监 | 流量趋势、转化数据、竞品动态 | 详细 PPT / 看板 |
| 季报 | CMO / VP | ROI 分析、战略调整、资源分配 | 高管摘要 + 数据附件 |

## ROI 计算模型

```
SEO ROI = (Organic Revenue × SEO 贡献比例 - SEO 总成本) / SEO 总成本 × 100%

其中：
- SEO 总成本 = 人力成本 + 工具成本 + 内容制作成本 + 外链建设成本 + 技术开发成本
- 贡献比例 = 根据归因模型确定
```
