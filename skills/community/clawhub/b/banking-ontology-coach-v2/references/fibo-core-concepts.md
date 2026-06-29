# 银行 FIBO 概念索引（离线对标主力；联网时以官方源为准）

覆盖银行建模最常用的 FIBO 概念，按域组织。每条给：概念名、所属域、大白话定义、关键父类/关系、是否"角色"。
**本文件是离线参照，覆盖有限。** 据此对标时一律标注"来源：内置离线数据，IRI 待核验"；精确定义与 IRI 以 spec.edmcouncil.org/fibo 官方源为准。角色类（标〔角色〕）一律用 PartyInRole 模式，不要立成独立类型。

## FND 基础域（Foundations）

- **Party（当事方）**：能在各种情境中扮演角色的实体（自然人或组织）。是"角色"模式的根。
- **PartyInRole（当事方角色）**：把"某当事方在某情境/合约中担任某角色"显式建模的模式。**所有〔角色〕概念都挂在这里。**
- **Agreement / Contract（协议 / 合约）**：当事方间达成、产生权利义务的约定。与"金融工具"区分。
- **Commitment / Obligation（承诺 / 义务）**：合约产生的应履行事项。
- **AutonomousAgent / Person / Organization（自治主体/自然人/组织）**：Party 之下的主要分支。
- 通用件：日期、时间区间、货币金额、地理位置、标识体系等。

## BE 业务实体域（Business Entities）

- **LegalEntity（法人实体）**：有法律人格、能独立担责、订立合约的组织。KYC 的"客户主体"常落于此。
- **LegalPerson / NaturalPerson（法人 / 自然人）**：与 LegalEntity 配套，自然人 vs 法人之分。
- **OwnershipAndControl（所有权与控制）**：股权、控制关系建模族。**受益所有权链、穿透识别建在这里。**
- **BeneficialOwner〔角色〕（受益所有人）**：通过所有权/控制链对某法人享有最终权益的自然人。
- **CorporateStructure（公司结构）**：母子公司、分支机构、集团结构。
- **FormalOrganization / GovernmentEntity（正式组织/政府实体）**：组织类型细分。

## FBC 金融商业域（Financial Business and Commerce）

- **FinancialInstitution / Intermediary〔部分角色〕（金融机构/中介）**：银行、券商等市场参与机构。
- **Bank（银行）**：FinancialInstitution 的子类。
- **Regulator〔角色〕（监管者）**：在监管情境中担任的角色。
- **FinancialInstrument（金融工具）**：代表金融价值或债权债务关系的工具（合约的标的，与协议本身区分）。
- **FinancialProduct / FinancialService（金融产品/服务）**：机构提供的产品与服务。
- **Account / FinancialAccount（账户）**：金融账户。
- **MarketInfrastructure（市场基础设施）**：交易所、清算所、支付系统等。

## SEC 证券域（Securities）

- **Security（证券）**：可交易的金融工具，FinancialInstrument 的子类。
- **Equity / Share（股权/股票）**、**DebtInstrument / Bond（债务工具/债券）**：证券主要分支。
- **Issuer〔角色〕（发行人）**、**Holder / Investor〔角色〕（持有人/投资者）**：证券情境中的角色。
- **Issuance（发行）**：证券发行事件。

## LOAN 贷款域（Loans）

- **Loan（贷款）**：一种债务安排（注意：贷款"协议"是 Agreement，贷款这一金融工具是其标的，分清）。
- **LoanContract / CreditAgreement（贷款合约/授信协议）**：合约层面。
- **Borrower〔角色〕（借款人）**、**Lender〔角色〕（贷款人）**、**Guarantor〔角色〕（担保人）**：贷款情境中的角色。
- **Collateral（担保物）**、**RepaymentSchedule（还款计划）**、**InterestRate（利率）**：贷款相关概念。

## DER 衍生品域（Derivatives）

- **Derivative（衍生品）**：价值依赖于标的的金融工具，FinancialInstrument 子类。
- **Swap / Option / Future / Forward（互换/期权/期货/远期）**：常见衍生品类型（如 InterestRateSwap 利率互换）。
- **Counterparty〔角色〕（对手方）**：衍生品/交易合约中担任的角色——**典型的"角色非类型"，用 PartyInRole**。
- **UnderlyingAsset（标的资产）**、**NotionalAmount（名义本金）**：衍生品相关概念。

## 其余按需的域
- **IND 指数与指标、CAE 公司行为与事件、BP 业务流程、MD 市场数据**：涉及时再去官方源对应域检索。

## 用法
对标某概念时：先按"它像哪个域"翻到对应段落找现成的；命中就在文档"FIBO 出处"列写"复用/特化/自有扩展 + 域 + 概念名 + 来源：内置离线数据，IRI 待核验"。命中不了再回 `fibo-reference.md` 的"查→复用→特化→扩展"四步流程；有联网工具的，优先去官方源检索精确结果。
