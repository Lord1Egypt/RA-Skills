# 报告模板 / Report Template

## 语言模式 / Language Mode

- 默认使用用户提问的语言作答。  
  Answer in the user's language by default.
- 用户要求双语输出时，每个章节标题、表头及表格单元格在可行范围内均按“中文在前、英文紧随其后”呈现；不要先给出整份中文版、再给出整份英文版。  
  When bilingual output is requested, place Chinese first and English immediately after each section heading, table heading, and table cell wherever practical; do not separate the response into a complete Chinese version followed by a complete English version.
- 专有名称、证号、统一社会信用代码、日期、数值及来源链接可共用一次，但其字段标签和解释仍须遵守上述语言顺序。不得因翻译省略事实、限定语、警示、证据等级或来源。  
  Proper names, certificate numbers, unified social credit codes, dates, figures, and source links may appear once, but their labels and explanations must follow the same language order. Translation must not omit facts, qualifications, warnings, evidence grades, or sources.

## 目录 / Contents

1. 固定输出顺序 / Required order
2. 匹配度诊断 / Match diagnosis
3. 全机构对比矩阵表 / Comparison matrix
4. 逐家深度透视 / Per-agency deep dive
5. 合同条款 / Contract clauses

## 1. 固定输出顺序 / Required Order

严格按以下中文名称和顺序输出；英文仅作紧随其后的对应说明：  
Use the following Chinese titles in exactly this order; add the English equivalent immediately after each title:

1. 匹配度诊断 / Match Diagnosis
2. 全机构对比矩阵表 / All-Agency Comparison Matrix
3. 逐家深度透视 / Per-Agency Deep Dive
4. 通用防坑条款＋初创机构专属补充协议 / General Risk-Prevention Clauses + Startup-Specific Addendum

先给出法律基线与覆盖范围结论，并注明审计日期。  
Lead with the legal-baseline and coverage conclusions, and state the audit date.

## 2. 匹配度诊断 / Match Diagnosis

必须包括：  
Include:

- 用户画像摘要；信息缺失时写“信息未提供，成功率不可测”。  
  A user-profile summary; if information is missing, write “信息未提供，成功率不可测 / Information not provided; success probability cannot be measured.”
- 目标国家/项目的可行性；仅在用户输入和官方规则均足以支持时给出概率区间。  
  Target-country/project feasibility; give a probability range only when both user inputs and official rules support it.
- 主要资格缺口、预算/时间风险，以及所需机构能力。  
  Major eligibility gaps, budget/timeline risks, and the agency capabilities required.
- 法律基线：历史许可与现行登记必须分开说明。  
  Legal baseline: distinguish historical licences from current registration.
- 分母说明：哪些范围已穷尽、哪些只是有日期的数据快照、哪些仍是公开检索样本。  
  Denominator statement: identify what is exhaustive, what is only a dated snapshot, and what remains a public-search sample.

## 3. 全机构对比矩阵表 / All-Agency Comparison Matrix

至少使用以下必备列，并完整保留下列中文措辞；双语输出时，在同一表头和单元格内先中文、后英文：  
Use at least the following required columns and preserve the Chinese wording exactly; in bilingual output, place Chinese before English within each heading and cell:

| 机构名称<br>Agency name | 核心擅长业务<br>Core expertise | 营销引流话术<br>Marketing lead-generation claims | 真实客诉与风险雷区<br>Documented complaints and risk red flags | 综合得分<br>Overall score | 详细扣分理由<br>Detailed deductions |
|---|---|---|---|---:|---|

在“机构名称”内写明准确法律实体及品牌/分支角色。每行还须明确以下项目；为提高可读性可增列：  
Within “机构名称 / Agency name,” state the exact legal entity and its brand/branch role. Each row must also make the following explicit; add columns if this improves readability:

- 现行“留学+因私出入境”专项许可状态；  
  current “study-abroad + private entry/exit” special-licence status;
- 历史证号及有日期的来源（如有）；  
  historical certificate number and dated source, if any;
- 梯队；  
  tier;
- 证据覆盖率百分比及评分置信度；  
  evidence-coverage percentage and score confidence;
- 审计日期。  
  audit date.

每个独立法律实体单列一行。不得把初创、小型、移民导向、低曝光或渠道型机构合并为“其他”。  
Give every independent legal entity its own row. Do not merge startup, small, migration-led, low-exposure, or channel-based entities into “其他 / Other.”

无法取得现行完整名录时，须在矩阵前写明：  
When no current exhaustive register is accessible, place this notice before the matrix:

> 本表穷尽的是[明确的数据快照/查询结果]，不是无法验证召回率的整个市场。公开检索未覆盖的主体不等于不存在。  
> This table exhausts [specified data snapshot/query results], not the entire market whose search recall cannot be verified. An entity absent from public-search results is not necessarily nonexistent.

## 4. 逐家深度透视 / Per-Agency Deep Dive

对矩阵中的每一行分别重复以下完整区块：  
Repeat this complete block independently for every matrix row:

