# 搜索策略与关键词模板

## 通用搜索模板

### 按公司名搜索

```
# 基础信息
"{公司名}" company overview
"{公司名}" founded headquarters CEO
"{公司名}" about us

# 融资信息（大中型公司适用）
"{公司名}" funding round investment
"{公司名}" crunchbase
"{公司名}" valuation revenue

# 产品业务
"{公司名}" product features pricing
"{公司名}" customers case study
"{公司名}" business model

# 社交媒体
site:linkedin.com/company "{公司名}"
site:x.com "{公司名}" OR site:twitter.com "{公司名}"

# 新闻舆情
"{公司名}" news
"{公司名}" controversy scandal
"{公司名}" lawsuit legal

# 竞品分析
"{公司名}" competitors alternatives
"{行业关键词}" top companies
similar companies to "{公司名}"
```

### 按邮箱域名搜索

```
# 域名归属
"{域名}" company owner
site:{域名}
"{域名}" WHOIS domain registration

# 域名关联公司
"{域名}" email company
"@{域名}" company

# 域名历史
site:web.archive.org "{域名}"
"{域名}" wayback machine

# 邮件格式探测
"{域名}" email format pattern
"{域名}" email convention
site:hunter.io "{域名}"
site:email-format.com "{域名}"
```

## SME（中小企业）专用搜索策略

中小企业的信息通常稀少，以下平台和策略更有效：

```
# 本地商业名录（按国家选择）
"{公司名}" site:yellow.co.nz          # 新西兰 Yellow Pages
"{公司名}" site:yelp.com              # 美国 Yelp
"{公司名}" site:hotfrog.com           # 全球商业目录
"{公司名}" site:fyple.co.nz           # 新西兰企业目录
"{公司名}" site:provenexpert.com      # 企业评价平台

# 本地电商平台
"{公司名}" site:trademe.co.nz         # 新西兰 Trade Me
"{公司名}" site:alibaba.com           # 阿里巴巴国际站

# 商业协会
"{公司名}" chamber of commerce
"{公司名}" business association

# Google 商家信息
"{公司名}" Google Maps reviews
"{公司名}" Google My Business

# 本地新闻（SME 更可能在本地媒体出现）
"{公司名}" local news
"{公司名}" community newspaper
```

## 增强搜索渠道使用指南

### 1. 专利/知识产权搜索

适用于：科技、制造、医药、消费电子等有研发投入的公司

```
# Google Patents
"{公司名}" site:patents.google.com

# 美国专利商标局
"{公司名}" site:uspto.gov trademark
"{公司名}" USPTO patent assignment

# WIPO 国际专利
"{公司名}" site:wipo.int patent

# 专利数量和价值评估
"{公司名}" patent portfolio
"{公司名}" intellectual property
```

**判断价值**：
- 专利数量多 → 研发实力强、技术壁垒高
- 近期有新专利 → 持续创新
- 专利诉讼 → 可能面临 IP 风险或主动维权

### 2. 政府合同搜索

适用于：美国政府供应商、国防承包商、IT 服务商

```
# 美国联邦支出
"{公司名}" site:usaspending.gov

# 联邦承包商注册
"{公司名}" site:sam.gov

# 政府合同
"{公司名}" government contract award
"{公司名}" federal contract

# 国防合同（如适用）
"{公司名}" Department of Defense contract
"{公司名}" defense contractor
```

**判断价值**：
- 有政府合同 → 财务稳定性较高（政府付款可靠）
- 合同金额大 → 规模和实力验证
- 合同类型 → 了解公司核心业务方向

### 3. 进出口数据搜索

适用于：贸易公司、制造商、跨境电商

```
# 进出口记录
"{公司名}" Panjiva OR ImportGenius
"{公司名}" import export records
"{公司名}" shipment data

# 海关数据
"{公司名}" customs data
"{公司名}" bill of lading

# 供应链关系
"{公司名}" supplier OR vendor OR distributor
```

**判断价值**：
- 进出口量 → 真实业务规模
- 供应商/客户 → 供应链关系和依赖度
- 贸易伙伴国家 → 市场分布和地缘风险

