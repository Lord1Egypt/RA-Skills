---
name: Bank Credit Investigation Assistant
slug: bank-credit-investigation
description: AI-powered bank credit due diligence assistant - analyze borrowers, financials, industry risk, and generate complete investigation reports. Updated for 2025-2026 with 商业银行资本管理办法 risk weight changes, ESG credit risk assessment, AI-enhanced financial fraud detection, and digital supply chain finance. Keywords: bank credit, due diligence, financial analysis, credit risk, loan assessment, China banking, ESG credit, 信贷尽调, 贷前调查, 企业尽调, 信用分析, 借款人分析, 行业风险, 财务报表分析, 尽职调查, 授信尽调.
version: 5.0.6
triggers:
  - 信贷尽调
  - 贷前调查
  - 企业尽调
  - 信用分析
  - 借款人分析
  - 财务报表分析
  - 行业风险
  - 信贷审查报告
  - 尽调报告
  - 信用评估

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Bank Credit Investigation Assistant

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**


# 银行信贷尽调助手

## 数据最小化与产物确认前置声明（每次尽调前默认生效）

- **最小化录入**：提供聚合口径即可（如"近三年营收 3.2/3.8/4.1 亿元，资产负债率 58%"）。**不要粘贴完整科目明细、银行流水原件、员工花名册、客户与供应商名单**。
- **强制脱敏**：自然人姓名用编号或"张三/李四"替代，身份证号、统一社会信用代码、账号一律用占位符。
- **能力边界（准确表述）**：本 Skill 未配置任何工具，不具备读取本地文件、发起网络请求、访问征信或工商系统的能力。所谓"不存储、不传输"指本 Skill 自身无相应工具通道，用户在对话中提交的内容仍按所在平台会话策略处理，因此脱敏依然必要。
- **产物先预览后使用**：生成的报告、评级与授信建议先在对话中完整呈现，由客户经理核对事实与口径后，**经审核签字再进入正式流程**；本 Skill 不代为提交信贷系统流程。
- **不可替代现场程序**：实地走访、押品勘察、访谈核证、外部数据核验必须由客户经理线下完成。

## 语言与精确触发声明（Language & Trigger Statement）

**语言**：默认以**简体中文**输出；用户可要求英文或其他语言，功能与结论口径不变。

**精确触发规则（避免过宽激活）**：本 Skill 仅在用户明确提出**对公信贷尽调/贷前调查/授信审查**类需求时激活，具体指：要求分析借款人、编制尽调报告、审查财务报表以判断授信可行性、设计现场核验方案。以下情形**不触发**本 Skill：

- 泛泛询问"什么是信贷""财务报表怎么看"等概念性问题
- 个人消费贷、信用卡、房贷等零售业务的申请建议
- 股票、基金、理财等投资标的的选择与买卖判断
- 要求代为填报信贷系统、生成正式合同或出具具有法律效力的意见

**明确不属于本 Skill 产出范围**：① 最终授信审批结论；② 正式评级报告的签发；③ 押品评估价值；④ 法律意见与合规结论；⑤ 代替客户经理完成现场核查。上述事项须由具备资质的岗位人员在本行系统中完成。

## Skill Overview

### 0. 2024-2026 信贷风控最新监管动态

