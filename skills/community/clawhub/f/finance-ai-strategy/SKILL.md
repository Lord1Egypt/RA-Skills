---
name: Financial AI Strategy Architect
slug: finance-ai-strategy
description: 帮助金融机构制定AI转型战略、评估AI投资优先级、设计AI治理框架，从数字金融迈向数智金融的战略规划指导。融合阿里百技图Agent体系与保险AI应用研究报告精华。
version: "5.2.0"
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - code-examples-reference
triggers:
  - finance-ai-strategy
  - finance-ai-strategy-architect
---

# SKILL.md

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供金融机构AI转型的战略分析框架，**不执行任何代码或脚本**
> - 所有战略建议均为参考性输出，**不能替代专业咨询团队的深度调研**
> - 不收集、不存储用户的任何机构数据、业务数据或个人信息
> - 监管合规信息请以国家金融监督管理总局（NFRA）官方文件为准
> - 文中涉及的行业数据、案例仅用于方法论说明，不构成对特定产品或供应商的推荐

## Identity

**⚠️ 精确触发规则**：仅当用户明确需要制定AI转型战略、评估AI投资优先级、设计AI治理框架等**金融AI战略规划类**话题时激活。日常对话提及"AI"、"战略"、"转型"、"数字化"等通用词汇时**不会自动触发**。

**用户确认规则**：匹配以下关键词时，需先向用户确认后再进入战略规划模式：
- "您需要金融AI战略规划支持吗？请注意：本技能输出仅供内部参考，不构成投资建议。确认继续？"

- **Skill Name**: 金融AI战略规划师 (Financial AI Strategy Architect)
- **Slug**: finance-ai-strategy
- **Version**: 5.2.0
- **Language**: 中文为主，英文关键术语保留
- **Author**: 葛成 (@gechengling)
- **Description**: 以麦肯锡方法论为体、阿里百技图Agent体系为用、保险AI研究报告为证，帮助金融机构制定从"数字"到"数智"的AI转型战略。
- **Key References**:
  - 阿里百技图：Agent生产力公式、金融AI雇员全景、多智能体协作框架
  - 保险AI研究报告：MCP/A2A生态、LLM选型策略、行业最佳实践
  - 麦肯锡：三地平线、MECE诊断、ROI评估方法论

---

## Core Thinking Models

### 模型一：金融AI三大视界（麦肯锡三地平线框架）

```
┌─────────────────────────────────────────────────────────────┐
│              金融AI战略 — 三大视界（Three Horizons）           │
├──────────────┬──────────────────┬────────────────────────────┤
│  Horizon 1    │  Horizon 2        │  Horizon 3                  │
│  (0-12个月)   │  (12-36个月)      │  (36-60个月)                │
├──────────────┼──────────────────┼────────────────────────────┤
│ 运营效率革命  │ 客户体验重塑      │ 商业模式创新                │
│              │                  │                            │
│ • 智能客服    │ • AI Agent投保    │ • AI原生保险产品            │
│ • 文档自动化  │ • 个性化产品推荐  │ • 动态定价2.0              │
│ • 智能理赔    │ • 全渠道客户旅程  │ • 去中介化平台              │
│ • RPA升级     │ • 多模态交互      │ • 生态化金融服务            │
├──────────────┼──────────────────┼────────────────────────────┤
│ 典型场景：    │ 典型场景：         │ 典型场景：                  │
│ 核保自动化   │ Agent驱动的理赔    │ 自主风控决策体系            │
│ 智能客服     │ 智能投顾           │ AI原生保险产品              │
│ 报表生成     │ 个性化营销         │ 开放银行/保险平台           │
├──────────────┴──────────────────┴────────────────────────────┤
│ 核心原则：Horizon 1 造血 → Horizon 2 蓄力 → Horizon 3 领跑   │
│ "先赋能、再替代、最后创新"                                  │
└─────────────────────────────────────────────────────────────┘
```

### 模型二：AI就绪度诊断（MECE框架）

**六大维度评估金融机构AI就绪度**：

| 维度 | 评估指标 | L1 初始级 | L3 发展级 | L5 领先级 |
|------|---------|-----------|-----------|----------|
| **战略** | AI在董事会优先级 | 未列入议程 | 专项AI委员会 | AI驱动战略决策 |
| **数据** | 数据基础建设 | 手工报表为主 | 统一数据中台 | 实时数据+知识图谱 |
| **技术** | AI基础设施 | 单点POC | MCP/A2A架构落地 | AI原生技术栈 |
| **人才** | AI团队配置 | 0-5人外包 | 20-50人内外部混编 | 200+ AI原生团队 |
| **治理** | AI风控体系 | 无明确规范 | 模型台账+三方审计 | 实时AI监管沙盒 |
| **生态** | 外部合作 | 单一供应商 | 多供应商+开源混合 | 自研+社区贡献+标准制定 |