### 4. 招聘信息搜索

适用于：所有公司（推断规模和方向）

```
# 主流招聘平台
"{公司名}" site:indeed.com jobs
"{公司名}" site:glassdoor.com jobs
"{公司名}" site:linkedin.com/jobs

# 官网招聘页
site:{公司域名}/careers
site:{公司域名}/jobs

# 招聘趋势
"{公司名}" hiring 2025 2026
"{公司名}" job openings careers

# 裁员信号
"{公司名}" layoffs OR firing OR downsizing
"{公司名}" site:layoffs.fyi
```

**判断价值**：
- 大量招聘 → 扩张信号，业务向好
- 重点招聘方向 → 战略重点（如大量招 AI = AI 转型）
- 裁员信息 → 财务压力或业务收缩
- 岗位数量 → 估算实际规模

### 5. 技术栈检测

适用于：科技/SaaS/电商/互联网公司

```
# BuiltWith 技术栈分析
"{公司名}" site:builtwith.com
"{公司域名}" builtwith technology profile

# Wappalyzer
"{公司域名}" wappalyzer tech stack

# 工程博客/技术栈
"{公司名}" engineering blog tech stack
"{公司名}" stackshare

# GitHub（开发者公司）
"{公司名}" site:github.com
```

**判断价值**：
- 技术栈先进 → 研发能力评估
- 使用的云服务 → 规模估算（AWS/Azure/GCP 费用等级）
- 开源项目 → 开发者社区影响力

### 6. BBB（美国商业改善局）

适用于：美国 B2C/B2B 公司、消费者/零售公司

```
"{公司名}" site:bbb.org
"{公司名}" Better Business Bureau rating
"{公司名}" BBB accreditation
"{公司名}" BBB complaints
```

**判断价值**：
- BBB 评级 → A+ 到 F，直接反映信誉
- 投诉数量和处理方式 → 客户服务态度
- 认证状态 → 是否主动维护信誉

### 7. OpenCorporates 全球注册验证

适用于：所有公司（交叉验证注册信息）

```
"{公司名}" site:opencorporates.com
"{公司名}" corporate registration worldwide
```

**判断价值**：
- 多国注册记录 → 跨国经营证据
- 注册状态 → 是否正常运营
- 关联公司 → 子公司/母公司关系
- 董事信息 → 关键决策者

### 8. 制裁/合规筛查（所有公司必做）

国际贸易合规底线，无论公司规模都必须检查：

```
# OFAC（美国财政部海外资产控制办公室）
"{公司名}" OFAC sanctions
"{公司名}" site:treasury.gov OFAC
"{公司名}" SDN list

# EU 制裁名单
"{公司名}" EU sanctions list
"{公司名}" European Union restrictive measures

# 联合国制裁
"{公司名}" United Nations sanctions

# 英国制裁
"{公司名}" site:gov.uk financial sanctions

# 综合筛查
"{公司名}" sanctions screening
"{公司名}" denied parties list
"{公司名}" entity list
```

**判断价值**：
- 在制裁名单上 → **禁止交易**，立即终止合作
- 在观察名单 → 高风险，需合规团队审核
- 不在任何名单 → 通过基本合规检查

### 9. WikiData/Wikipedia

适用于：大型/知名公司

```
"{公司名}" site:en.wikipedia.org
"{公司名}" wikidata
"{公司名}" wikipedia company
```

**判断价值**：
- 有 Wikipedia 页面 → 知名度较高
- 页面内容全面 → 信息交叉验证
- 页面争议标记 → 需谨慎对待

### 10. 应用商店搜索

适用于：有移动应用的 SaaS/消费类公司

```
"{公司名}" site:apps.apple.com
"{公司名}" site:play.google.com
"{公司名}" app store rating reviews
```

**判断价值**：
- 评分和评论 → 产品质量和用户满意度
- 下载量估算 → 用户规模
- 更新频率 → 产品维护状况

### 11. 专业评测平台

适用于：SaaS/软件/B2B 服务公司