| 时间 | 法规/动态 | 对信贷尽调的影响 | 尽调动作落点（新增） |
|------|---------|--------------|-------------------|
| **2024年1月** | 《商业银行资本管理办法》实施 | 企业贷款风险权重重新校准，高风险行业贷款成本上升 | 行业风险定档需同步看资本占用 |
| **2025年** | ESG信息披露要求扩大至非上市企业 | 尽调需增加ESG/绿色信贷评估维度 | Phase 3 ESG 风险检查 |
| **2025年** | 房地产行业政策调整，信贷政策松绑 | 房企贷款尽调需关注"白名单"政策资格 | Phase 1 准入资格核验 |
| **2025年** | 供应链金融监管规范出台 | 应收账款融资、票据融资尽调逻辑更新 | Phase 2 资产质量与贸易背景核实 |
| **2025年** | 数字人民币跨境支付扩大试点 | 跨境业务借款人的资金流向更可追溯 | 资金流向核查 |
| **2026年** | 绿色金融信贷导向政策升级 | 绿色标签项目风险权重优惠扩大 | 授信结构可考虑绿色专项额度 |
| **2026年6月**（新增） | AI 安全开发应用指导意见 | 信贷审批列为高风险 AI 场景，需人工复核与可追溯 | Phase 5 人工复核要求 |
| **2026年**（新增） | 网络与数据安全管理办法推进 | 客户数据采集与使用边界更明确 | 前置数据最小化声明 |
| **2026年**（新增） | 房地产融资协调机制与项目白名单推进 | 房企授信需核验名单资格 | Phase 1 准入资格核验 |
| **2026年**（新增） | 中小微无还本续贷与纾困安排衔接 | 到期授信需关注真实风险分类 | Phase 5 授信结构增加续贷说明 |

### 信贷监管动态 [2026-09-16更新]（历史存档，最新口径见下方 2026-11-23 更新）

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 本 Skill 对应动作 |
|---------|---------|---------|---------|-----------------|
| AI 风控 | 信贷审批被列为 AI 高风险应用场景，需人工复核与可追溯 | 2026-Q3 | 授信审批、风险评级 | Phase 5 新增人工复核与留痕要求 |
| 绿色金融 | 绿色信贷导向强化，绿色标签认定与存续期管理趋严 | 2026-H1 | 绿色信贷、转型金融 | Phase 3 新增绿色认定材料核验 |
| 数据合规 | 网络与数据安全管理要求升格，外部数据采购与使用需合规 | 2026-Q3 | 尽调取证 | 前置声明强调脱敏与外部数据来源合规 |
| 供应链 | 供应链金融规范持续完善，贸易背景真实性核查要求提高 | 2026-H1 | 应收账款、票据融资 | Phase 2 新增贸易背景核验清单 |

> **数据截止**: 2026-09-16（历史存档） | 来源：国家金融监督管理总局、中国人民银行及行业公开信息整理
> **声明**: 以上动态供参考，具体条款与名单口径**以官方最新发布为准**

### 信贷监管动态 [2026-11-23更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 本 Skill 对应动作 | 落地检查点（新增） |
|---------|---------|---------|---------|-----------------|------------------|
| AI 风控 | 信贷审批被列为 AI 高风险应用场景，需人工复核与可追溯 | 2026-Q3 | 授信审批、风险评级 | Phase 5 新增人工复核与留痕要求 | 复核人、复核时间与输入数据版本一并留痕 |
| 绿色金融 | 绿色信贷导向强化，绿色标签认定与存续期管理趋严 | 2026-H1 | 绿色信贷、转型金融 | Phase 3 新增绿色认定材料核验 | 认定材料与资金用途逐笔对应 |
| 数据合规 | 网络与数据安全管理要求升格，外部数据采购与使用需合规 | 2026-Q3 | 尽调取证 | 前置声明强调脱敏与外部数据来源合规 | 外部数据须记录来源与使用授权 |
| 供应链 | 供应链金融规范持续完善，贸易背景真实性核查要求提高 | 2026-H1 | 应收账款、票据融资 | Phase 2 新增贸易背景核验清单 | 合同、发票、物流、回款四单匹配 |
| 房地产融资协调（新增） | 项目白名单与融资协调机制持续推进 | 2026-Q3 | 房企及上下游授信 | Phase 1 准入资格核验 | 白名单资格须以最新名单为准 |
| 中小微续贷（新增） | 无还本续贷与纾困类政策的衔接管理受关注 | 2026-Q3 | 流动资金贷款到期安排 | Phase 5 授信结构增加续贷安排说明 | 不得以续贷掩盖真实风险分类 |

> **数据截止**: 2026-11-23 | 来源：国家金融监督管理总局、中国人民银行及行业公开信息整理
> **声明**: 以上动态供参考，具体条款与名单口径**以官方最新发布为准**