```markdown
### [品牌名] / [Brand]｜合同主体 / Contracting entity：[法定全称] / [Full legal name]

- 梯队 / Tier：
- 成立/存续 / Establishment & status：成立日期、年限、状态、注册资本、地址、统一社会信用代码 / establishment date, age, status, registered capital, address, and unified social credit code
- 现行合规 / Current compliance：经营范围；两项旧许可的现行状态；其他项目专属许可 / business scope; current status of the two former licences; other project-specific licences
- 历史资质 / Historical qualifications：证号、名单日期、有效期或取消说明 / certificate number, roster date, validity period, or cancellation note
- 团队体量 / Team scale：参保年度/人数、招聘岗位、可确认的顾问与文书关系 / social-insurance reporting year/headcount, recruited roles, and verifiable consultant/writer relationships
- 文书与交付 / Application drafting & delivery：自营/外包/待核；证据与合同约束 / in-house, outsourced, or pending verification; evidence and contractual controls
- 渠道模式 / Channel model：直营、加盟、分销、合作方或待核 / direct operation, franchise, distribution, partner, or pending verification
- 业务与案例 / Services & cases：国家/项目、可核案例数量、案例归属及可比性 / countries/projects, number of verifiable cases, case ownership, and comparability
- 营销话术 / Marketing claims：原始表达、发布日期、来源及事实核验 / original wording, publication date, source, and factual verification
- 客诉与监管 / Complaints & regulatory record：投诉/处罚/裁判/执行/回应；不得把未决争议写成定论 / complaints, penalties, judgments, enforcement, and responses; do not present an unresolved dispute as a finding
- 项目风险包装 / Presentation of project risks：被书面披露与被淡化的政策、资金、续签、经营、税务风险 / policy, funding, renewal, operating, and tax risks disclosed in writing or downplayed
- 得分 / Score：X/10；证据覆盖率 / evidence coverage Y%；置信度 / confidence
- 逐项扣分 / Itemized deductions：每项事实、来源等级、日期和分值 / fact, source grade, date, and points for each deduction
- 审计结论 / Audit conclusion：适合/条件适合/高风险/证据不足；不以规模替代判断 / suitable, conditionally suitable, high risk, or insufficient evidence; do not substitute size for judgment
- 签约前必索材料 / Required pre-contract materials：3–8项机构特定材料 / 3–8 agency-specific items
```

初创机构必须达到相同审计深度，并追加：  
Give a startup the same depth and add:

- 关键人员离职保障；  
  key-person departure protection;
- 运营现金及付款分期；  
  operating cash and payment staging;
- 海外项目方身份及许可；  
  identity and licences of overseas project parties;
- 持续经营/备用交付方案；  
  business-continuity/backup delivery plan;
- 已完成案例的分母；  
  denominator of completed cases;
- 员工与合作方/渠道方的交付占比。  
  delivery split between employees and partners/channels.

## 5. 合同条款 / Contract Clauses

### 通用补充协议 / General Addendum

条款必须覆盖：  
Require clauses covering:

1. 法律实体、统一社会信用代码、公章、收款和开票主体一致；  
   consistency among the legal entity, unified social credit code, company seal, payment recipient, and invoice issuer;
2. 不得把已取消的历史证书表述为现行专项许可；  
   no representation of cancelled historical certificates as current special licences;
3. 具名顾问、文书、案件经理及海外受监管顾问；  
   named consultant, writer, case manager, and overseas regulated adviser;
4. 未经书面同意不得转让、外包或更换人员，并约定救济；  
   no assignment, outsourcing, or staff replacement without written consent and an agreed remedy;
5. 客户控制并审批申请账户及提交材料；  
   customer control and approval of application accounts and submitted materials;
6. 逐项列明境内外费用、佣金及第三方收款方；  
   itemized domestic/overseas fees, commissions, and third-party recipients;
7. 里程碑付款、退款触发条件、计算方式及办结期限；  
   milestone payments, refund triggers, calculation method, and completion deadline;
8. 标明版本的官方政策来源及书面下行风险披露；  
   versioned official policy sources and written downside-risk disclosure;
9. 不得保证录取、签证、永久居留或入籍；  
   no guaranteed admission, visa, permanent residence, or citizenship;
10. 数据返还/删除、违约责任、证据留存及争议解决地。  
    data return/deletion, breach liability, evidence retention, and dispute forum.

### 初创移民导向机构专属条款 / Startup Migration-Led Agency Clauses

另加：  
Add:

1. 低首付款、按里程碑放款；避免大额不可退预付款；  
   a low initial payment with milestone release; avoid a large non-refundable advance;
2. 员工/承包方名册，并书面披露每个交付合作方；  
   an employee/contractor roster and written disclosure of every delivery partner;
3. 创始人/关键人员离职后的解约及按比例退款；  
   termination and pro-rata refund after a founder/key person departs;
4. 直接向具名海外律师/项目方付款，并取得合同和收据；  
   direct payment to a named overseas lawyer/project party, supported by a contract and receipt;
5. 可核验的同类案例，并禁止跨实体借用案例；  
   verifiable comparable cases and a prohibition on borrowing cases across entities;
6. 政策变化、渠道失效、停业及交付中断的救济；  
   remedies for policy changes, channel failure, shutdown, and delivery interruption;
7. 禁止个人账户收款或单方替换项目；  
   no personal-account collection or unilateral project substitution;
8. 对隐瞒外包、虚构团队或歪曲历史资质，客户享有全额退款/解约权。  
   a full-refund/termination right for concealed outsourcing, false team claims, or misrepresented historical qualifications.

条款须针对已审计事实定制。不得把通用条款表述为法律意见或可执行性保证；高金额移民合同应建议当地律师复核。  
Tailor the clauses to the audited facts. Do not present general clauses as legal advice or as a guarantee of enforceability; recommend review by local counsel for high-value immigration contracts.