```
# G2
"{公司名}" site:g2.com

# Capterra
"{公司名}" site:capterra.com

# Trustpilot
"{公司名}" site:trustpilot.com

# Gartner Peer Insights
"{公司名}" site:gartner.com reviews

# Software Advice
"{公司名}" site:softwareadvice.com
```

### 12. 学术引用搜索

适用于：研究型/医药/生物科技公司

```
"{公司名}" site:scholar.google.com
"{公司名}" research paper publication
"{公司名}" clinical trial results
```

### 13. 行业论坛/社区搜索

适用于：科技/消费类公司（了解真实用户反馈）

```
"{公司名}" site:reddit.com
"{公司名}" site:quora.com
"{公司名}" forum discussion community
```

**注意**：论坛信息为 D 级来源（匿名/个人观点），仅作参考，不作为评估依据

## 行业特殊搜索策略

### 科技/SaaS 公司

```
site:github.com "{公司名}"
"{公司名}" API documentation
"{公司名}" tech stack engineering blog
"{公司名}" open source projects
site:producthunt.com "{公司名}"
site:g2.com "{公司名}"
site:capterra.com "{公司名}"
```

### 电商/零售公司

```
"{公司名}" marketplace sellers
"{公司名}" revenue GMV
"{公司名}" shipping fulfillment
site:trustpilot.com "{公司名}"
site:bbb.org "{公司名}"
"{公司名}" site:apps.apple.com OR site:play.google.com
```

### 金融/Fintech 公司

```
"{公司名}" regulatory license
"{公司名}" SEC filing
site:sec.gov "{公司名}"
"{公司名}" compliance audit
"{公司名}" financial statements
"{公司名}" banking license charter
```

### 医疗/生物科技公司

```
"{公司名}" FDA approval clinical trial
site:clinicaltrials.gov "{公司名}"
"{公司名}" patent research
"{公司名}" medical device approval
"{公司名}" site:scholar.google.com
```

### 制造业公司

```
"{公司名}" factory manufacturing facility
"{公司名}" supply chain suppliers
"{公司名}" certifications ISO
"{公司名}" production capacity
"{公司名}" Panjiva OR ImportGenius
```

### 仓储/物流公司

```
"{公司名}" warehouse distribution
"{公司名}" 3PL logistics
"{公司名}" pallet handling equipment
"{公司名}" freight forwarding
```

### 建筑/工程公司

```
"{公司名}" construction projects
"{公司名}" building permits
"{公司名}" contractor license
"{公司名}" safety violations OSHA
```

### 咨询/专业服务公司

```
"{公司名}" consulting clients
"{公司名}" thought leadership reports
"{公司名}" partners directors
site:glassdoor.com "{公司名}"
```

## 各国/地区工商注册查询

| 地区 | 注册平台 | 查询方式 | 是否免费 |
|------|---------|---------|---------|
| 新西兰 | Companies Office | companies-register.companiesoffice.govt.nz/search | 免费 |
| 澳大利亚 | ASIC | search.asic.gov.au | 免费（基本信息） |
| 美国（各州不同） | Secretary of State | 各州官网查询 | 多数免费 |
| 美国（全国） | SEC Edgar | site:sec.gov "{公司名}" | 免费 |
| 美国（全球注册） | OpenCorporates | opencorporates.com | 免费（基本信息） |
| 英国 | Companies House | find-and-update.company-information.service.gov.uk | 免费 |
| 德国 | Handelsregister | "{公司名}" Handelsregister | 部分付费 |
| 法国 | INPI / SIRENE | data.insee.fr | 免费 |
| 日本 | 法人番号公表サイト | hojin.k.go.jp | 免费 |
| 新加坡 | ACRA | bizfile.acra.gov.sg | 部分付费 |
| 中国香港 | 公司注册处 | icris.cr.gov.hk | 部分付费 |
| 加拿大 | 各省注册处 | 因省而异 | 多数免费 |
| 韩国 | DART | dart.fss.or.kr | 免费 |
| 印度 | MCA | mca.gov.in | 部分付费 |
| 荷兰 | KvK | kvk.nl | 免费（基本信息） |
| 瑞士 | ZEFIX | zefix.admin.ch | 免费 |