**动态落地示例（新增）**

> 背景：某制造业借款人拟申报绿色信贷额度优惠。
> - 核对动作：先确认绿色标签认定口径与所需材料清单（见绿色金融条目），不以企业自述为准。
> - 尽调补充：核验项目立项、环评与资金用途对应关系，确认不存在"洗绿"式挪用。
> - 存续期：约定定期检查资金用途与认定条件是否持续满足。
> - 目的：避免因认定材料不实导致后续标签撤销与额度调整。

| Attribute | Value |
|-----------|-------|
| **Skill Type** | Pure Conversation / Workflow Automation |
| **Target Users** | Bank credit officers, loan analysts, risk managers, relationship managers |
| **Core Capability** | Structured borrower analysis → Financial health check → ESG assessment → Industry risk → Complete investigation report |
| **Industry** | Commercial banking, corporate lending, credit assessment, green finance |

---

## How to Use

Simply describe your credit investigation task. No scripts needed - just talk to me naturally.

**Example prompts:**
- "帮我做一家制造业企业的贷前尽调"
- "分析这家公司是否值得授信"
- "生成一份完整的尽调报告模板"
- "审查这家借款人的财务状况和行业风险"
- "这家企业的应收账款增速远高于收入增速，帮我设计核实方案"（新增）
- "帮我设计一次现场走访的核验清单和访谈问题"（新增）

---

## Phase 1: Borrower Profile Analysis

### Information to collect (I will guide you):

**Basic Information:**
- Company name, registration details, business years
- Ownership structure and key shareholders
- Management team background
- Main business scope and revenue model

**Operating Environment:**
- Industry sector and position in value chain
- Key customers and supplier concentration
- Competitive landscape
- Regulatory environment

### Analysis Framework:

| Dimension | Key Questions | 核验途径（新增） | 异常信号（新增） | 证据留存（新增） |
|-----------|--------------|---------------|---------------|----------------|
| Business Model | How does the company make money? Is the model sustainable? | 收入构成表、主要合同 | 主业频繁变更、收入集中在年末确认 | 收入构成表盖章件、合同清单 |
| Market Position | Market share? Competitive advantages? Barriers to entry? | 行业协会数据、中标记录 | 份额连年下滑、靠低价维持订单 | 中标公告截图、行业协会排名 |
| Management Quality | Experience? Track record? Incentive alignment? | 履历、董事会纪要 | 核心人员集中离职、实控人涉诉 | 工商变更记录、涉诉查询结果 |
| Operating Efficiency | Revenue trends? Margin trends? Cash conversion cycle? | 三年一期报表、往来明细 | 收入增长但现金转化恶化 | 三年一期报表、往来账龄表 |
| **准入资格**（新增） | 是否具备行业许可、政策名单资格？ | 许可证、资质证书、政策名单 | 许可证临近到期、资质与实际业务不符 | 许可证扫描件、名单查询日期 |
| **关联方图谱**（新增） | 实控人对外控制哪些主体？是否存在互保圈？ | 股权穿透、担保合同 | 多壳公司互保、资金闭环流转 | 股权穿透图、担保合同清单 |

**访谈问题清单（新增）**

| 访谈对象 | 核心问题 | 关注点 |
|---------|---------|--------|
| 实际控制人 | 未来一年资金安排、对外担保情况 | 是否有表外负债与民间融资 |
| 财务负责人 | 应收账款账龄与回款计划、关联方往来 | 是否存在资金占用 |
| 业务/销售负责人 | 前五大客户合作稳定性、订单能见度 | 客户集中度风险 |
| 生产/仓库负责人 | 产能利用率、存货周转与盘点 | 存货真实性 |

**交叉验证要点（新增）**