**诊断方法论**（MECE逻辑树）：
```
金融机构AI就熟度
├── 能力维度（内部）
│   ├── 数据基础（数据中台、数据质量、数据合规）
│   ├── 技术能力（算力、模型、工程化）
│   ├── 人才储备（AI团队、培训体系、文化接受度）
│   └── 组织架构（AI部门定位、决策流程、激励机制）
│
├── 战略维度（顶层设计）
│   ├── 愿景清晰度（是否明确AI战略定位）
│   ├── 资源投入（预算、人力、管理层承诺）
│   └── 路线图（分阶段目标、里程碑）
│
└── 环境维度（外部）
    ├── 监管要求（NFRA/CBIRC合规）
    ├── 市场竞争（同行进度、技术替代风险）
    └── 技术演进（MCP/A2A、多模态、Agent）
```

### 模型三：Agent生产力公式（阿里百技图精华）

**AI Agent = 大模型(LLM) × 工具生态(MCP/A2A) × 业务流程(RPA/Workflow)**

```
Agent生产力公式：

             协作系数 α
    Productivity = (LLM能力 × 工具生态 × 流程数字化)  
                   ─────────────────────────────
                        治理成本 + 风险系数

其中：
- LLM能力: 推理、多模态、长上下文、Function Calling
- 工具生态: MCP服务器数量、A2A协议成熟度、API覆盖度
- 流程数字化: 业务流程数字化率、数据可获取性
- 协作系数α: 多Agent协作效率（单Agent=1, 多Agent=1.5-3）
- 治理成本: 安全审计、合规检查、模型监控的人力投入
```

**Agent能力层级**（L1-L3渐进路线）：

| 层级 | 名称 | 能力特征 | 金融适用场景 |
|------|------|---------|------------|
| **L1** | 工具型Agent | 单一任务、规则驱动、有限感知 | 报表生成、文档处理、智能客服 |
| **L2** | 分析型Agent | 多步骤推理、信息检索、人机协作 | 核保辅助、理赔初审、风险分析 |
| **L3** | 决策型Agent | 自主规划、多工具调用、持续学习 | 资产配置、动态风控、反欺诈 |

**金融AI雇员全景**（阿里百技图推荐的10类核心AI Agent角色）：

| Agent类型 | 核心能力 | 适用岗位替代/赋能 |
|-----------|---------|-----------------|
| 财务分析官 | 财报分析·估值模型·行业对比 | 信用分析师、投资经理 |
| 风险管理师 | 风险识别·模型监控·压力测试 | 风控专员、合规经理 |
| 理赔处理官 | 影像审核·赔付计算·反欺诈 | 理赔调查员 |
| 承保核保师 | 风险定价·保单审核·再保安排 | 核保员 |
| 客户服务官 | 智能问答·情感分析·投诉处理 | 客服代表 |
| 研究分析师 | 研报生成·数据挖掘·趋势预测 | 研究员 |
| 投资顾问 | 资产配置·组合优化·市场分析 | 投资顾问 |
| 合规审查官 | 政策解读·违规检测·报告生成 | 合规专员 |
| 数据科学家 | 模型开发·特征工程·A/B测试 | 数据分析师 |
| 反欺诈分析师 | 异常检测·关联图谱·规则引擎 | 反欺诈专员 |

### 模型四：场景优先级矩阵（价值×可行性）

```
Y轴（商业价值）：高/中/低
X轴（技术可行性）：高/中/低

四象限排序策略：

1️⃣ 高价值+高可行 → 立即规模化（2026-2027 Q1-Q2）
   - 智能客服（85%替代率，已大规模验证）
   - 文档处理（70%效率提升，技术成熟）
   - 风控决策（决策时效<3秒，模型稳定）

2️⃣ 高价值+低可行 → 预研+试点（2026-2027 Q3-Q4）
   - Agent驱动的投资顾问（监管待明确）
   - 全自动核保引擎（需解决可解释性）
   - 多Agent协作理赔（技术仍在演进）

3️⃣ 低价值+高可行 → 快速试水（2026 Q1-Q2）
   - 智能质检（部署简单，ROI中等）
   - 报表自动化（工具成熟）

4️⃣ 低价值+低可行 → 暂缓/外包
   - 通用客服（非核心能力）
   - 数据标注（可外包）
```

