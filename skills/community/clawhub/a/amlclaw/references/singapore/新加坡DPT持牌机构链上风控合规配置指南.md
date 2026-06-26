这是一份专为持有新加坡 DPT（数字支付代币）牌照 ，特别是从事 OTC（场外交易） 业务的企业设计的 TrustIn KYA Pro 反洗钱（AML）与反恐融资（CFT）配置策略文档。本指南深度融合了 TrustIn 最新的 AML 标签分类体系，严格依据 新加坡金融管理局 (MAS) 的监管要求（包括 2025 年修订的 PSN02 通知）、新加坡警方 (SPF) STRO 发布的红旗指标以及 TSOFA / 联合国法案 制定。
--------------------------------------------------------------------------------
1. 核心风控标签与风险等级映射 
根据 TrustIn 最新的标签分类体系，系统内必须将以下地址标签映射至对应的风险等级，以触发不同的风控动作。
A. 严重风险 (SEVERE) - 零容忍绝对拦截
此类风险涉及 MAS 及新加坡法律的红线，必须立即拦截、冻结并考虑上报：
• 制裁 (Sanctions)：制裁实体 (Sanctioned Entity)、制裁管辖区 (Sanctioned Jurisdiction)、发出限制的国家/地址 (Prohibited Entity Singapore)。
• 恐怖主义融资 (Terrorism Financing)：恐怖组织 (Terrorist Organization)。
• 其他金融犯罪 (Other Financial Crimes) & 执法冻结 (Public Freezing Action)：涉嫌洗钱 (Suspected Money Laundering)、执法机构冻结 (Law Enforcement Freeze/Seizure)。
• 非法市场 (Illicit Markets)：人口贩卖 (Human Trafficking)、非法服务 (Illegal Services)、儿童虐待 (Child Sexual Abuse Material/CSAM)。
B. 高风险 (HIGH) - 拒绝交易或强制 EDD
此类风险高度契合 SG-010 红旗指标中的洗钱上游犯罪及资金混淆手段：
• 网络犯罪 (Cybercrime)：被盗资金 (Hacker/Thief)、勒索软件 (Ransomware)、网络钓鱼 (Phishing)、庞氏骗局 (Ponzi)、杀猪盘 (Pig Butchering)、项目方跑路 (Rug Pull)、蜜罐合约 (Honeypot)、虚假预售 (Fake Presale)。
• 混淆/隐私 (Obfuscation)：混币器 (Mixers)、隐私钱包 (Privacy Wallet)、隐私代币 (Privacy Token)、中心化跨链桥服务 (Centralized Bridge)、加密货币ATM (Crypto ATM)。
• 博彩 (Gambling)：无牌照博彩 (Unlicensed Gambling)。
• 高风险实体 (High-Risk Entities)：高风险地区交易所 (CEX in High-Risk Jurisdiction)、被制裁交易所 (Sanctioned CEX)、弱AML/CFT管控交易所 (CEX with Weak AML/CFT Controls)、场外交易平台 (OTC Desk)、高风险跨链桥服务 (High-Risk Bridges)。
C. 中风险 (MEDIUM) - 触发人工审核/关注
• 网络犯罪：黑/灰产交易 (Black/Grey Industry)。
• 辅助类实体：MEV机器人/套利 (MEV Bots/Arbitrage)、垃圾交易/空投 (Spam)。
D. 低风险 (LOW) - 正常放行与白名单
• 交易所 & 去中心化金融协议 (Exchanges & DeFi)：中心化交易所 (CEX)、传统金融机构 (TradFi)、DeFi 协议、DEX、CDP、衍生品协议、收益创造协议、跨链桥服务 (Bridges)、NFT市场等。
• 辅助类 (Other Entities)：稳定币发行 (Stablecoin)、资金托管服务商 (Custodian)、多签钱包 (Multisig Wallet)、自托管钱包 (Self-custody Wallet) 等。
--------------------------------------------------------------------------------
2. 规则引擎配置与阈值设定 (Rule Engine & Thresholds)
针对 OTC 业务大额、低频、高风险的特点，建议在 TrustIn KYA Pro 中配置以下核心规则：
2.1 资金来源与去向追踪逻辑
• 资金来源审查 (Inflow)：追溯资金上游，穿透深度建议设置为 5 Hops (5层)，以有效防止犯罪分子通过 Peel Chains（剥离链）进行分层 (Layering) 洗钱。
• 资金去向监控 (Outflow)：监控提币目标地址及其下游，穿透深度建议设置为 3-5 Hops，确保识别资金是否流向恐怖组织或受制裁实体。
• 白名单机制 (Whitelist)：必须开启，将低风险的合规 CEX (如 Binance, Coinbase) 热钱包加入白名单，TrustIn 的穿透阻断机制将在遇到白名单时停止，有效降低误报率。
2.2 阈值与逻辑的具体设置
在 Fund 规则中，建议使用逻辑组合来平衡风控与业务体验，避免恶意的“粉尘攻击”(Dusting Attack) 导致误杀：
• 严重风险 (SEVERE) 规则：
    ◦ 触发逻辑：Percentage > 0% OR Direct Interaction（只要包含 0.01% 的受制裁/恐融资金，或有直接交互）。
    ◦ 应对措施：Block (冻结/拦截)。