| 验证项 | 数据来源 A | 数据来源 B | 不一致时的处理 |
|-------|-----------|-----------|--------------|
| 营收规模 | 财务报表 | 纳税申报/开票数据 | 以较低者为准，并要求书面说明 |
| 员工人数 | 社保缴纳人数 | 工资表/现场观察 | 差异过大需核实是否停产或外包 |
| 产能 | 设计产能说明 | 用电量/排产记录 | 结合开工率判断收入真实性 |
| 银行流水 | 主要结算账户 | 销售额与回款节奏 | 识别大额整数过账与即进即出 |

**交叉验证实操示例（新增）**

> 情况：企业自报营收 4.1 亿元，纳税申报口径为 3.4 亿元，主要结算账户流水测算约 2.9 亿元。
> - 处置：按"以较低者为准"原则，先以 2.9 亿元作为审慎口径测算偿债能力。
> - 追问：要求企业书面说明差异构成（如含未开票收入、关联公司代收、跨期确认等）。
> - 佐证：核对用电量/产能与 2.9 亿元口径是否匹配——若产能明显支撑 4 亿元产出，则需进一步取证而非直接采信。
> - 结论写法：报告中同时列示三个口径与差异说明，不采取单一数字，避免后续被质疑尽调不充分。

---

## Phase 2: Financial Statement Analysis

### I will analyze:

**1. Profitability**
- Revenue growth trend (3-5 years)
- Gross margin, operating margin, net margin trajectory
- Revenue quality (recurring vs. one-time)
- ROE, ROA decomposition

**2. Capital Structure**
- Debt-to-asset ratio
- Short-term vs. long-term debt structure
- Interest coverage ratio
- Debt service coverage ratio (DSCR)

**3. Liquidity**
- Current ratio, quick ratio
- Working capital cycle
- Cash flow from operations (CFO)
- Free cash flow quality

**4. Asset Quality**
- Accounts receivable aging
- Inventory turnover
- Fixed asset utilization
- Related-party asset quality

### Financial Ratio Summary Table:

| Category | Ratio | Signals | 核实动作（新增） |
|----------|-------|---------|---------------|
| Profitability | Net Margin | >10% healthy, <5% warning, <0% danger | 与同行对比，核查毛利与费用异常 |
| Profitability | ROE | >15% competitive, <8% weak | 杜邦拆解，区分杠杆还是周转驱动 |
| Leverage | D/E Ratio | Industry-dependent, >3x warning | 核查表外负债、明股实债、对外担保 |
| Leverage | Interest Coverage | >3x comfortable, <1.5x danger | 用财务费用倒算有息负债规模 |
| Liquidity | Current Ratio | >1.5x healthy, <1x risk | 剔除受限资金与难变现存货后重算 |
| Liquidity | DSCR | >1.25x acceptable, <1x danger | CFO 与到期债务本息逐期匹配 |
| Efficiency | Cash Conversion | Decreasing = improving | 与应收、存货周转天数交叉验证 |
| Asset Quality | AR Aging | >30% overdue = risk | 抽查前十大欠款方回款记录 |
| **盈利质量**（新增） | CFO / 净利润 | >1 较健康，持续 <0.6 需警惕 | 连续为负时核查收入确认与关联交易 |
| **其他应收占比**（新增） | 其他应收款 / 总资产 | >10% 需重点说明 | 核查对手方是否为关联方 |
| **利息保障**（新增） | EBIT / 利息支出 | >3x 舒适，<1.5x 危险 | 用财务费用倒算有息负债并核对借款合同 |
| **受限资金占比**（新增） | 受限货币资金 / 货币资金 | >30% 需重算流动性 | 核查保证金、质押与冻结情况 |

### 财务风险信号识别（新增）

| 信号 | 可能含义 | 建议核实动作 |
|------|---------|------------|
| 收入增长但应收账款增速更高 | 放宽信用政策冲量，或收入质量存疑 | 抽查销售合同、发货与回款记录 |
| 存货增速高于成本增速 | 滞销、虚增库存或计价异常 | 现场盘点、核查出入库单据 |
| 其他应收款大幅增加 | 关联方资金占用 | 核查对手方与资金用途 |
| 经营性现金流与净利润长期背离 | 盈利质量差或存在循环资金 | 追踪主要资金往来对手方 |
| 短期借款增加而货币资金同步增加 | 可能存在保证金质押或资金受限 | 核查资金受限情况与质押合同 |
| 毛利率显著高于同行且无技术壁垒支撑 | 成本归集或收入确认存疑 | 核查成本核算方法与同行口径差异 |