### 工商注册查询搜索模板

```
# 通用方法：搜索公司名 + 国家 + 注册
"{公司名}" {国家} company registration number
"{公司名}" {国家} business number

# 直接访问注册平台搜索
# 进入对应国家的注册平台网站，输入公司名搜索
# 提取：注册号、注册日期、注册地址、董事信息、公司状态
```

## 物理存在验证搜索模板

```
# Google Maps 验证
"{公司名}" Google Maps
"{公司地址}" Google Street View

# 虚拟办公室识别
"{公司地址}" virtual office OR coworking
"{公司地址}" registered agent

# WHOIS 域名查询
"{域名}" WHOIS lookup
"{域名}" domain registration date

# Wayback Machine（网站历史）
site:web.archive.org "{域名}"
"{域名}" wayback machine history
```

## 联系方式采集搜索模板

在背调全流程中，任何渠道发现的联系方式都必须记录：

```
# 官网联系页（最优先）
site:{公司域名}/contact
site:{公司域名}/about
site:{公司域名}/team

# 关键人员 LinkedIn
"{公司名}" CEO OR founder OR director site:linkedin.com/in
"{关键人名}" LinkedIn

# 社交媒体账号
"{公司名}" site:linkedin.com/company
"{公司名}" site:x.com OR site:twitter.com
"{公司名}" site:facebook.com
"{公司名}" site:instagram.com
"{公司名}" site:youtube.com

# 邮件格式推断
"{域名}" email format
site:rocketreach.co "{公司名}"
site:zoominfo.com "{公司名}"
site:apollo.io "{公司名}"

# 多地办公室
"{公司名}" office locations
"{公司名}" branch offices
"{公司名}" headquarters address phone

# 客服/售后
"{公司名}" customer service contact
"{公司名}" support email phone
```

## 信息可信度评估等级

| 等级 | 来源类型 | 示例 |
|------|---------|------|
| A（高） | 官方注册信息、政府网站 | SEC filing, Companies House, 工商注册, OFAC |
| B（中高） | 权威媒体、行业报告 | TechCrunch, Forbes, Gartner, 行业协会 |
| C（中） | 社交媒体、员工评价、本地商业名录 | LinkedIn, Glassdoor, Yellow Pages, BBB |
| D（低） | 匿名论坛、个人博客 | Reddit, Quora, 个人网站 |
| E（待验证） | 无法溯源的信息 | 无来源声称 |

在报告中引用信息时，标注来源可信度等级，如："据 TechCrunch 报道（B级来源）"

## 常见陷阱与规避

### 同名公司混淆
- 搜索 "Arrow" 可能出现 Arrow Electronics（美上市巨头）、Arrow Warehousing（NZ SME）等
- **规避方法**：每次搜索都附加国家/行业限定词，确认结果属于目标公司后再采信
- **报告规则**：如果发现近似名公司，在报告中明确声明"本报告仅针对 XXX，与 YYY 无关"

### 虚假/过时信息
- 有些公司网站长期不更新，地址可能已变更
- **规避方法**：交叉验证 — 官网地址 vs Google Maps 地址 vs 工商注册地址
- 注意注册地址与经营地址可能不同

### SME 信息稀缺
- 小公司可能在所有第三方平台都无记录
- **规避方法**：降低预期，重点验证物理存在（地址、电话、Google Maps）
- 如果仅能通过官网和本地名录确认存在，可给出"信息有限但无负面记录"的评估

### 制裁名单误命中
- 常见名称可能命中制裁名单中的同名不同实体
- **规避方法**：交叉验证地址、行业、国家等维度确认是否为同一实体
- 如无法确认，在报告中标注"可能命中制裁名单，需人工复核"

### 联系方式时效性
- 员工离职后邮箱/电话可能失效
- 公司搬迁后电话可能变更
- **规避方法**：标注来源时间和可信度，建议用户发送前先验证
