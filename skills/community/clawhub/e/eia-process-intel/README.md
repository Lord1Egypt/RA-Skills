# eia-process-intel / 环评工艺情报

从环评报告提取企业真实产线的结构化事实，审查数字背后的监管博弈，推断工艺路线与设备选型，沉淀为可生长的三元组 ledger。适用于 WorkBuddy / Codebuddy / Claude Code / Codex。

Extract structured production-line facts from Chinese environmental impact assessment (EIA) reports, audit the numbers for regulatory gaming, infer process routes and equipment selection, and accumulate a growing triple-store ledger. Works with WorkBuddy / Codebuddy / Claude Code / Codex.

---

## 中文说明

### 这是什么

做硬科技一级市场尽调时，环评报告是少见的"公司自己写的、带法定责任、公示在建设之前"的文件：设备清单、物料平衡、产品方案都是强制披露项。本 skill 把"人工读环评"产品化为六段流水线：

1. **获取**（Phase 0）：公示平台三级检索指引 + 排污许可平台 + 存量文库
2. **提取**（Phase 1）：产品方案 / 逐工序工艺 / 设备清单 / 原辅材料 / 物料平衡 / 污染源 → 结构化事实表，每行带来源
3. **博弈审查**（Phase 2）：字段博弈分级——越影响审批/环保投入/监管的口径越会失真（产能/产品结构/排放量=高风险；设备数量/物理信息=低风险）；压线特征清单抓"批小建大、化整为零"
4. **交叉验证**（Phase 3）：用低风险信任锚（设备数量、物理信息）反算高风险字段；排污许可执行报告、危废转移联单等外部材料收窄区间
5. **推断**（Phase 4）：工艺路线三面证据定路线；工序→设备映射库推选型档次；物料平衡倒推良率区间（物料平衡法）；CAPEX 强度
6. **落账**（Phase 6）：带来源的三元组 JSONL ledger，一赛道一文件，随尽调生长；本体答不了的问题记失败查询，schema 只随真实需求演进

### 核心设计

- **环评数字不是事实**：数字入账前必过利益审查 + 物理交叉验证两道关
- **低风险字段是信任锚**：用便宜的真话检验贵的谎话
- **口径纪律**：披露与推断严格分离；反算输出永远是带口径的区间
- **映射库=本体词汇层**：工序→设备映射与三元组 ledger 共用一套设备类别词表
- **失败查询驱动生长**：加实体/关系必须有真实失败查询作依据

### 目录结构

```
eia-process-intel/
├── SKILL.md                  # Full playbook (English, runtime entry) — trigger table, grading table, 7 questions, Phase 0–6, recipes
├── references/
│   ├── field-credibility.md  # 字段博弈分级表 + 压线特征 + 利益审查三问（含分级更新记录）
│   ├── cross-validation.md   # 产能/良率/排放/产品结构反算配方 + 外部源清单
│   ├── ledger-schema.md      # 本体最小集：8 实体 8 关系 + JSONL 格式 + 生长机制
│   └── mappings/
│       └── semiconductor-equipment.md  # 半导体/红外/纳米压印种子映射
├── examples/
│   ├── format-demo-ir-detector.md     # 虚构 IR 探测器案例格式演示（中文）
│   └── format-demo-ir-detector-en.md  # 英文版
├── CHANGELOG.md
└── README.md
```

### 用法

对 AI 说"帮我分析这个环评"或直接丢环评 PDF；ledger 落在尽调项目工作区 `{项目目录}/eia-ledger/<赛道>.jsonl`。

---

## English

### What it is

In hard-tech private-market due diligence, the EIA filing is a rare document the company itself wrote under legal liability, disclosed before construction: the equipment list, material balance, and product scheme are all mandatory disclosures. This skill productizes "reading EIAs by hand" into a six-phase pipeline: acquire → structured extraction → adversarial gaming review → physics-based cross-validation → inference (route / equipment tier / yield / CAPEX) → append-only triple ledger with provenance.

### Core design

- **EIA numbers are not facts**: every number passes an interest review and physical cross-validation before entering the ledger
- **Low-risk fields are trust anchors**: cheap truths test expensive lies
- **Caliber discipline**: disclosed vs. inferred strictly separated; back-calculations are ranges with explicit calibers
- **Mapping library = ontology vocabulary**: the process→equipment mapping and the ledger share one equipment-class vocabulary
- **Failed-query-driven growth**: entities/relations are added only with real failed queries as justification

### Usage

Ask your agent to "analyze this EIA report" or drop the PDF. The ledger lives in your DD project workspace at `{project dir}/eia-ledger/<track>.jsonl`. The main playbook (`SKILL.md`) is written in English with Chinese domain terms inline.

---

## License

MIT