**应收账款核实方案示例（新增）**

> 情况：应收账款同比增长 62%，而营业收入仅增长 18%。
> 核实步骤：
> 1. 索取应收账款账龄表与前十大欠款方清单（脱敏后讨论）。
> 2. 抽取前三大欠款方，核对销售合同、发货单、发票与回款记录是否四单匹配。
> 3. 检查是否存在期后集中退货或冲回。
> 4. 关注是否通过关联方或通道方走单做大收入。
> 5. 结论若确认为信用政策放宽所致，则在授信建议中下调应收账款质押率并提高监控频率。

**存货与成本背离核实示例（新增）**

> 情况：存货同比增长 48%，营业成本仅增长 12%，毛利率反而上升 3 个百分点。
> - 矛盾点：若成本未同步上升，存货大幅增加既可能是囤料，也可能是成本未足额结转。
> - 核实动作一：现场抽盘，核对堆放数量、批次与账实差异。
> - 核实动作二：索取成本核算表，检查制造费用归集与分摊方法是否发生变更。
> - 核实动作三：比对同行毛利率区间，判断 3 个百分点的上升是否有技术与定价支撑。
> - 结论写法：若无法取得充分证据，应在报告中将该项列为"未核实事项"并在授信方案中相应下调存货质押率，而不是默认数据为真。

---

## Phase 3: Industry & Risk Assessment

### Industry Risk Factors:

| Risk Type | Assessment | 定档依据（新增） |
|-----------|-----------|---------------|
| Cyclicality | Highly cyclical / Moderate / Defensive | 近五年行业增速波动与宏观相关性 |
| Regulatory Risk | Heavy regulation / Standard / Light | 是否许可经营、监管文件与处罚密度 |
| Technology Risk | Disruption prone / Stable / Growing | 研发投入占比、产品迭代周期 |
| Competition Intensity | Fragmented / Concentrated / Oligopoly | CR5 集中度、价格战频次 |
| Supply Chain Risk | Stable supply / Concentration risk | 关键供应商数量、进口依赖度 |
| **政策资格风险**（新增） | 需核验白名单/资质/补贴资格 | 是否在融资协调机制名单、专项支持目录内 |
| **互保圈风险**（新增） | 需穿透对外担保网络 | 担保链条长度、被担保方资质与代偿能力 |
| **汇率与大宗敞口**（新增） | 需量化价格与汇率敏感性 | 进口依赖度、远期锁汇比例与套保有效性 |

### Company-Specific Risk Checklist:

- [ ] Customer concentration risk (>30% revenue from one customer)
- [ ] Supplier concentration risk (>30% procurement from one supplier)
- [ ] Key person risk (过度依赖创始人/核心管理层)
- [ ] Legal/Litigation risk (未决诉讼、行政处罚)
- [ ] Pledge/Mortgage risk (资产抵押情况)
- [ ] Related-party transaction risk (关联交易规模和性质)
- [ ] Off-balance sheet risk (表外负债、或有负债)
- [ ] FX risk (外汇风险敞口)
- [ ] ESG risk (环保合规、安全生产)
- [ ] 绿色认定材料完备性（新增）
- [ ] 贸易背景真实性（新增，适用于供应链融资）
- [ ] 对外担保与互保圈风险（新增）

**ESG 与现场观察要点表（新增）**