### 模型五：大模型选型与MCP/A2A生态

**LLM选型四维评估矩阵**：

| 评估维度 | 闭源（GPT/Claude） | 开源（Qwen/DeepSeek/Llama） | 垂直金融模型 |
|---------|-------------------|---------------------------|------------|
| 推理能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 多模态 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 金融知识 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 成本效益 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 数据安全 | ⭐⭐（数据出境风险） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 生态兼容 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**MCP/A2A协议生态（2026年现状）**：

| 协议 | 发起方 | 定位 | 金融行业适配度 |
|------|--------|------|--------------|
| **MCP** (Model Context Protocol) | Anthropic → Linux AAIF治理 | 模型与外部系统通信标准（类似TCP/IP） | ⭐⭐⭐⭐⭐ 1000+服务器，50+官方 |
| **A2A** (Agent-to-Agent) | Google | 多Agent间协作通信 | ⭐⭐⭐⭐ Agent协作标准 |
| **Function Calling** | OpenAI | 单模型工具调用 | ⭐⭐⭐ 基础能力，已广泛支持 |

**选型推荐**（麦肯锡式决策树）：
```
数据敏感度？
├── 高（监管数据）→ 开源模型本地部署（Qwen/DeepSeek）
│   └── 是否需多模态？
│       ├── 是 → Qwen-VL / DeepSeek-VL
│       └── 否 → Qwen3 / DeepSeek-R1
│
└── 低（非敏感场景）→ 闭源API（Claude/GPT）
    └── 是否需长上下文？
        ├── 是 → Gemini 2M Token / Claude 200K
        └── 否 → GPT-4o / Claude Sonnet 4
```

### 模型六：AI治理金字塔（合规框架）

```
┌─────────────────────────────────────────┐
│           顶层：AI战略层                  │
│  AI伦理委员会 · AI战略委员会 · NFRA监督 │
├─────────────────────────────────────────┤
│         二层：AI治理委员会                │
│  跨部门协调 · 模型风险管治 · 合规审计    │
├─────────────────────────────────────────┤
│         三层：AI运营规范                  │
│  模型全生命周期管理 · 数据治理 · 算法公平 │
│  · 可解释性 · 偏差监控(±5%应急机制)     │
├─────────────────────────────────────────┤
│         四层：技术基础设施                 │
│  安全审计 · 隐私保护 · 模型监控 · 灾备    │
│  · MCP连接安全 · A2A通信加密             │
└─────────────────────────────────────────┘

2026年监管新要求（中国人民银行）：
1. 建立AI模型台账，重大模型变更须经独立第三方审计
2. 模型偏差超±5%须启动应急机制
3. 金融科技伦理委员会：算法公平性/透明度/可解释性纳入年度评级
4. 数据要素×金融：企业数据资产入表，数据质量评分纳入央行评级
```

### 模型七：AI项目ROI评估（麦肯锡方法论）

**三层次ROI评估**：

```
第一层：直接成本节约
  = 人力替代 × 人均成本 + 效率提升 × 时间价值 + 错误减少 × 损失避免

第二层：间接收益
  = 客户满意度提升 × 留存率 × CLV + 交叉销售率提升 × 平均客单价

第三层：战略价值（量化）
  = 数据资产积累 + 技术能力沉淀 + 品牌溢价 + 监管合规成本降低

推荐指标：
- Payback Period（回收期）：建议<18个月
- IRR（内部收益率）：目标>25%
- ROI（3年）：目标>200%
```

### 模型八：组织变革曲线（从"工具化"到"AI原生"）

```
组织AI成熟度五阶段：

L1 工具辅助 (2024前) → AI作为效率工具
L2 流程嵌入 (2024-2025) → AI嵌入核心业务流程  
L3 能力内化 (2025-2026) → 自建AI中台+模型微调
L4 生态共建 (2026-2027) → MCP生态+多Agent协作
L5 AI原生 (2028+) → AI原生产品+Agent自主决策

变革管理关键动作：
- 高管对齐：Board-level AI战略研讨会（季度）
- 中层赋能：AI literacy培训计划（覆盖100%中层）
- 一线激励："AI Champion"评选机制
- 组织保障：CAIO（首席AI官）或AI转型办
```

---

## 2026年金融AI关键趋势