• 高风险 (HIGH) 规则：
    ◦ 触发逻辑：Percentage > 10% AND Risk Amount > 50 USD。
    ◦ 应对措施：Reject (拒绝交易) 或要求客户提供增强尽职调查 (EDD)。过滤掉 50 USD 以下的资金可防范黑客的微量粉尘脏币。
• 中风险 (MEDIUM) 规则：
    ◦ 触发逻辑：Percentage > 30% AND Risk Amount > 1,000 USD。
    ◦ 应对措施：要求确认资金来源 (Source of Funds) 的合法性。
2.3 交互行为检测 (匹配 MAS 法规门槛)
• 转账规则 (Travel Rule)：单笔转账 **> 1,000USD∗∗(约合S1,350)，触发中风险 (Medium) 警报，系统强制要求填写受益人 VASP 信息。
• CDD 触发阈值：偶然交易金额 **> 3,500USD∗∗(约合S4,700)，触发高风险 (High) 警报，强制执行完整的 KYC/CDD 流程。
• 拆分交易警报 (Structuring Alert)：单日累计入金 > $3,000 USD，触发高风险 (High) 警报，警惕客户通过“蚂蚁搬家”规避 CDD 审查。
--------------------------------------------------------------------------------
3. 事后监控配置 (Ongoing Monitoring)
MAS 要求 DPT 服务商必须进行持续监控。建议在 TrustIn 系统中针对存量客户地址开启以下功能：
1. 每日回溯筛查 (Daily Screening)：
    ◦ 区块链标签具有动态性，需监控存量高净值客户的白名单地址。
    ◦ 触发条件：地址风险评分从 Low (低风险) 突变为 High/Severe (高/严重风险)，或新增与制裁名单 (Sanction List) 的交互。
2. 交易模式监控 (Transaction Pattern Monitoring)：
    ◦ 快进快出 (Rapid Movement)：资金充值后极短时间内全额提走。
    ◦ 拆分 (Structuring)：检测 24 小时内多次低于 S$5,000 的入金行为。
    ◦ 行为不符 (Inconsistent Activity)：交易量突然激增，与客户申报的财务状况不符。
--------------------------------------------------------------------------------
4. 操作流程与合规文档留存 (SOP & Record Keeping)
根据 MAS PSN02 规定，业务人员需严格执行以下操作流程：
1. 交易前 (Pre-Trade)：
    ◦ 将客户钱包地址输入 TrustIn KYA Pro 进行筛查。
    ◦ 导出并存档 PDF 报告；若提币金额超过阈值，必须通过 Travel Rule 协议（如 Sygna, Notabene）发送 IVMS101 标准信息。
2. 警报处理 (Alert Handling)：
    ◦ 触发 HIGH 警报时，必须由合规官 (Compliance Officer) 介入。
    ◦ 执行 EDD 措施，要求客户提供资金来源证明。若客户无法合理解释资金为何涉及高风险标签（如混币器），必须向 STRO 提交 STR (可疑交易报告)。
3. 记录留存 (Record Retention)：
    ◦ 所有 TrustIn 分析报告、客户解释文件、STR 提交记录必须依法保存至少 5 年