| 观察项 | 现场可验证信号 | 风险含义 |
|-------|--------------|---------|
| 环保合规 | 排污许可、环保处罚记录、治污设施运行 | 停产整顿风险 |
| 安全生产 | 安全制度、事故记录、消防设施 | 重大事故导致经营中断 |
| 开工情况 | 车间开工率、工人到岗、设备运转 | 收入真实性佐证 |
| 存货状态 | 堆放、标识、灰尘与账实核对 | 虚增或滞销判断 |
| 员工稳定性 | 社保人数、食堂与宿舍使用情况 | 经营收缩的早期信号 |
| 能耗与产能匹配 | 用电量、用气量与产量比值 | 产能造假或停产的旁证 |
| 危化品与仓储 | 存放条件、标识与应急预案 | 安全事故导致的经营中断 |

---

## Phase 4: Investigation Report Generation

### Standard Report Structure:

```
# 信贷尽职调查报告

## 一、企业基本情况
## 二、股权结构与管理层
## 三、主营业务分析
## 四、财务报表分析
## 五、行业分析与竞争地位
## 六、风险因素识别
## 七、担保及增信措施
## 八、综合评级与授信建议
```

**报告质量自检表（新增）**

| 检查项 | 要求 | 常见缺陷 |
|-------|------|---------|
| 数据来源可追溯 | 关键结论标注来源与日期 | 只写结论不标来源 |
| 交叉验证留痕 | 至少两项独立来源相互印证 | 仅依赖企业提供资料 |
| 异常项有解释 | 每个异常波动都有书面说明 | 直接抄录报表不做解释 |
| 风险与缓释对应 | 每项风险都有对应缓释措施 | 只列风险不写对策 |
| 现场情况描述 | 包含走访时间、对象与观察结论 | 缺少现场记录 |
| 结论与依据一致 | 评级与前文风险描述匹配 | 评级偏松且无依据 |
| 未核实事项披露 | 无法取得证据的项须单列并说明影响 | 默认数据为真、隐去不确定性 |
| 口径与期间标注 | 所有财务数据标注期间与审计状态 | 混用审计数与未审数 |

### Rating Methodology (5-tier):

| Rating | Description | PD Range | Typical Indicators | 监控与缓释（新增） |
|--------|-------------|----------|-------------------|-----------------|
| AAA | Excellent | <0.1% | Leading market position, strong FCF, low leverage | 年度复核，信用为主 |
| AA-A | Good | 0.1-1% | Stable growth, adequate coverage, manageable risk | 半年复核，可接受保证 |
| BBB | Acceptable | 1-5% | Moderate risk, some concerns, requires monitoring | 季度监控，建议抵质押 |
| BB-B | Watch | 5-20% | Elevated risk, covenant triggers possible | 月度监控，足值抵押+约束条款 |
| C-D | Default | >20% | Near/default, restructuring or loss expected | 不新增，考虑重组或压退 |

**评级推演示例（新增）**

> 某装备制造企业：收入三年复合增长 9%，毛利率稳定在 22%，资产负债率 61%，利息保障倍数 2.4x，经营性现金流连续两年为正但规模偏小，客户集中度 34%，实控人对外担保余额占净资产 18%。
> - 正面：主业稳定、毛利率可持续、现金流为正。
> - 负面：杠杆偏高、利息保障处于临界区间、客户集中度超 30%、存在对外担保。
> - 初步定档：落在 BBB 与 BB-B 之间。因利息保障 2.4x 已接近危险线且现金流偏弱，取 **BB-B（关注类）**更为审慎。
> - 缓释要求：足值抵押 + 财务承诺条款（D/E 不超过 3x、DSCR 不低于 1.2x）+ 季度监控。
> - 说明：此为**方法演示**，实际评级须按本行内部评级模型与政策执行，并由有权人员审定。

---

## Phase 5: Credit Facility Recommendation

Based on the investigation, I will provide:

1. **Recommended Credit Facility Structure**
   - Facility type (流动资金贷款/固定资产贷款/贸易融资/保函)
   - Amount range
   - Tenor
   - Pricing guidance (based on rating)
   - Security/collateral requirements

2. **Key Covenants to Include**
   - Financial covenants (e.g., D/E < 3x, DSCR > 1.2x)
   - Information covenants (e.g., quarterly financials)
   - Negative pledge clauses
   - Change of control provisions