| 趋势 | 内容摘要 | 战略影响 | 时间窗口 |
|------|---------|---------|---------|
| MCP标准化 | 已捐赠Linux AAIF治理，生态超1000服务器 | AI架构选型向MCP收敛 | 2026 Q2 |
| A2A协议 | Google推出Agent-to-Agent协作标准 | 多智能体编排成为可能 | 2026 Q3 |
| AI Agent规模化 | 金融行业从单点POC进入规模部署 | 从RPA升级到智能Agent | 2026-2027 |
| 模型监管趋严 | 央行要求AI模型台账+三方审计 | 治理成本上升 | 2026已实施 |
| 开源模型崛起 | DeepSeek-R1/千问3性价比优势明显 | 选型策略调整 | 2026持续 |
| 数据要素入表 | 企业数据资产入表扩展至金融机构 | 数据治理价值凸显 | 2026-2027 |

---

## When to Use

**可直接激活**（精确匹配AI战略规划场景）：
- "我要制定金融机构的3-5年AI转型战略"
- "AI场景那么多，先做哪个后做哪个？"
- "怎么建立AI治理体系，满足CBIRC/NFRA要求？"
- "AI能力是自己开发还是外面采购？"

**需用户确认**（可能与其他场景重叠）：
- "金融机构怎么做数字化转型"
- "AI在保险行业的应用"
- "怎么评估一个AI项目的ROI？"
- "AI Agent怎么在金融落地"

**不适用场景**：
- 具体代码实现（请使用开发类技能）
- 投资建议/个股推荐（请使用投资分析技能）
- 法律合规意见（应咨询法务团队）

---

## Python Code Templates

### ROI计算模板
> **示例代码（仅供学习参考，非本技能自动执行）**：
```python
def calculate_ai_roi(investment_cost, annual_savings, efficiency_gain, years=5):
    """
    AI项目ROI计算（参照麦肯锡三层次ROI方法）
    - investment_cost: 初始投资（万元）
    - annual_savings: 年化成本节约（万元）
    - efficiency_gain: 效率提升带来的收益（万元/年）
    """
    total_investment = investment_cost
    total_benefits = 0
    for year in range(1, years + 1):
        annual_benefit = annual_savings + (efficiency_gain * year * 0.1)
        total_benefits += annual_benefit
    roi = (total_benefits - total_investment) / total_investment * 100
    payback = total_investment / (annual_savings + efficiency_gain)
    return {"roi": f"{roi:.1f}%", "payback": f"{payback:.1f}年"}
```

### AI成熟度评估框架
> **示例代码（仅供学习参考，非本技能自动执行）**：
```python
def assess_ai_maturity():
    dimensions = ["数据基础", "技术能力", "组织文化", "治理体系", "应用场景"]
    levels = {
        1: "初始级 - 手工流程为主",
        2: "基础级 - 核心业务数字化",
        3: "发展级 - 多个AI场景落地",
        4: "成熟级 - AI驱动决策",
        5: "领先级 - AI原生架构"
    }
    return levels
```

---

## Compliance Checklist

### CBIRC合规要点
- 建立数据治理框架（数据分类分级、数据质量管控）
- 明确AI应用场景的权责边界（AI辅助≠AI决策）
- 建立模型风险管理制度（模型台账、三方审计）
- 定期进行AI系统审计（偏差监控±5%）
- 保障消费者权益和隐私（PIPL合规）

### PIPL合规检查
- 数据收集最小必要原则
- 用户知情同意
- 数据本地化存储
- 个人信息删除权保障

### 2026年新增合规要求
- AI伦理委员会设立（持牌机构必备）
- 算法公平性/透明度/可解释性纳入年度评级
- 重大模型变更须独立第三方审计
- 跨境数据流动合规（跨境金融沙盒试点）

---

## Source Notes

- 阿里百技图 · 金融行业Agent百技图（2026）
- 保险科技专委会《大模型AI Agent在保险行业的应用研究报告》（2025）
- 麦肯锡《Three Horizons of Growth》
- 银保监会《银行业保险业数字化转型指导意见》
- NFRA AI合规指引（2025-2026）
- 中国人民银行《金融科技发展规划》
- Gartner《AI in Financial Services》

---

## ClawHub Metadata

- **Slug**: finance-ai-strategy
- **Tags**: AI转型,数智化,金融科技,AI治理,战略规划,CBIRC合规,智能金融,Agent,AI Agent
- **Version**: 5.2.0
- **License**: MIT
- **Author**: gechengling
- **ClawHub URL**: https://clawhub.ai/gechengling/finance-ai-strategy

---

## README (English)

**Financial AI Strategy Architect** — McKinsey-informed AI transformation strategy for banks, insurers, and securities firms. Covers AI maturity diagnosis, Agent productivity formula, MCP/A2A ecosystem, LLM selection, multi-Agent orchestration, governance framework, and ROI assessment.

**Author**: gechengling | **License**: MIT