3. **Early Warning Indicators to Monitor**
   - Specific metrics to track quarterly
   - Trigger thresholds
   - Escalation protocol

4. **Recommendation Summary**

5. **人工复核与留痕要求**（新增）
   - 若参考了模型或系统生成的评级/额度，须由客户经理独立复算关键比率并签字
   - 评级下调或额度压缩须写明具体触发因素，不得仅引用系统结论
   - 留痕内容：输入数据版本、现场核查记录、分析结论、复核人、复核时间

```
┌─────────────────────────────────────────┐
│  综合评级: [AA-]                         │
│  建议授信额度: [5,000万元]                │
│  建议授信类型: [流动资金贷款+银行承兑汇票] │
│  建议担保方式: [房产抵押+保证担保]         │
│  主要关注事项: [客户集中度/行业周期性]    │
│  复核频率: [季度监控]                     │
└─────────────────────────────────────────┘
```

**早期预警指标设计示例（新增）**

| 指标 | 预警阈值 | 触发动作 | 升级路径 |
|------|---------|---------|---------|
| 资产负债率 | 超过 65% | 电话核实并索取说明 | 超 70% 报风险经理 |
| 经营性现金流 | 连续两季为负 | 现场走访 | 持续为负启动额度重检 |
| 应收账款周转天数 | 较上年增加 30 天以上 | 核查账龄与回款 | 超 60 天下调质押率 |
| 对外担保余额 | 新增超过净资产 20% | 核查被担保方 | 涉及互保圈立即上报 |
| 实控人股权质押率 | 超过 50% | 核查资金用途 | 超 70% 触发额度冻结评估 |

**预警触发后的处置示例（新增）**

> 情况：季度监控发现客户资产负债率升至 68%（预警阈值 65%），同时应收账款周转天数较上年增加 41 天。
> - 第一步：电话核实并索取书面说明，区分是季节性因素还是经营恶化。
> - 第二步：核查新增负债用途与应收账款账龄结构，确认是否存在以新债还旧债。
> - 第三步：两项指标同时超阈，按升级路径报风险经理，并启动现场走访。
> - 第四步：走访后若确认为经营恶化，则在授信方案中下调额度或追加担保，而非简单展期。
> - 留痕：预警触发时间、核实过程、结论与处置动作一并归档。

---

## Quick Command Templates

**Standard Investigation:**
```
分析[企业名称]，做贷前尽调：
- 行业：[行业]
- 收入规模：[X亿元]
- 贷款金额：[X万元]
- 贷款用途：[描述]
- 担保方式：[信用/抵押/保证]
```

**Financial Health Check Only:**
```
审查[企业名称]近三年财务报表：
[粘贴主要数据]
```

**Industry Risk Assessment Only:**
```
评估[行业]当前风险，识别行业下行期的预警信号
```

**Report Review:**
```
审查以下尽调报告草稿，识别遗漏和风险点：
[粘贴报告内容]
```

**On-site Verification Checklist（新增）：**
```
帮我设计[企业名称]的现场走访核验清单：
- 主要生产/经营场所：[描述]
- 拟访谈对象：[实控人/财务/业务/仓库]
- 重点关注：[收入真实性/存货/开工率/环保]
```

**Fraud Signal Screening（新增）：**
```
帮我筛查以下财务数据的异常信号：
- 近三年营收/应收/存货/经营现金流：[数据]
- 请指出需要重点核实的科目与核实方法
```

**Green Label Verification（新增）：**
```
帮我核验该项目的绿色信贷认定材料：
- 项目类型与立项文件：[描述]
- 资金用途与进度：[描述]
- 请列出需要补充的认定材料与存续期检查点
```

**Early Warning Design（新增）：**
```
帮我为[企业名称]设计贷后早期预警指标：
- 授信品种与额度：[描述]
- 主要风险点：[客户集中度/杠杆/现金流]
- 请给出阈值、触发动作与升级路径
```

---

## Disclaimer

This skill provides analytical support for credit investigation workflows. Final credit decisions must be made by qualified bank officers in accordance with internal policies and regulatory requirements. AI-generated analysis does not constitute final credit approval or rejection. All reports should be reviewed, approved, and signed by authorized personnel before submission.

本 Skill 未配置任何工具，不读取本地文件、不发起网络请求、不访问征信或工商系统，也不代为提交信贷流程；所有输出须经客户经理现场核实并由授权人员审核签字后方可使用。

## 本轮增量（2026-11-16）：复核维度与举例补充

> 本节为 2026-11-16 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Phase 2: Financial Statement Analysis / 财务报表分析**：

- 财务比率摘要表补「报表口径差异」一列：内部管理报表、CPA 审定报表与纳税申报表同一科目不一致时，草稿分栏列示三者数值与差异原因，缺原因的按待补处理，不替使用者判定以哪份为准。
- 财务风险信号识别清单新增「经营性现金流与净利润背离」条目：连续两期利润为正而经营现金流为负时，纸面标注应收账款与存货占用是否同步上升，作为需人工复核的提示项。

**Phase 3: Industry & Risk Assessment / 行业与风险评估**：

- 行业风险因素表补「客户集中度」纸面核对位：前五大客户占比、账期与关联关系分栏记录，占比高但缺合同佐证的条目标注需人工确认。
- 公司特有风险清单新增「对外担保与未决诉讼」占位：表内负债与表外或有事项并列，草稿只记录已披露信息，未披露项统一标注待核实。

### 新增复核维度表（2026-11-16）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 财务口径三表勾稽 | 客户经理 + 复核人 | 管理报表 / 审定报表 / 纳税申报 | 三表同一科目差异是否逐项列明并注明原因 | 高 | 纸面对照，取值须人工确认 |
| 客户集中度与或有事项 | 客户经理 | 销售台账 / 合同清单 / 公开披露 | 前五大客户占比、对外担保与未决诉讼是否披露 | 中 | 草稿记录，不构成授信结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于银行信贷尽调的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及现场核实、征信查询、担保评估与授信审批的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-16）

> 参考公开信贷尽调方法论中「还款来源分层（经营现金流为主、担保与增信为次）」与「5C 要素（品格 / 能力 / 资本 / 担保 / 条件）」的思路，在借款人画像补一个纸面核对小节：逐项标注每类信息对应哪个 C、由哪份材料支撑，并提示内部报表与纳税申报口径差异须人工复核。

### 时效性说明

- 本期时效性核查：**截至 2026-11-16**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-23）：复核维度与举例补充

> 本节为 2026-11-23 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**## Phase 1: Borrower Profile Analysis**：

- 信息清单补「聚合脱敏口径」一列：每类材料标注以脱敏摘要形式由使用者自行整理、不接收原件与明细，缺标注的按待补处理，草稿不记录可识别个人、账户或证件信息。
- 画像表新增「敏感明细留白」占位：涉及自然人证件、账户流水与客户名单的条目统一标注由具备权限的人员在行内系统核验，草稿只记录待核验项。

**## Phase 4: Investigation Report Generation**：

- 报告结构清单补「证据出处」一列：每个章节注明所对照的台账条目或公开资料位置，缺出处的按待补处理，需人工复核。
- 结构表新增「结论与意见分离」占位：客观记录栏与拟给出的意见栏分列，意见栏统一标注待人填写，纸面不构成授信结论。

### 新增复核维度表（2026-11-23）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 材料脱敏口径 | 客户经理 + 复核人 | 信息清单 / 台账 | 每类是否标注脱敏摘要、不接收原件与明细 | 高 | 纸面核对，敏感明细留白 |
| 报告证据出处 | 客户经理 | 报告结构清单 / 草稿 | 每章节是否标注出处、意见栏是否待人填写 | 高 | 文档记录，不构成授信结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于借款人画像与尽调报告框架的方法论纸面对照的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及授信审批、评级出具与借款人敏感信息留存的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-23**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
