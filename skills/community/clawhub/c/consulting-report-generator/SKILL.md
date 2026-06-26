---
name: consulting-report-generator
description: >
  通用型专业报告生成技能。支持任意内容输入（PPT/文字/PDF/图片），自动识别内容类型，
  自适应生成结构严谨的专业总结报告。覆盖精益生产、智能制造、计划物控（PC&MC）、
  数字化转型、AI与工业智能五大领域，同时支持项目管理、市场分析、技术总结等通用场景。
  基于mck-ppt-design专业布局框架（70+种麦肯锡风格布局模式），python-pptx原生绘制。
  【v6.1新增】支持 PPT/DOCX/PDF 三格式输出，默认PPT。DOCX基于python-docx，
  PDF基于reportlab（Markdown→PDF管道）。用户可通过"生成DOCX/PDF/Word"指令切换格式。
  【v6.1新增】支持根据PPT结构自动生成脑图PDF（思维导图），可视化报告大纲。
  用户可通过"生成脑图"指令触发。
  【v6新增】生成PPT前执行素材智能搜集（行业图片/图标/参考PPT/配色方案）
  并基于内容+偏好双因子推荐最佳模板风格，确认后再进入设计生成阶段。
  自动搜索行业基准数据、提取参考素材、OCR识别文档文字、智能扩增补充内容。
  内置自进化系统：每日自动发现新技能、追踪使用模式、记录错误与改进、持续优化模板。
  采用微软雅黑字体（Mac兼容），无BLOCK_ARC。触发词：生成PPT、做报告、项目总结、
  阶段性总结、咨询报告、生成总结报告、把这份资料做成PPT、根据这个内容生成报告。
  用户上传任何内容时，自动触发此技能进行专业报告生成。
compatibility: Requires Python 3.9+, pip, python-pptx, lxml.
---

# 通用报告生成器 v6.1（自进化·深度研究·素材增强·多格式输出·脑图PDF）

> **版本演进**：v3 Pro（布局重构）→ v4（通用双模式）→ **v5（自进化系统）→ v5.1（深度研究增强）→ v6（素材智能搜集+模板风格引擎）→ v6.1（PDF/DOCX多格式输出+脑图）**
>
> **核心升级**：
> - 🧬 **技能自进化系统** — 每日发现新技能、追踪使用模式、自动优化
> - 🔍 **技能发现引擎** — 扫描126+本地技能，智能推荐可集成的新能力
> - 📊 **使用分析引擎** — 追踪布局模式使用频率，优化模板选择
> - 🐛 **错误学习机制** — 记录每次错误与修复，避免重复问题
> - 🔄 **持续优化循环** — 自动更新技能生态矩阵，保持与时俱进
> - 🎯 **内容类型自识别** — 上传任意PPT/文字，自动判断内容类型
> - 🔬 **深度研究引擎** — 多源交叉验证、证据层次、三轮调研循环
> - 🖼️ **OCR/文档识别** — PDF、图片、Word、Excel文字提取
> - 🧠 **内容智能扩增** — 联网搜索补充，扩展报告深度
> - ✨ **去AI味润色** — 集成 humanizer-zh 去除AI痕迹
> - 🎨 **素材智能搜集引擎**（v6新增）— 自动搜图、搜图标、搜参考PPT、搜配色方案
> - 👔 **模板风格智能选择**（v6新增）— 内容驱动+用户偏好双因子风格推荐
> - 📄 **多格式输出**（v6.1新增）— PPT/DOCX/PDF 三格式支持，无明确指令时默认生成PPT
> - 🧠 **脑图PDF输出**（v6.1新增）— 根据PPT结构自动生成思维导图PDF，可视化报告大纲


---

## 一、定位

### 技能名称
`consulting-report-generator`（通用报告生成器）

### 核心能力
> **输入任意内容 → 自动识别 → 自适应模板 → 生成专业报告**

无论你上传的是制造咨询PPT、项目规划文档、市场调研报告、技术总结、还是任何行业的工作总结，本技能会自动分析内容类型，选择最合适的模板和布局，生成结构严谨的专业报告。

### 双模式工作

| 模式 | 触发条件 | 说明 |
|:----|:---------|:-----|
| **🎯 通用模式** | 任何非制造领域的内容 | 自适应模板，自动检测内容结构，生成通用总结报告 |
| **🔧 制造专家模式** | 检测到制造/精益/数字化关键词 | 调用ie-expert等专业分析技能，不限页数深度展开 |

### 内容类型自动检测

当用户上传资料时，自动执行内容分析：

```
输入内容分析
     │
     ├── 关键词检测: 精益/OEE/MES/TPM/SMED → 制造专家模式
     ├── 关键词检测: 项目/里程碑/成果/阶段 → 项目管理模式
     ├── 关键词检测: 市场/竞争/客户/份额 → 市场分析模式
     ├── 关键词检测: 技术/架构/系统/方案 → 技术总结模式
     └── 未匹配 → 通用模式（自适应模板）
```

### 用户角色
精益生产、智能制造、计划物控（PC&MC）、数字化转型、AI与工业智能资深咨询专家；
以及任何需要将内容转化为专业报告的职场人士。

### 覆盖领域

| 领域 | 说明 | 模式 |
|:----|:------|:----:|
| **精益生产** | VSM、5S、TPM、SMED、Kaizen、OEE、JIT | 制造专家 |
| **计划物控** | MPS、MRP、RCCP、排产调度、库存控制、齐套管理 | 制造专家 |
| **智能制造** | MES/WMS、数字化车间、数据采集、工业互联网 | 制造专家 |
| **数字化转型** | 数字化战略、IT架构、数据治理、系统集成 | 制造专家 |
| **AI与工业智能** | AI质检、预测维护、智能排产、数字孪生 | 制造专家 |
| **项目管理** | 项目总结、阶段汇报、结项报告 | 通用 |
| **市场分析** | 竞品分析、市场调研、行业报告 | 通用 |
| **技术总结** | 技术方案、架构设计、研发总结 | 通用 |
| **运营分析** | 经营分析、绩效报告、数据复盘 | 通用 |

### 报告类型（5种）— 不限页数，内容深度驱动

| 类型 | 默认深度 | 适用场景 | 说明 |
|:----|:--------:|:---------|:-----|
| **阶段总结** | 章节完整展开 | 项目中期/里程碑汇报 | 按项目模块逐项深入展开，每模块3-5页 |
| **项目总结** | 不限深度 | 终期交付/结项汇报 | 全链条覆盖，每项改善措施都展开分析和对比 |
| **分析报告** | 不限深度 | 调研/诊断/市场分析 | 每个诊断维度独立成节，数据+根因+改善建议 |
| **汇报提案** | 详实论证 | 方案汇报/投资审批 | 方案论证、数据支撑、对比分析完整呈现 |
| **专题分析** | 全深度展开 | 特定课题深度研究 | 完整的研究方法+数据分析+结论+建议 |

> **核心原则**：除非用户指定页数，否则**不设上限**。每个模块充分展开，数据表格完整呈现，对比分析逐项展开，确保信息密度和专业深度。生成建议页数为各项之和，但不受限于任何固定页数。

---

## 二、架构 — 九层设计

```
┌─ 自进化层 ──【v5新增】──────────────────────────────────────┐
│  技能发现引擎 + 使用分析 + 错误学习 + 模板优化              │
│  ▸ 每日扫描 ~/.workbuddy/skills/ 发现新技能                │
│  ▸ 追踪布局模式使用频率，自动推荐最佳模板                   │
│  ▸ 记录每次执行错误与修复，持续改进                         │
│  ▸ 自动更新技能生态矩阵，保持与系统同步                     │
│  ▸ 每次执行后写入进化日志，供后续参考                       │
├─ 识别层 ──────────────────────────────────────────────────┤
│  内容类型自动检测 + 自适应模板选择                          │
│  ▸ 关键词扫描 → 判断内容领域（制造/项目/市场/技术/通用）    │
│  ▸ 结构分析 → 识别章节/数据/图表/KPI                      │
│  ▸ 模板匹配 → 根据内容类型选择最佳模板                     │
│  ▸ 制造领域 → 启用专家技能生态                             │
├─ 设计层 ──────────────────────────────────────────────┤
│  mck-ppt-design 引擎（70种麦肯锡布局模式）              │
│  ▸ Cover / TOC / Section / Appendix                    │
│  ▸ Big Number / Data Table / Metric Cards / KP Tracker │
│  ▸ 2x2 Matrix / Three-Pillar / Pyramid / Process       │
│  ▸ Side-by-Side / Before-After / Scorecard              │
│  ▸ Exec Summary / Key Takeaway / Case Study            │
│  ▸ Timeline / Vertical Steps / Cycle / Funnel          │
│  ▸ Grouped Bar / Horizontal Bar / Trend / Dashboard    │
├─ 素材层 ──【v6新增】───────────────────────────────────┤
│  PPT素材智能搜集 + 模板风格选择引擎                     │
│  ▸ 行业图片搜索 → 按内容关键词收集高质量配图            │
│  ▸ 图标/装饰元素 → 创建装饰图标资源池                   │
│  ▸ 参考PPT分析 → 提取优秀设计元素（配色/字体/布局比例）   │
│  ▸ 风格双因子推荐 → 内容主题 × 受众期望 → 最优风格       │
│  ▸ 素材本地化 → 下载并保存到素材缓存目录                 │
│  ▸ 用户确认 → 展示素材预览，让用户调整风格选择            │
├─ 研究层 ──【v5.1新增】──────────────────────────────────┤
│  深度研究引擎 + 多源交叉验证 + 证据层次                    │
│  ▸ 关键数据点识别 → 自动判断是否需要深度研究              │
│  ▸ 三级调研（广度/深度/交叉验证）                         │
│  ▸ 四级证据体系（L1-L4）                                  │
│  ▸ 对接academic-deep-research等研究技能生态               │
├─ 内容层 ──────────────────────────────────────────────┤
│  联网搜索（免API） + 内容扩增引擎                       │
│  ▸ multi-search-engine（16引擎中英双语）                │
│  ▸ WebSearch（WorkBuddy内置搜索）                      │
│  ▸ WebFetch（搜索结果详情提取）                         │
│  ▸ 智能扩增：搜索补充资料 → 扩展报告深度                │
├─ 提取层 ──────────────────────────────────────────────┤
│  OCR识别 + 文档解析 + 图片文字提取                      │
│  ▸ markitdown（PDF/Word/Excel/图片OCR/HTML/URL）       │
│  ▸ Read工具（直接读取PDF/图片/文本）                    │
│  ▸ python-pptx提取（PPT图片/文字）                      │
│  ▸ 原PPT图片提取复用（extract_images_from_pptx()）     │
├─ 分析层 ──────────────────────────────────────────────┤
│  通用分析（所有模式）  │  制造专家（仅制造领域）          │
│  ▸ 数据趋势分析        │  ▸ ie-expert（工业工程）        │
│  ▸ 竞品对比分析        │  ▸ rohoon-6sigma（六西格玛）    │
│  ▸ SWOT/波特五力       │  ▸ inventory-*（库存分析）     │
│  ▸ 数据可视化          │  ▸ planning-mc（计划物控）      │
│  ▸ 图表生成            │  ▸ lean-toolkit（精益工具）     │
│  ▸ 统计建模            │  ▸ mfg-toolkit（制造咨询）     │
│                        │  ▸ CIO（数字化战略）            │
├─ 输出层 ──────────────────────────────────────────────┤
│  三格式输出引擎（v6.1新增）：                        │
│  ▸ PPT（默认）：python-pptx + mck-ppt-design 布局     │
│  ▸ DOCX：python-docx 原生生成，完整格式化+表格+图表   │
│  ▸ PDF：Markdown→reportlab 管道，CJK字符完美支持      │
│  ▸ 🧠 脑图PDF：从Slide Config自动生成结构脑图（v6.1） │
│  全格式统一规范：微软雅黑（Mac兼容）                  │
│  humanizer-zh 去AI味润色                              │
│  full_cleanup() 深度XML净化 + AUDIT() 自审函数        │
└────────────────────────────────────────────────────────┘
```

---

## 三、内容分析引擎（v4 通用 ⭐）

### 3.1 功能定位

**核心创新**：不再依赖固定的内容预设，而是智能分析用户提供的实际内容，自动决定报告的结构、模板和重点。

### 3.2 内容类型检测

接收到用户内容后，执行以下分析流程：

```python
# 内容类型自动检测
def detect_content_type(text):
    """根据提取的文字内容判断内容类型"""
    indicators = {
        "manufacturing":   ["精益", "OEE", "TPM", "SMED", "MES", "WIP", "Kaizen",
                           "5S", "VSM", "Takt", "换型", "在制", "节拍", "数字化车间"],
        "project":         ["项目背景", "里程碑", "交付物", "甘特图", "阶段",
                           "进度", "风险", "项目总结", "结项", "收益"],
        "market":          ["市场", "竞品", "客户", "份额", "SWOT", "波特",
                           "增长率", "市场规模", "竞争对手"],
        "technical":       ["架构", "系统", "方案设计", "技术路线", "模块",
                           "接口", "部署", "测试", "上线", "版本"],
        "business":        ["营收", "利润", "KPI", "增长率", "ROI", "成本",
                           "预算", "达成率", "同比", "环比", "运营"],
    }

    scores = {k: sum(1 for kw in v if kw in text) for k, v in indicators.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] >= 3 else "general"
```

检测结果决定：
- **制造领域**（manufacturing）→ 启用制造专家模式 + 内容驱动不限页模板
- **项目管理**（project）→ 项目管理模板（含甘特/里程碑/风险矩阵）
- **市场分析**（market）→ 市场分析模板（含竞品矩阵/SWOT/趋势图）
- **技术总结**（technical）→ 技术总结模板（含架构图/路线图/对比表）
- **运营分析**（business）→ 运营分析模板（含KPI仪表盘/趋势/行动项）
- **通用**（general）→ 通用模板（摘要/数据/对比/时间线/行动）

### 3.3 自适应模板引擎

基于内容类型，自动选择模块化结构（页数由内容量自动决定）：

```
制造领域: [封面→目录→背景→KPI→BA→支柱→流程→时间线→仪表盘→结束]
项目管理: [封面→目录→概述→里程碑→成果→风险→资源→时间线→行动→结束]
市场分析: [封面→目录→环境→竞品→SWOT→趋势→策略→对比→建议→结束]
技术总结: [封面→目录→背景→架构→方案→对比→路线→验证→展望→结束]
通用模板: [封面→目录→摘要→数据→分析→对比→时间线→行动→总结→结束]
```

### 3.4 内容驱动的内容层

对于**通用模式**，报告章节内容直接从用户提供的资料中提取和重组：

| 模板章节 | 内容来源 | 生成方式 |
|:---------|:---------|:---------|
| 封面标题 | 自动从内容中提取主题 | 提取最高频关键词或首句 |
| 摘要 | 用户资料中的概要/总结部分 | 浓缩提炼，去AI味 |
| 关键数据 | 提取的数字/指标/KPI | 做成#8 Big Number卡片 |
| 分析对比 | 内容中的对比/优劣势 | 做成#20 Before/After |
| 时间线 | 内容中的时间/阶段节点 | 做成#29 Timeline |
| 行动项 | 内容中的建议/下一步 | 做成#35 Action Items |
| 来源 | 用户资料本身 | 标注"数据来源：用户资料" |

---

## 四、资料提取子系统

### 4.1 功能定位

从用户提供的各类材料中智能提取文字内容，作为 PPT 生成的内容根基：

| 输入类型 | 提取方法 | 输出 |
|:---------|:---------|:-----|
| PDF 文件 | `markitdown` / `Read`（内置PDF阅读） | 纯文本/Markdown |
| Word (.docx) | `markitdown` / python-pptx 读取 | 结构化文本 |
| Excel (.xlsx) | `markitdown` / openpyxl 读取 | 表格数据 |
| 图片 (PNG/JPG) | `markitdown` (OCR) / `Read`（内置图片阅读） | 识别的文字 |
| HTML/URL | `markitdown` / `WebFetch` | 格式化文本 |
| PPTX (参考) | `extract_images_from_pptx()` + python-pptx 文本读取 | 图片+文字 |
| 纯文本 (.txt/.md) | `Read` 直接读取 | 原文 |

### 4.2 提取流程

```
用户提供资料
     │
     ▼
┌── 判断文件类型 ──────────────────────────────────────┐
│                                                        │
│  PDF/Word/Excel/Image  ──→ 方法A: markitdown CLI       │
│                            方法B: Read工具（内置支持）  │
│                                                        │
│  PPTX ──→ extract_images_from_pptx() + python-pptx读取 │
│                                                        │
│  HTML/URL ──→ WebFetch / markitdown                    │
│                                                        │
│  图片含表格 ──→ 手动提取表格结构 + 文字描述             │
│                                                        │
└────────────────────────────────────────────────────────┘
     │
     ▼
┌── 提取结果处理 ───────────────────────────────────────┐
│  ▸ 按文件来源分类整理                                   │
│  ▸ 识别关键数据点（数字、指标、日期、KPI）              │
│  ▸ 提取行业术语和技术要点                               │
│  ▸ 整理为结构化内容摘要                                 │
│  ▸ 输出 `extracted_content.md` 供后续使用               │
└────────────────────────────────────────────────────────┘
```

### 4.3 markitdown 使用规范

```bash
# 安装
pip install 'markitdown[all]'

# 基本用法
markitdown 输入文件路径 -o 输出文件.md

# 示例
markitdown report.pdf -o report.md          # PDF
markitdown data.xlsx -o data.md             # Excel
markitdown photo.png -o photo.md            # 图片OCR
markitdown https://example.com -o page.md   # 网页
markitdown doc.docx -o doc.md               # Word
```

### 4.4 资料提取规则（R6-R9）

| 规则 | 要求 |
|:----|:------|
| **R6** | 用户提供资料时，必须优先执行资料提取，不得跳过 |
| **R7** | 提取的文字必须按文件来源分类整理，不得混杂 |
| **R8** | 提取结果中识别关键数据点（数字/指标/年份）单独标注 |
| **R9** | 提取失败时告知用户，使用降级方法（Read工具→WebFetch）重新尝试 |

---

## 五、内容扩增子系统

### 5.1 功能定位

基于用户提供的资料内容，通过联网搜索 + 专业技能分析，智能扩展补充，提升报告的信息密度和专业深度。

### 5.2 三级扩增模型

```
L1: 直引 → 直接引用用户资料中的事实和数据
    └── 来源标记为 "数据来源：用户资料"

L2: 搜索补充 → 对每个关键数据点搜索行业基准/对标值
    └── 来源标记为 "来源：XXX（搜索日期）"

L3: 专业深化 → 调用技能生态进行专业分析
    └── 调用 ie-expert / rohoon-6sigma 等分析
```

### 5.3 扩增策略矩阵

| 用户资料内容 | 搜索补充方向 | 扩增目标 | 研究深度 |
|:-------------|:-------------|:---------|:--------:|
| 项目周期/范围 | 搜索同行业同类项目周期基准 | 对比分析，评估项目效率 | standard |
| 效率指标（OEE/良率/周期） | 搜索行业基准值、TEEPTRAK报告 | 行业对标，凸显差距 | standard |
| 库存周转数据 | 搜索同行业库存周转基准 | 定位行业水平 | standard |
| 改善措施清单 | 搜索最佳实践案例、成功对标 | 丰富方案论证 | quick |
| 投资/成本数据 | 搜索行业ROI基准、政策补贴 | 论证投资的必要性 | quick |
| 项目名称/关键词 | 搜索行业趋势、最新政策 | 提升报告时效性 | standard |
| 竞争对手提及 | 搜索竞争对手动态、行业排名 | 竞争格局分析 | **deep** |
| 市场规模/政策引用 | 搜索权威报告+政策原文 | 数据权威性验证 | **deep** |
| 技术趋势/前沿课题 | 搜索学术论文+行业白皮书 | 前瞻性分析 | **deep** |

### 5.4 扩增执行流程

```
提取的原始内容
     │
     ▼
┌── 关键数据点识别 ────→ 数字指标、KPI、日期、行业术语
     │
     ▼
┌── 搜索规划 ──────────→ 每个数据点对应2个搜索关键词
     │
     ├── [深度检测] 是否需要三轮调研？
     │   ├─ 数字指标 → standard/deep
     │   ├─ 竞品/政策 → deep
     │   └─ 纯描述 → quick（跳过研究）
     │
     ▼
┌── 联网执行 ──────────→ multi-search-engine / WebSearch
     │                      (根据深度级别执行1-3轮)
     ▼
┌── 交叉验证 ──────────→ 多来源对比（仅deep模式）
     │
     ▼
┌── 数据融合 ──────────→ 用户数据 + 搜索数据 = 综合结论
     │
     ▼
┌── 专业深化 ──────────→ 调用技能生态验证分析
     │
     ▼
┌── 内容撰写 ──────────→ 撰写扩增后的报告内容
     │
     ▼
┌── 去AI味润色 ────────→ humanizer-zh 去除AI痕迹
```

### 5.5 去AI味润色（集成 humanizer-zh）

生成的内容在写入 PPT 前，必须执行去AI味处理：

```python
# 检查点：每条文案输出前自检以下特征
CHECK_LIST = [
    "❌ 夸大的象征用语（"革命性""颠覆性""前所未有的"）",
    "❌ 宣传性/空洞表述（"赋能""抓手""闭环""打通"）",
    "❌ 模糊归因（"一般来说""某种程度""通常"）",
    "❌ 过度三段式（"第一...第二...第三..."）",
    "❌ AI常用词汇（"值得关注的是""值得注意的是"）",
    "❌ 过多连接短语（"此外""同时""另外""而且"）",
]
```

**规则**：每条 Action Title 和正文段落必须经过自检，去除上述特征后再写入 PPT。

---

## 六、设计要求

### 6.1 布局模式（基于 mck-ppt-design）

废弃全部自定义图表函数（VSM/GANTT/BAR/PIE等），全面使用 mck-ppt-design 的布局模式：

| 类别 | 布局模式 | 用途说明 |
|:----|:---------|:---------|
| **结构导航** | #1 Cover / #5 Section Divider / #6 TOC / #36 Closing | 封面/章节/目录/结束 |
| **数据统计** | #8 Big Number / #11 Data Table / #12 Metric Cards / #52 KPI Tracker | 关键数字/表格/指标/KPI追踪 |
| **框架矩阵** | #14 Three-Pillar / #16 Process Flow / #24 Exec Summary | 三支柱/流程箭头/执行摘要 |
| **对比评估** | #20 Before/After / #39 Horizontal Bar / #37 Grouped Bar | 改善前后对比/水平柱状图排名/分组柱状图 |
| **时间流程** | #24 Exec Summary / #29 Timeline / #35 Action Items | 执行摘要/时间线/行动项卡片 |
| **综合仪表盘** | #57 Dashboard | KPI行+柱状图+关键洞见 |
| **深蓝递进** | #60 HeaderBar | 深蓝顶栏标题+副标题 |
| **深蓝递进** | #61 PYRAMID | 居中多层金字塔布局 |
| **深蓝递进** | #62 BLOCK_3COL | 父块内三列子块 |
| **深蓝递进** | #63 TAG_CHIP | 层级标签chip |
| **深蓝递进** | #64 LEFT_LABEL_BAR | 左标签+右内容色条 |
| **战略分析** | #70 SWOT | SWOT四象限战略分析矩阵 |
| **数据可视化** | #71 PIE_BAR | 占比柱状图（避免BLOCK_ARC） |
| **卡片装饰** | #72 ICON / DECORATED_CARD | 图标装饰+带图标卡片 |
| **对比分析** | #73 MATRIX | 比较矩阵（多维度对比） |

### 6.2 配色规范 — Theme Contract 主题合约模式

采用标准化的 **5 色主题合约** 机制，所有布局函数统一遵守。每个主题定义 5 个颜色密钥：

```
Theme Contract = {primary, secondary, accent, light, bg}
```

**当前系统默认合约（咨询专业风）：**

| 密钥 | 变量名 | RGB | 用途 |
|:----|:------|:----:|:-----|
| **primary** | NV | (05, 1C, 2C) | 主色/标题/表格头/关键强调 |
| **secondary** | D3 | (33, 33, 33) | 正文内容/次级文字 |
| **accent** | AB | (00, 6B, A6) | 第一项强调/连接/引导 |
| **light** | BG | (F2, F2, F2) | 背景面板/卡片底/浅灰行 |
| **bg** | WH | (FF, FF, FF) | 白色背景 |

**扩展辅助色（所有合约通用）：**

| 颜色 | 简写 | RGB | 用途 |
|:----|:----|:----:|:-----|
| 强调绿 | AG | (00, 7A, 53) | 正向/改善后/完成 |
| 强调橙 | AO | (D4, 6A, 00) | 警示/连接箭头/风险 |
| 强调红 | AR | (C6, 28, 28) | 负向/改善前/未达标 |
| 浅蓝 | LB | (E3, F2, FD) | 蓝色卡片背景 |
| 浅绿 | LG2 | (E8, F5, E9) | 绿色卡片背景 |
| 浅橙 | LO | (FF, F3, E0) | 橙色卡片背景 |
| 浅红 | LR | (FF, EB, EE) | 红色卡片背景 |
| 中灰 | M6 | (66, 66, 66) | 次级文字/来源 |
| 浅灰 | LG | (CC, CC, CC) | 分隔线 |
| 深蓝L1 | LV1 | (05, 1C, 2C) | 递进色最深层 |
| 深蓝L2 | LV2 | (0A, 30, 4A) | 递进色第2层 |
| 深蓝L3 | LV3 | (10, 44, 62) | 递进色第3层 |
| 深蓝L4 | LV4 | (16, 58, 7A) | 递进色第4层 |
| 深蓝L5 | LV5 | (1C, 6C, 92) | 递进色第5层(最浅) |
| 子色1 | SV1 | (10, 60, 78) | 交付加速 |
| 子色2 | SV2 | (10, 68, 82) | 成本精控 |
| 子色3 | SV3 | (10, 70, 8C) | 质量跃升 |

### 6.6 多配色主题 — Theme Contract 引擎（v5新增·v6增强）

每个主题遵循标准的 **5 色合约**：`{primary, secondary, accent, light, bg}`。

| 主题名 | primary | secondary | accent | light | bg | 风格 | 推荐内容类型 |
|:------|:--------|:----------|:-------|:------|:---|:-----|:------------|
| **deepblue** | #051C2C 深蓝 | #333333 深灰 | #006BA6 蓝 | #F2F2F2 浅灰 | #FFFFFF 白 | 咨询专业风 | manufacturing, supply_chain, lean, project |
| **tech** | #005A96 亮蓝 | #333333 深灰 | #007A53 绿 | #F0F7FF 浅蓝 | #FFFFFF 白 | 科技现代风 | AI, digital, smart_mfg, IT_architecture |
| **business** | #2C3E50 商务灰 | #333333 深灰 | #006BA6 蓝 | #F5F5F5 浅灰 | #FFFFFF 白 | 沉稳专业风 | management, finance, operation, general |
| **vibrant** | #D46A00 活力橙 | #333333 深灰 | #C62828 红 | #FFF5EB 浅橙 | #FFFFFF 白 | 热情鲜明风 | innovation, kickoff, change, startup |

**Python 主题合约实现：**

```python
# Theme Contract 字典（供生成脚本引用）
THEME_CONTRACT = {
    "deepblue": {
        "primary": (0x05, 0x1C, 0x2C), "secondary": (0x33, 0x33, 0x33),
        "accent": (0x00, 0x6B, 0xA6), "light": (0xF2, 0xF2, 0xF2),
        "bg": (0xFF, 0xFF, 0xFF),
        "style_name": "咨询专业风", "section_deco": "深蓝左侧竖条",
    },
    "tech": {
        "primary": (0x00, 0x5A, 0x96), "secondary": (0x33, 0x33, 0x33),
        "accent": (0x00, 0x7A, 0x53), "light": (0xF0, 0xF7, 0xFF),
        "bg": (0xFF, 0xFF, 0xFF),
        "style_name": "科技现代风", "section_deco": "渐变色横条",
    },
    "business": {
        "primary": (0x2C, 0x3E, 0x50), "secondary": (0x33, 0x33, 0x33),
        "accent": (0x00, 0x6B, 0xA6), "light": (0xF5, 0xF5, 0xF5),
        "bg": (0xFF, 0xFF, 0xFF),
        "style_name": "沉稳专业风", "section_deco": "灰色细线分隔",
    },
    "vibrant": {
        "primary": (0xD4, 0x6A, 0x00), "secondary": (0x33, 0x33, 0x33),
        "accent": (0xC6, 0x28, 0x28), "light": (0xFF, 0xF5, 0xEB),
        "bg": (0xFF, 0xFF, 0xFF),
        "style_name": "热情鲜明风", "section_deco": "橙色全宽色块",
    },
}

def apply_theme(theme_name):
    """一键应用主题合约——设置全局色值"""
    t = THEME_CONTRACT[theme_name]
    NV = RGBColor(*t["primary"]); D3 = RGBColor(*t["secondary"])
    AB = RGBColor(*t["accent"]);  BG = RGBColor(*t["light"])
    WH = RGBColor(*t["bg"])
    return t["style_name"]
```

**风格自动选择逻辑（双因子推荐）：**

```python
def auto_select_theme(content_type, user_preference=""):
    """
    根据内容类型和用户偏好自动选择最佳主题
    内容类型权重60%，用户偏好权重40%
    """
    type_theme_map = {
        "manufacturing": "deepblue",
        "project": "deepblue",
        "digital": "tech",
        "AI": "tech",
        "finance": "business",
        "management": "business",
        "innovation": "vibrant",
        "startup": "vibrant",
    }
    
    user_vibe_map = {
        "高端": "deepblue", "权威": "deepblue", "严肃": "deepblue",
        "科技": "tech", "前沿": "tech", "未来": "tech",
        "沉稳": "business", "稳重": "business", "保守": "business",
        "活力": "vibrant", "创新": "vibrant", "热情": "vibrant",
    }
    
    # 内容类型匹配
    recommended = type_theme_map.get(content_type, "business")
    
    # 校正：如果用户表达了偏好
    for word, theme in user_vibe_map.items():
        if word in user_preference:
            return theme  # 用户偏好优先级更高
    
    return recommended
```

使用方式：生成脚本开头调用 `theme = auto_select_theme(content_type, user_preference)`，然后 `apply_theme(theme)` 一键切换全局色系。

### 6.3 字体规范

**全微软雅黑 + Arial英文：**

| 层级 | 用途 | 字号 | 样式 |
|:----|:----|:----:|:----:|
| H0 | 封面标题 | 40pt | Bold, Microsoft YaHei |
| H1 | Section标题 | 28pt | Bold, Microsoft YaHei |
| H2 | Action Title（每页标题） | 22pt | Bold, Microsoft YaHei |
| H3 | 卡片/子标题 | 14-16pt | Bold, Microsoft YaHei |
| H4 | 正文/列表 | 12-14pt | Regular, Microsoft YaHei |
| H5 | 注释/来源 | 9pt | Regular, Microsoft YaHei |

**规则：**
- 中文统一用 `Microsoft YaHei`（微软雅黑）
- 英文/数字统一用 `Arial`
- 通过 `a:ea` 节点设置东亚字体：`ea.set('typeface', 'Microsoft YaHei')`
- 设置拉丁字体：`latin.set('typeface', 'Arial')`

### 6.4 Mac兼容规则（R1-R5）

| 规则 | 要求 | 违反后果 |
|:----|:-----|:---------|
| **R1** | 字体：中文=微软雅黑 + 英文=Arial（不用Georgia） | Mac缺失Georgia显示方块 |
| **R2** | ❌ 禁止 `MSO_SHAPE.BLOCK_ARC`（Mac PowerPoint不渲染） | 饼图/环形图用表格或柱状图替代 |
| **R3** | ❌ 禁止 `MSO_SHAPE.DIAMOND`（菱形） | 改用圆角矩形+文字标注 |
| **R4** | 文本框 `top+height` 不重叠，间距显式计算 | 多行文本动态计算高度 |
| **R5** | 生成后必须执行 `full_cleanup()` | Mac打开时报错 |

### 6.5 资料提取兼容规则（R6-R9）

R6-R9 规则的完整定义请参考 **第四章第4.4节「资料提取规则（R6-R9）」**，此处不再重复。

**快速索引：**
- R6 → 资料必须优先提取
- R7 → 提取内容按来源分类
- R8 → 关键数据点单独标注
- R9 → 提取失败降级重试

---

## 七、内容标准 — 深度优先自适应引擎（v6 升级 ⭐）

> **核心原则**：不再设定固定页数上限。报告结构由内容量自动决定，每个模块充分展开到细节。除非用户明确指定页数，否则页数不受限制，以信息完整和专业深度为唯一衡量标准。

### 模块化内容装配器

报告由以下模块组成，根据内容量自动装配。每个模块的页数由内容深度决定，不设上限：

| 模块 | 用途 | 最小内容 | 典型展开 | 不设上限说明 |
|:----|:-----|:--------|:--------|:------------|
| **封面** | 项目标识 | 1页 | 1页 | 保持不变 |
| **目录** | 导航 | 1页 | 1-2页 | 随章节数自动扩展 |
| **章节分隔** | 视觉过渡 | 每章节1页 | 每章节1页 | 按实际章节数生成 |
| **背景/概述** | 项目背景与目标 | 1页 | 2-4页 | 背景+痛点+目标可各占1页 |
| **KPI/大数字** | 关键指标速览 | 1页 | 2-4页 | 每个维度可独立成页 |
| **诊断/分析** | 问题发现与根因 | 2页 | 4-10页 | 每个诊断维度1-2页完整展开 |
| **改善方案** | 解决方案详述 | 2页 | 6-12页 | 每个改善模块2-3页（方案+措施+预期） |
| **对比分析** | 前后对比/对标 | 1页 | 2-6页 | 每个对比点可独立成页 |
| **数据表格** | 详细数据支撑 | 1页 | 2-8页 | 每个数据集独立表格 |
| **时间线** | 实施路径 | 1页 | 2-4页 | 详细到每月的里程碑 |
| **仪表盘** | 综合洞见 | 1页 | 2-4页 | 多维度多图表 |
| **行动项** | 下一步计划 | 1页 | 2-4页 | 每个行动项带详细描述 |
| **结束页** | 总结致谢 | 1页 | 1-2页 | 保持不变 |

> 每个模块的「典型展开」为参考建议，实际页数由内容量自行决定，**不受任何上限约束**。

### 内容深度分级

生成的每一页报告内容按以下三级深度展开：

| 深度级别 | 说明 | 示例 |
|:--------|:-----|:------|
| **L1: 结论先行** | 一页给出核心结论 + 关键支撑数据 | 适合高层面向决策者的总览页 |
| **L2: 分析展开** | 问题描述 + 根因分析 + 数据证据 + 影响评估 | 适合核心分析页 |
| **L3: 细节完整** | 全部数据表格 + 分项对比 + 详细注释 + 来源标注 | 适合数据支撑页 |

**展开规则**：页面内容自动判断是否需要更多页来充分表达。如果一页排不下，自动拆分到下一页继续展开，不受任何页数限制。

### 自动页数生成算法

```
内容总量(Total Content Units)
     │
     ▼
┌── 评估内容密度 ─────────────────────────────────────┐
│                                                      │
│  每个模块的 TCU = Σ(段落数 × 1.0 + 数据点 × 0.5     │
│                       + 图表数 × 1.5 + 列表项 × 0.3) │
│                                                      │
│  每个Action Title(一页)容量 ≈ 4-6 TCU                │
│                                                      │
│  该模块页数 = ceil(模块TCU / 每页TCU容量)            │
│                                                      │
│  总页数 = Σ(各模块页数) + 导航页(封面+目录+章节分隔) │
│                                                      │
└──────────────────────────────────────────────────────┘
     │
     ▼
如用户指定页数（如"20页"）：
     → 按比例压缩每个模块的TCU分配
     → 优先保留L1深度，压缩L3细节
     → 保证完整性和连贯性

如未指定页数（默认）：
     → 所有模块按L2-L3深度完整展开
     → 页数不受限制，以内容完整为准
     → 总页数 = 自然生成的页数
```

### 建议页数参考（非约束）

以下为参考范围，实际生成**不受此范围限制**：

| 报告类型 | 最小建议 | 完整深度建议 | 说明 |
|:--------|:--------:|:-----------:|:-----|
| 阶段总结 | 8页 | 20-35页 | 按模块展开，每个模块3-5页 |
| 项目总结 | 12页 | 35-60+页 | 全链条展开，不限页数 |
| 分析报告 | 10页 | 25-40+页 | 每个诊断维度独立成节 |
| 汇报提案 | 8页 | 20-35页 | 方案论证+数据支撑完整 |
| 专题分析 | 6页 | 15-30+页 | 研究方法+数据+结论完整展开 |

### Action Title 要求

每页标题必须是**完整句子**（陈述结论），而非标题式短语：

```
❌ "组织优化"
✅ "深入调研发现问题 — 组织架构不匹配、职责交叉"

❌ "项目背景"
✅ "民和电器携手连恩，启动精益+数字化双轮驱动战略转型"

❌ "库存分析"
✅ "库存管理行业对标 — 中国制造业与国际差距1.4-2.3倍"
```

### 来源标注规范

- 每个数据/图表下方必须标注来源
- **三级来源标注体系**：

| 来源级别 | 内容来源 | 标注格式 | 示例 |
|:---------|:---------|:---------|:-----|
| L1：用户资料 | 直接引用用户提供的资料 | `"数据来源：用户资料"` | 用户资料 |
| L2：搜索补充 | 联网搜索到的行业数据 | `"来源：XXX·年份"` | 简道云·2026 |
| L3：技能分析 | 调用专业技能分析结论 | `"来源：ie-expert分析"` | ie-expert分析 |

- 位置：页面底部 7.05 英寸位置（9pt, M6色）

---

## 八、助手函数规范

所有生成的 PPT 脚本必须包含以下助手函数（参考 `generate_pro.py` 实现）：

| 函数 | 用途 |
|:----|:------|
| `cs(s)` | 清理 shape 的 p:style XML，防文件损坏 |
| `sf(run, is_en)` | 设置字体：中文 YaHei，英文 Arial，通过 a:ea 节点 |
| `TX(s, l, t, w, h, tx, ...)` | 统一文本框，支持 Microsoft YaHei |
| `R(s, l, t, w, h, c)` | 矩形（无边框） |
| `RR(s, l, t, w, h, c)` | 圆角矩形 |
| `HL(s, x, y, ln, c, t)` | 水平线（薄矩形替代connector） |
| `OV(s, x, y, lb, sz, bg, fg)` | 圆形标签 |
| `AT(s, tx, sz)` | Action Title（白色背景+下划线，22pt Bold） |
| `SR(s, tx, y)` | 来源标注（9pt M6色，7.05寸位置） |
| `PN(s, n)` | 页码（仅显示当前页号） |
| `full_cleanup(path)` | 深度XML净化（正则移除p:style+空ln+themeShadow，补齐typeface） |
| `AUDIT(prs)` | 自审函数（图形量≥200，密度≥8，无BLOCK_ARC，去AI味通过） |
| `HDR(s, title, subtitle)` | 深蓝顶栏标题（新增v4） |
| `PYRAMID(s, layers, header)` | 居中多层金字塔（新增v4） |
| `BLOCK_3COL(s, cx, cy, cw, ch, items)` | 三列子块布局（新增v4） |
| `TAG_CHIP(s, text, x, y)` | 层级标签芯片（新增v4） |
| `LEFT_LABEL_BAR(s, x, y, w, h, label, lw, content, lb, cb)` | 左标签右内容条（新增v4） |
| `apply_theme(name)` | 配色主题切换（v5新增：deepblue/tech/business/vibrant） |
| `auto_select_theme(ct, pref)` | **模板风格选择（v6新增）** 根据内容类型+用户偏好推荐主题 |
| `SWOT(s, s,w,o,t, y)` | SWOT四象限分析矩阵（v5新增） |
| `PIE_BAR(s, items, y, title)` | 占比柱状图替代饼图（v5新增） |
| `ICON(s, x, y, char, sz, bg, fg)` | 装饰图标（v5新增） |
| `DECORATED_CARD(s, x, y, w, h, icon, title, desc, clr)` | 带图标装饰卡片（v5新增） |
| `MATRIX(s, headers, rows, y)` | 比较矩阵（v5新增） |
| `collect_ppt_materials(type, kws)` | **素材搜集（v6新增）** 搜集行业图片/图标/参考PPT等 |
| `generate_search_terms(type, kws)` | **搜索词生成（v6新增）** 根据内容类型生成素材搜索关键词 |
| `save_material_inventory(collected)` | **素材清单保存（v6新增）** 输出素材清单到 material_inventory.md |

---

## 九、布局模式实现规范

### 布局：#1 Cover — 封面
```python
def cover(s, title, subtitle="", date="", company=""):
    # 顶部细线：NV色
    # 标题：40pt Bold, NV色，多行动态计算高度
    # 副标题：24pt, D3色
    # 日期+公司：14pt, M6色
    # 底部装饰线：NV色 2pt
```
- 封面标题高度根据行数动态计算：`th = 0.8 + 0.65 * (lines-1)` 英寸

### 布局：#6 TOC — 目录
```python
def toc(s, items):
    # items = [(编号, 标题, 描述), ...]
    # 每行：圆形编号(NV) + 章节名(16pt,Bold) + 描述(14pt,M6)
    # 底部：灰色分隔线
```
- 全部8个章节必须完整列出

### 布局：#5 Section — 章节分隔页
```python
def SEC(s, n, title, subtitle=""):
    # 左侧NV色竖条
    # "PART N" 16pt M6色
    # 标题 28pt Bold NV色
    # 副标题 14pt D3色
```

### 布局：#8 Big Number — 大数字
```python
def BN(s, items, y=TZ):
    # items = [(大数字, 标签, 颜色), ...]
    # 第一项：NV底色+白字 或 BG底+NV字
    # 大数字44pt Bold，标签14pt
```

### 布局：#11 Data Table — 数据表
```python
def TB(s, l, t, rows, cols, data, col_ws=None):
    # 使用 add_table() 原生表格（不自绘）
    # 表头：NV深蓝底 + 白字 Bold 9pt
    # 数据行：浅灰交替行（#F5F7FA）
    # 字体：9pt Microsoft YaHei
    # 居中对齐
```

### 布局：#12 Metric Cards — 指标卡片
```python
def MCARDS(s, items, y=TZ):
    # items = [(数值, 标签, 示例值, 颜色), ...]
    # 白底卡片 + 顶部色彩条
    # 数值24pt Bold 色彩色，标签11pt M6，详情10pt D3
```

### 布局：#14 Three-Pillar — 三支柱
```python
def PILLAR(s, items, y=TZ):
    # items = [(标题, [要点列表...], 颜色), ...]
    # 顶部色条 + 标题14pt WH色
    # 下方BG色卡片 + 要点列表12pt D3色
```

### 布局：#16 Process Flow — 流程箭头
```python
def FLOW(s, steps, y=Inches(2.5)):
    # steps = [(标题, 描述), ...]
    # 第一项NV色，后续BG色
    # 箭头用文本"→" AO色
```

### 布局：#24 Exec Summary — 执行摘要
```python
def EXEC(s, title, points):
    # title: 摘要标题
    # points: [(编号, 标题, 描述), ...]
    # 首项：NV底白字 关键结论
    # 后续：编号OV + 标题(14pt NV Bold) + 描述(14pt D3)
```
- 用于 P4 项目背景、P8 方案概览等需要结论先行的页面
- 顶部深蓝结论条 + 下方3-4个支撑论点

### 布局：#20 Before/After — 对比
```python
def BA(s, before, after, y=TZ):
    # 左栏 BG色 "现状(Before)" D3色文字
    # 右栏 NV色 "目标(After)" WH色文字
    # 中间 "→" 箭头 NV色
```

### 布局：#29 Timeline — 时间线
```python
def TIMELINE(s, items, y=Inches(3.0)):
    # items = [(标题, 描述), ...]
    # 水平LG色连接线 2pt
    # 圆形编号节点 NV色
    # 上方标题 16pt Bold NV色
    # 下方描述 11pt D3色
```

### 布局：#35 Action Items — 行动项
```python
def ACTIONS(s, items, y=TZ):
    # items = [(行动, 时间, 负责人), ...]
    # 多列BG色卡片
    # 编号 + 标题(14pt NV色) + 时间(11pt M6) + 负责人(11pt D3)
```

### 布局：#36 Closing — 结束页
```python
def CLOSE(s, main_text, sub_text="", tagline=""):
    # 顶部NV色细线
    # 主标题 28pt NV色 Bold 居中
    # 装饰线 NV色 1.5pt
    # 副标题 18pt D3色
    # 底部NV色粗线 2pt
    # 标语：20pt AO色 Bold
```

### 布局：#39 Horizontal Bar — 水平柱状图
```python
def HBAR(s, items, y=TZ, title=""):
    # items = [(标签, 值), ...] 已排序
    # 第一名NV色，后续BG色
    # 背景浅灰条 + NV色填充条
```

### 布局：#37 Grouped Bar — 分组柱状图
```python
def GBAR(s, data, labels, colors, y=TZ, title=""):
    # data = [[系列1的值], [系列2的值], ...] 每行=一个系列
    # labels = [组标签, ...] 如 ["M1","M2","M3"]
    # colors = [颜色1, 颜色2, ...] 每个系列的颜色
```
- 通常嵌入 #57 Dashboard 中使用
- 含Y轴刻度（0%-100%）、数值标签、图例
- 用于月度趋势对比、多系列数据展示

### 布局：#52 KPI Tracker — KPI追踪
```python
def KTRACK(s, items, y=TZ):
    # items = [(名称, 进度0-1, 详情, 状态on/risk/off), ...]
    # 表头(11pt M6 Bold) + 黑色分割线
    # 进度条 on=AG / risk=AO / off=AR
    # 达成率 14pt Bold 状态色
```

### 布局：#57 Dashboard — 仪表盘
```python
def DASH(s, kpis, data, labels, colors, insights):
    # kpis = [(数值, 标签, 颜色), ...] 顶行KPI卡片
    # data/labels/colors → 分组柱状图
    # insights → BG色底+NV色字 关键洞见
```

---

## 十、完整工作流（S0-S15）

### S0: 内容分析与自进化检查（双轨并行 ⭐）
**内容分析轨道** — 在提取资料前，先对内容进行类型分析：

1. 提取内容样本（前1000字符或文件标题）
2. 运行 `detect_content_type()` 检测内容类型
3. 根据检测结果选择模式：制造专家 / 项目管理 / 市场分析 / 技术总结 / 通用
4. 根据模式选择对应的内容驱动模板（页数不限）
5. 通知用户检测结果，确认或手动调整

**自进化轨道** — 与内容分析同时执行：

1. 加载进化数据（`self_evolution/` 目录下的 known_skills / usage_log）
2. 调用 `self_evolution.py scan` 扫描新技能
3. 检查上次错误是否已修复
4. 加载高频使用的布局模式偏好
5. 如有新发现技能，通知用户集成建议

```
检测结果示例：
  "检测到内容类型：项目管理（置信度85%）
  将使用项目管理模板，包含：里程碑/风险矩阵/资源分配等章节
  如需切换模板请告知"

💡 系统提示：
  "自进化检查完成 | 已发现 0 个新技能 | 上次错误已修复 ✅"
```

### S1: 资料收集与识别
确认用户提供了哪些资料：
- `[ ]` PDF 文件 → 计划使用 markitdown / Read 提取文字
- `[ ]` Word 文档 → 计划使用 markitdown 提取文字
- `[ ]` Excel 表格 → 计划使用 markitdown 提取数据
- `[ ]` 图片/截图 → 计划使用 markitdown OCR / Read 识别
- `[ ]` 参考 PPTX → 计划使用 extract_images_from_pptx() 提取
- `[ ]` 参考 URL → 计划使用 WebFetch 获取内容
- `[ ]` 纯文本/笔记 → 计划使用 Read 读取
- `[ ]` 未提供任何资料 → 跳过S1，从S2开始

### S2: 资料提取
执行资料提取流程：
1. 对每个文件执行对应的提取方法
2. 按来源分类整理提取结果
3. 标注关键数据点（数字、指标、年份、KPI）
4. 输出 `extracted_content.md` 内容摘要文件
5. 如提取失败，尝试降级方法（Read → WebFetch）

### S3: 内容扩增
基于提取的资料内容执行联网扩增：
1. 识别关键数据点 → 每个点搜索2个关键词
2. 融合用户资料 + 搜索数据 → 形成综合结论
3. 调用专业技能验证分析（仅制造领域）
4. 输出扩增后的内容大纲
5. 执行去AI味自检（参考5.5节检查清单）

### S4: 需求确认
与用户确认：内容类型检测结果、资料提取结果、内容扩增大纲、报告类型。
重点确认扩增的数据是否准确、模板选择是否合适。

**输出格式选择（v6.1 新增）：**
```
请选择输出格式：
  ○ 📊 PPT（默认）— 适用于会议汇报/客户演示
  ○ 📝 DOCX — 适用于报告存档/详细文字论述
  ○ 📄 PDF — 适用于正式交付/打印输出
提示：默认为PPT，无需特别声明。如需DOCX/PDF请明确说明。
```

### S5: 联网调研（免API）
使用 `multi-search-engine` + `WebSearch` + `WebFetch` 搜索行业基准数据。
- 每个搜索点至少搜索2个关键词交叉验证
- 所有来源必须标注"来源：XXX（搜索日期）"

### S6: 原PPT图片提取（如有）
调用 `extract_images_from_pptx()` 提取参考PPT图片，按页归类。
提取的图片嵌入新PPT的对应页面。

---

### S6.5: PPT素材搜集与模板风格选择 【v6 新增 ⭐】

> **核心变更**：在生成PPT前，先执行素材搜集操作，然后基于内容+用户偏好双因子驱动选择最佳模板风格，之后再进入设计和生成阶段。

#### 第一步：PPT素材智能搜集

基于已确认的报告大纲和内容主题，执行素材搜集操作：

```python
# 素材搜集操作规范
MATERIAL_TYPES = {
    "industry_image": {
        "description": "行业相关高清图片",
        "search_terms": ["行业关键词 + 制造现场/数字化/精益", "industry + factory/digital/lean"],
        "source": "WebSearch / WebFetch 图片搜索",
        "usage": "封面背景、章节分隔页、案例展示页",
    },
    "icon_element": {
        "description": "装饰图标（简单线条图标）",
        "search_terms": ["SVG icon + sector_name", "图标 + 行业"],
        "source": "WebSearch 图标资源",
        "usage": "指标卡片、流程步骤、列表装饰",
    },
    "reference_slide": {
        "description": "同类行业PPT参考设计",
        "search_terms": ["行业 + PPT模板/报告设计", "consulting deck + industry"],
        "source": "WebSearch + WebFetch 提取设计元素",
        "usage": "参考配色方案、布局比例、信息图表风格",
    },
    "color_palette": {
        "description": "行业相关配色方案",
        "search_terms": ["行业 + 品牌色/VI色彩", "color palette + industry"],
        "source": "WebSearch 品牌/VI资料",
        "usage": "辅助确定报告主色和强调色",
    },
    "data_chart": {
        "description": "行业数据可视化参考",
        "search_terms": ["行业 + 数据可视化/图表", "industry chart/data viz"],
        "source": "WebSearch 公开报告图表",
        "usage": "参考图表类型选择和视觉呈现方式",
    },
}

def collect_ppt_materials(content_type, keywords):
    """基于内容类型和关键词搜集PPT素材"""
    collected = {}
    
    # 1. 根据内容类型确定搜索关键词
    search_terms = generate_search_terms(content_type, keywords)
    
    # 2. 对每种素材类型执行搜索
    for mat_type in MATERIAL_TYPES:
        results = web_search(f"{search_terms} {mat_type.search_terms[0]}")
        if results:
            # 提取前3个最有价值的素材链接
            top_results = filter_best_results(results, mat_type)
            collected[mat_type] = top_results
    
    # 3. 对参考素材进行详情提取
    for mat_type, results in collected.items():
        for result in results[:2]:  # 提取前2个
            detail = web_fetch(result.url)
            enrich_material(mat_type, result, detail)
    
    # 4. 输出素材清单供用户确认
    save_material_inventory(collected)
    return collected
```

**素材搜集规则（R15-R18）：**

| 规则 | 要求 |
|:----|:------|
| **R15** | 必须基于已确认的内容大纲生成搜索关键词，拒绝通用关键词 |
| **R16** | 每种素材类型至少搜集2-3个高质量来源，优先行业官网/权威报告 |
| **R17** | 搜集到的素材需标注来源URL和用途说明，供后续生成脚本引用 |
| **R18** | 若用户未提供参考PPT，素材搜集不可跳过——至少要搜集配色方案+行业图片 |

#### 第二步：模板风格智能选择

基于内容分析结果和素材搜集情况，使用**双因子推荐算法**选择最佳模板风格：

```python
THEMES = {
    "deepblue": {
        "name": "咨询专业风",
        "palette": "NV(#051C2C)深蓝 + WH白 + AB(#006BA6)蓝",
        "best_for": ["manufacturing", "supply_chain", "lean", "project"],
        "vibe": "高端、权威、严肃",
        "deco_style": "简约线条、几何装饰、数据驱动",
        "font_emphasis": "Bold标题+清晰层级",
        "section_deco": "深蓝左侧竖条",
    },
    "tech": {
        "name": "科技现代风",
        "palette": "AB(#005A96)亮蓝 + WH白 + AG(#007A53)绿",
        "best_for": ["AI", "digital", "smart_mfg", "IT_architecture"],
        "vibe": "前沿、创新、高效",
        "deco_style": "渐变色块、轻薄阴影、科技图标",
        "font_emphasis": "Light标题+清晰层级",
        "section_deco": "渐变色横条",
    },
    "business": {
        "name": "沉稳专业风",
        "palette": "D3(#333333)商务灰 + NV深蓝点缀 + AB蓝",
        "best_for": ["management", "finance", "operation", "general"],
        "vibe": "稳重、理性、信任",
        "deco_style": "灰底卡片、精细边框、保守排版",
        "font_emphasis": "规则的标题+正文",
        "section_deco": "灰色细线分隔",
    },
    "vibrant": {
        "name": "热情鲜明风",
        "palette": "AO(#D46A00)活力橙 + WH白 + AR(#C62828)红",
        "best_for": ["innovation", "kickoff", "change", "startup"],
        "vibe": "活力、推动、紧迫",
        "deco_style": "大色彩块、粗轮廓、大数字强调",
        "font_emphasis": "大号标题+高对比",
        "section_deco": "橙色全宽色块",
    },
}

def select_theme(content_type, user_mood, material_results):
    """双因子模板风格推荐算法"""
    content_score = {}  # 内容因子：基于内容类型
    for theme_name, theme in THEMES.items():
        # 内容类型匹配度
        best_for = theme["best_for"]
        match_count = sum(1 for t in best_for if t in content_type or content_type in t)
        content_score[theme_name] = match_count
    
    # 如果用户表达了偏好，增强偏好分
    if user_mood:
        mood_map = {
            "高端": "deepblue", "权威": "deepblue", "严肃": "deepblue",
            "科技": "tech", "创新": "tech", "前沿": "tech",
            "稳重": "business", "保守": "business", "专业": "business",
            "活力": "vibrant", "创新2": "vibrant", "推动": "vibrant",
        }
        for word, theme in mood_map.items():
            if word in user_mood:
                content_score[theme] += 2  # 用户偏好权重
    
    # 选择分值最高的主题
    best_theme = max(content_score, key=content_score.get)
    return best_theme
```

**算法逻辑：**
1. **内容因子**（权重60%）：由内容类型检测结果决定
   - 制造/精益/供应链 → deepblue
   - AI/数字化/智能制造 → tech
   - 管理/财务/运营 → business
   - 创新/变革/启动会 → vibrant
2. **用户偏好因子**（权重40%）：来自用户表述/历史记录
   - 用户明确说"高端/权威" → deepblue
   - 用户说"科技感/前沿" → tech
   - 用户说"稳重/保守" → business
   - 用户说"活力/创新" → vibrant
3. **校正因子**：素材搜集结果反馈
   - 如果搜集到的素材中有明确的品牌色/VI倾向，反向校准推荐

#### 第三步：风格确认与素材预览

将推荐的模板风格 + 搜集到的素材列表呈现给用户确认：

```
┌─ 模板风格推荐 ──────────────────────────────────────────┐
│                                                          │
│  推荐风格：🔵 咨询专业风 (deepblue)                      │
│  ○ 深蓝主色 #051C2C × 白色背景 × 蓝色强调               │
│  匹配理由：内容类型"精益制造" × 用户偏好"高端"          │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │  素材搜集清单：                                      ││
│  │  ✅ 行业图片：3张（制造现场图×2, 数字化看板×1）     ││
│  │  ✅ 装饰图标：5个（生产/质量/物流/计划/设备）        ││
│  │  ✅ 参考PPT：2个（同行业咨询报告设计）               ││
│  │  ✅ 配色方案：已从参考PPT提取2组备选                 ││
│  │  └─ 来源详见 material_inventory.md                   ││
│  └──────────────────────────────────────────────────────┘│
│                                                          │
│  可选风格：                                              │
│  ○ ⚪ 咨询专业风（推荐） ○ 🔵 科技现代风                │
│  ○ ⚫ 沉稳专业风      ○ 🟠 热情鲜明风                  │
│                                                          │
│  请确认风格，或选择其他风格：                            │
└──────────────────────────────────────────────────────────┘
```

- 如果用户调整风格，更新 `theme = apply_theme(selected_theme)`
- 将素材引用信息写入生成脚本注释
- 将素材图片/图标路径嵌入生成脚本中

---

### S7: 设计大纲 + Slide Config 模块化架构
按照选定的内容类型和模板模块，逐页确定内容和布局模式。**页数由内容量自动决定，不设上限**。
- 每个模块按内容深度分级（L1-L3）展开
- 数据丰富时自动拆分到多页，不急于一页塞完
- 如果用户指定了页数，按比例压缩模块深度；否则完全展开

**Slide Config 模块化架构**（借鉴 PPT 演示文稿技能）：

每页幻灯片定义为独立的 `slide_config` 数据块，统一元数据结构：

```python
# 每页的标准化 Slide Config
slide_config = {
    "type": "cover|toc|section|content|summary|closing",
    "index": 1,         # 页码
    "layout": "#1 Cover",  # mck-ppt-design 布局模式编号
    "title": "页面Action Title（完整句子）",
    "depth": "L1|L2|L3",   # 内容深度级别
    "theme": "deepblue",   # 主题合约名称
    "data_sources": [],    # 数据来源列表
}

# 生成时统一从 Slide Config 渲染
def render_slide(prs, config, theme):
    """根据Slide Config渲染单页"""
    if config["type"] == "cover":
        return cover(prs, config["title"], ...)
    elif config["layout"] == "#14 Three-Pillar":
        return PILLAR(prs, config["data"], theme)
    # ...
```

优势：
- ✅ 每页数据独立，便于并行生成
- ✅ 后期修改某页不影响其他页
- ✅ 支持导出为 JSON 作为大纲确认

### S8: 专业技能分析（仅制造领域）
| 专业领域 | 调用技能 | 应用于报告章节 |
|:---------|:---------|:--------------|
| 精益生产诊断 | ie-expert | P7调研发现 |
| 六西格玛分析 | rohoon-6sigma | P16验证成果 |
| 库存分析 | inventory-eye / inventory-demand-planning | P14库存分析 |
| 计划物控 | planning-mc-assistant | P10计划流程 |
| 精益工具 | lean-production-toolkit | P8改善方案 |
| 制造咨询 | manufacturing-consulting-toolkit | 全流程辅助 |
| 数字化转型 | Chief Information Officer | P18数字化规划 |

---

### S8.5: 渐进交付策略选择 — Draft→Iterate→Final 【v6 新增】

借鉴 AI绘图技能的渐进式工作流，支持三阶段交付模式：

```python
class DeliveryMode:
    """渐进交付模式定义"""
    DRAFT = {
        "name": "草稿模式",
        "desc": "快速生成报告骨架：封面+目录+每页Action Title+关键数据标记",
        "sections": "全部章节的L1深度（结论先行）",
        "turnaround": "1-2分钟，快速确认方向",
        "best_for": "需求不确定/需要先确认框架",
    }
    ITERATE = {
        "name": "迭代模式",
        "desc": "在草稿基础上填充：L2分析展开+数据图表+对比分析",
        "sections": "L2深度展开 + 部分L3数据表格",
        "turnaround": "5-10分钟",
        "best_for": "草稿方向确认后逐步完善",
    }
    FINAL = {
        "name": "完整模式",
        "desc": "全质量输出：L3完整细节 + 全数据表格 + 精美排版",
        "sections": "全深度L3展开",
        "turnaround": "10-30分钟（页数不限）",
        "best_for": "终稿交付",
    }
```

**用户交互流程：**

```
您希望以哪种模式生成？
  ○ 草稿模式（快速骨架，确认方向）
  ○ 迭代模式（逐步完善）
  ○ 完整模式（一步到位，推荐 ⭐）

选择 DRAFT → 执行 S9-S12 生成草稿 → 确认 → 升级为 ITERATE
选择 ITERATE → 执行 S9-S12 生成迭代版 → 确认 → 升级为 FINAL
选择 FINAL → 一步执行全部流程
```

**渐进交付规则（R26-R27）：**

| 规则 | 要求 |
|:----|:------|
| **R26** | 默认使用完整模式（Final），除非用户明确要求草稿或迭代 |
| **R27** | 草稿/迭代模式下，AUDIT() 门槛适当降低（密度≥5即可），终版必须全量通过 |

### S9: 编写生成脚本
参考 `references/generate_pro.py` 模板（制造领域）或按通用模板模块规则编写：
1. 导入 python-pptx / lxml
2. 设置常量和配色
3. 按内容驱动模块逐页生成（使用 mck-ppt-design 布局模式），页数由内容量决定
   - 数据丰富时每个模块可拆分为2-4页，不设上限
   - 每个数据点独立制作图表，不合并在一页
   - 每个对比项独立成页，不压缩空间
4. 全微软雅黑，无 BLOCK_ARC
5. 每条文案执行去AI味自检
6. 包含 `full_cleanup()` + `AUDIT()`

---

### S9.5: 格式适配生成 【v6.1 新增 ⭐】

根据 S4 确认的格式选择，将报告内容转换为对应格式：

**格式路由：**

```
                      ┌─ PPT ──→ python-pptx + mck-ppt-design 布局（默认）
  报告内容大纲         │
  (Slide Config JSON) ──┼─ DOCX ─→ python-docx 原生生成
                      │
                      └─ PDF ──→ Markdown → reportlab
```

#### PPT 格式（默认）

使用现有的 python-pptx + mck-ppt-design 引擎，遵循全部 S9 规则：
- 安装依赖：`pip install python-pptx lxml`
- 脚本模板：`references/generate_pro.py`
- 输出扩展名：`.pptx`

#### DOCX 格式

使用 python-docx 生成专业 Word 文档：

```python
# DOCX 生成示例
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# 封面（无页眉页脚）
title = doc.add_heading('', level=0)
run = title.add_run('报告标题')
run.font.name = 'Microsoft YaHei'
run.font.size = Pt(26)
run.font.color.rgb = RGBColor(0x05, 0x1C, 0x2C)

# 章节（Heading 1）
doc.add_heading('章节标题', level=1)

# 正文
p = doc.add_paragraph()
run = p.add_run('正文内容...')
run.font.name = 'Microsoft YaHei'
run.font.size = Pt(11)

# 表格
table = doc.add_table(rows=5, cols=4)
table.style = 'Light Grid Accent 1'

# 保存
doc.save('report.docx')
```

**生成规范：**
| 元素 | DOCX 映射方式 | 说明 |
|:----|:-------------|:-----|
| 封面 | 独立Section+大号标题 | 无页码，与正文分节 |
| 目录 | 自动生成 TOC 字段 | Word中按F9更新 |
| 章节 | Heading 1/2/3 层级 | 对应 PPT 的 Section 和 Action Title |
| 数据表格 | Word 原生表格 | 保留表头深蓝底色 |
| 关键数字 | 加粗+着色段落 | 对应 PPT 的 Big Number |
| 图表 | 简化版柱状图/表格 | DOCX不支持复杂图表，用表格+文字替代 |

- 安装依赖：`pip install python-docx`
- 脚本模板：`references/generate_docx.py`
- 输出扩展名：`.docx`

#### PDF 格式

使用 Markdown→PDF 管道，两条路径可选：

**路径A：reportlab（推荐，零依赖）**
```bash
# 简易PDF生成（md-to-pdf-cjk 方案）
python3 -c "
from md_to_pdf import convert
convert('report.md', '报告标题', 'report.pdf')
"
```

**路径B：Markdown直接转换**
```bash
pip install 'markitdown[all]'
markitdown report.docx -o report.md  # DOCX转MD
# 然后使用 md-to-pdf-cjk 技能转换
```

**生成规范：**
| 元素 | PDF 映射方式 | 说明 |
|:----|:------------|:-----|
| 封面 | 独立首页+大标题 | reportlab Canvas绘制 |
| 章节 | 大号加粗标题 | 对应 PPT 的 Section |
| 正文 | 11pt常规字体 | 微软雅黑嵌入 |
| 表格 | reportlab Table | 保留表头样式 |
| 关键数字 | 大号+着色 | 对应 PPT 的 Big Number |

- 安装依赖：`pip install reportlab markdown`
- 脚本模板：`references/generate_pdf.py`
- 输出扩展名：`.pdf`

**格式规则（R28-R29）：**

| 规则 | 要求 |
|:----|:------|
| **R28** | 无明确格式指令时，默认生成 PPT |
| **R29** | 无论何种格式，内容深度标准一致（L1-L3），不得因格式不同降低质量 |

### S10: 执行生成
根据选择的格式安装对应依赖并执行：

```bash
# PPT格式（默认）
pip install python-pptx lxml
python generate_report.py

# DOCX格式
pip install python-docx
python generate_report_docx.py

# PDF格式
pip install reportlab markdown
python generate_report_pdf.py
```

### S11: 质量审查 + 5-Pass Editor 审校
执行 `AUDIT()` + `full_cleanup()`，按交付检查清单逐项确认。

**5-Pass Editor 自动审校机制**（借鉴内容工厂技能）：

报告生成后，自动执行 5 轮审校：

```python
def editorial_review(draft_content):
    """
    5轮审校流程，每轮聚焦一个维度
    输出：审校后的内容 + 编辑报告
    """
    report = {"passes": [], "changes": []}
    
    # Pass 1: 清晰度手术 — 删除30%冗余，去除填充词和被动语态
    # ▸ "值得注意的是/一般来说/某种程度" → 删除
    # ▸ 长句拆短，每句≤25字
    # ▸ 将被动变主动（"被建议"→"建议"）
    
    # Pass 2: 故事流 — 检查每个章节的因果逻辑
    # ▸ 开头是否有结论句
    # ▸ 段落间是否有逻辑递进
    # ▸ 数据→分析→结论是否完整
    
    # Pass 3: 语气一致性 — 统一为管理咨询权威自信语气
    # ▸ "可能/也许/大概" → "数据显示/分析表明"
    # ▸ "我们希望" → "我们建议"
    # ▸ 禁止使用削弱权威性的措辞
    
    # Pass 4: 质量检查 — 数据完整性核查
    # ▸ 每个数据点是否有来源标注
    # ▸ 对比数据是否完整（before/after成对出现）
    # ▸ Action Title是否完整句子
    
    # Pass 5: 格式化 — 格式/拼写/标点统一
    # ▸ 中英文空格统一
    # ▸ 数字格式统一（"10%" vs "10 %"）
    # ▸ 标点符号全角/半角统一
    
    return edited_content, report
```

**编辑报告示例：**
```
📋 5-Pass Editor 编辑报告
├─ Pass 1 清晰度: 删减28%字数 (2,340→1,685字), 移除填充词12处
├─ Pass 2 故事流: 修复3处因果关系断裂, 补充2个数据支撑
├─ Pass 3 语气一致: 替换5处削弱表述, 统一为"我们建议"语气
├─ Pass 4 质量检查: 发现2个缺失来源标注, 均已补充 ✅
└─ Pass 5 格式化: 统一中英文间距12处, 标点修正5处
```

### S12: 自进化日志（v5 新增）
报告生成完成后，自动写入进化日志：
1. 记录本次使用的内容类型和模板 → `usage_log.json`
2. 记录使用的布局模式及其频率 → `template_stats.json`
3. 如有错误发生 → 写入 `error_log.json`（含修复方案）
4. 更新 `evolution_summary.md` 进化摘要
5. 输出本次进化日志摘要：`💡 自进化：记录本次使用 | 累计X次 | 成功率Y%`

---

### S13: 技能自修复（S13）— 【v6 新增 ⭐】

> **核心思想**：每次PPT生成都是技能自我进化的机会。运行时遇到的任何问题，都要被分析、记录，并自动反馈到 SKILL.md 中，让下一次生成时技能已经\"学会了\"。

#### 第一步：问题收集

在 S0-S12 全过程中捕获所有异常和用户反馈：

```python
def collect_issues():
    """收集本次执行中遇到的所有问题"""
    issues = {
        "errors": [],        # 运行时错误（崩溃/异常）
        "warnings": [],      # 非致命问题（AUDIT未达标/素材缺失）
        "user_feedback": [], # 用户主动反馈（"文件打不开"/"风格不对"）
        "improvements": [],  # 执行过程中发现的可优化点
    }
    # 1. 从 error_log.json 提取新增错误
    # 2. 从 S11 质量审查结果提取未达标项
    # 3. 从用户交互中提取反馈关键词
    # 4. 审计生成脚本，发现可优化的编码模式
    return issues
```

#### 第二步：问题分级

| 级别 | 定义 | 处理方式 | 示例 |
|:----|:-----|:---------|:-----|
| **P0 - 致命** | PPT文件无法打开/崩溃 | 必须修复，追加到「常见错误」+更新 `full_cleanup()` 规范 | 文件损坏需修复 |
| **P1 - 严重** | 内容或排版严重异常 | 追加到「常见错误」+更新相关函数规范 | 中文显示方块 |
| **P2 - 一般** | 单次可修复，不影响整体 | 更新进化日志，暂不修改SKILL.md | 数据源未搜索到 |
| **P3 - 优化** | 可做得更好但非错误 | 记录到 improvements.json，积累多次再批量更新 | 布局模式可更美观 |

#### 第三步：自动修复规则

```python
def auto_repair(issues, skill_base_path):
    """根据收集到的问题自动修复技能文件"""
    for issue in issues["errors"]:
        if issue["level"] != "P0" and issue["level"] != "P1":
            continue
        
        error_text = issue["description"]
        cause_text = issue["root_cause"]
        fix_text = issue["fix"]
        
        # 检查是否已在 SKILL.md 的「常见错误与修复」中
        if not is_already_documented(error_text):
            # 追加新的错误条目
            append_error_to_skill_md(error_text, cause_text, fix_text)
            print(f"🛠️ 自修复：追加错误「{error_text}」到SKILL.md")
        
        # 检查是否涉及函数实现规范
        if issue.get("function_to_update"):
            fn_name = issue["function_to_update"]
            update_function_spec(fn_name, issue["new_spec"])
            print(f"🛠️ 自修复：更新函数 `{fn_name}()` 实现规范")
        
        # 更新交付清单（如发现新的检查项）
        if issue.get("new_checklist_item"):
            append_checklist_item(issue["new_checklist_item"])
            print(f"🛠️ 自修复：追加交付检查项「{issue['new_checklist_item']}」")
    
    # 更新 reference 文件
    if issue.get("new_reference_file"):
        save_reference_file(issue["new_reference_file"])
    
    # 写入进化摘要
    update_evolution_summary(issues)
```

**自修复规则（R19-R22）：**

| 规则 | 要求 |
|:----|:------|
| **R19** | 每次执行后必须执行 S13 自修复分析，不得跳过 |
| **R20** | P0/P1 级问题必须在 SKILL.md 的「常见错误与修复」中有对应条目；如没有，自动追加 |
| **R21** | 函数实现规范变更时，同步更新「助手函数规范」和对应布局函数的文档 |
| **R22** | 新发现的检查项自动追加到「交付检查清单」，并更新版本号 |

#### 第四步：进化日志输出

```
💡 S13 技能自修复报告：
├─ 🔍 本次共发现 2 个问题
├─ ✅ 已修复：full_cleanup() 实现规范更新（原因：p:style替换不够彻底→改为正则删除完整节点）
├─ ✅ 已修复：追加错误「PPTX文件损坏」到常见错误（原因：空a:ln节点残留）
└─ 📊 累计自修复次数：3 | 累计修复条目：7
```

---

### S14: 文件交付与微信推送 — 【v6 新增 ⭐】

> **核心变更**：报告生成完成后，根据输出格式交付对应文件，自动推送到微信小程序。

#### 第一步：交付准备

```python
def prepare_delivery(output_path, output_format):
    """准备交付文件"""
    import os
    
    file_size = os.path.getsize(output_path)
    file_name = os.path.basename(output_path)
    ext_map = {"PPT": ".pptx", "DOCX": ".docx", "PDF": ".pdf"}
    
    delivery_info = {
        "file": output_path,
        "name": file_name,
        "format": output_format,
        "size_kb": round(file_size / 1024, 1),
        "pages": TOTAL_PAGES,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    
    save_delivery_log(delivery_info)
    return delivery_info
```

#### 第二步：交付执行

使用 `deliver_attachments` 工具将文件发送到 WorkBuddy 微信小程序：

```
步骤:
1. 调用 deliver_attachments(file_path) 发送文件
2. 提示用户: "文件已送达！请确保微信WorkBuddy小程序中已开启「产物回传到小程序」开关"
3. 如用户需要自动推送，创建自动化定时任务
```

**交付方式：**
| 方式 | 说明 | 条件 |
|:----|:-----|:-----|
| ✅ `deliver_attachments` | 发送到WorkBuddy微信小程序（推荐） | 用户已绑定微信 |
| 📧 QQ邮件 | 通过qq-email发送邮件附件 | 需配置QQ邮箱授权码 |
| ☁️ 腾讯文档 | 上传到腾讯文档并分享链接 | 需配置tencent-docs |

#### 第三步：自动化交付（可选）

如果用户希望"生成后自动发微信"，创建自动化任务：

```yaml
# 自动化配置
schedule: "每次PPT生成后"
动作: 自动执行 deliver_attachments + 发送通知消息
提示: "用户需开启「产物回传到小程序」开关"
```

**交付规则（R23-R25）：**

| 规则 | 要求 |
|:----|:------|
| **R23** | 每次PPT生成后必须执行 S14 文件交付，不可跳过 |
| **R24** | 交付时必须提示用户检查微信小程序「产物回传到小程序」开关状态 |
| **R25** | 交付成功后写入 `delivery_log.json`，记录文件名称、大小、生成时间 |

---

### S15: PPT结构脑图生成（PDF） — 【v6.1 新增 ⭐】

> **核心功能**：PPT生成完成后，根据 Slide Config 数据自动生成思维导图 PDF，以可视化的方式展现报告的整体结构。

#### 第一步：提取PPT结构数据

```python
def extract_slide_structure(slide_configs):
    """从Slide Config提取脑图层级"""
    mindmap_data = []
    for cfg in slide_configs:
        stype = cfg.get("type", "content")
        if stype == "section":
            mindmap_data.append({
                "type": "section",
                "title": cfg.get("label", "") + " " + cfg.get("title", ""),
                "pages": []
            })
        elif stype in ("content", "cover", "toc"):
            if mindmap_data:
                mindmap_data[-1]["pages"].append(cfg.get("title", "")[:25])
            else:
                mindmap_data.append({
                    "type": "section",
                    "title": cfg.get("title", "")[:25],
                    "pages": []
                })
        elif stype == "closing":
            mindmap_data.append({
                "type": "section",
                "title": "总结与致谢",
                "pages": []
            })
    return mindmap_data
```

#### 第二步：生成脑图PDF

使用 reportlab 绘制层级化的脑图树：

```
├── 🏠 PPT结构大纲
│   ├── 📂 PART 01 精益生产概述
│   │   ├── 📄 精益生产的起源与发展演进
│   │   ├── 📄 核心理念：一个目标两大支柱
│   │   └── 📄 精益屋是TPS经典结构
│   ├── 📂 PART 02 七大浪费
│   │   ├── 📄 TIMWOOD七种浪费总览
│   │   ├── 📄 生产过剩与等待浪费
│   │   └── 📄 加工·库存·动作·不良浪费
│   └── 📂 ...
```

- 安装依赖：`pip install reportlab`
- 脚本模板：`references/generate_mindmap.py`
- 输出扩展名：`.pdf`
- 默认输出路径：`ppt_structure_mindmap.pdf`

#### 第三步：脑图交付

脑图 PDF 随主报告一起交付：

```python
def deliver_mindmap(mindmap_path):
    """随主文件一起交付脑图"""
    deliver_attachments(mindmap_path)
    print(f"🧠 脑图已随报告交付: {mindmap_path}")
```

**脑图规则（R30-R31）：**

| 规则 | 要求 |
|:----|:------|
| **R30** | 脑图为可选项，用户可要求生成或不生成，默认不生成 |
| **R31** | 如用户要求脑图，必须在PPT生成后自动提取结构并生成PDF脑图 |

### 11.1 API依赖安装及离线检查

在执行本技能前，自动检测运行环境和依赖：

```bash
# 安装依赖（需网络，仅首次）
pip install python-pptx lxml python-docx reportlab

# 检测离线组件状态
python3 -c "from references.generate_offline_content import ContentGenerator; g=ContentGenerator(); print(g.get_mode_label())"
```

**离线模式检查清单：**
- [ ] 📦 python-pptx, python-docx, reportlab 已安装（离线环境需提前装好）
- [ ] 🧠 Ollama 已安装并运行（可选，仅本地模型模式需要）
- [ ] 📋 离线模板库已就绪（随skill自带，免安装）

### 11.2 自审（AUDIT）— 质量优先，页数不限 | **多格式适配**

| 检查项 | 合格线 | 说明 |
|:-------|:------:|:-----|
| 图形密度（PPT） | ≥ 10 图/页 | 仅PPT格式检查（DOCX/PDF不适用） |
| 微软雅黑覆盖 | ≥ 80% | 中文全部使用微软雅黑 |
| 无 BLOCK_ARC / DIAMOND | 零容忍 | Mac兼容性检查（仅PPT） |
| 格式完整性 | 100% | 文件可正常打开、无损坏、内容完整 |
| 字体嵌入（PDF） | 必含 CJK | PDF需确保中文字符正确渲染 |

### 11.3 交付检查清单（23项）

**基础质量（必过项）：**
- [ ] ✅ 微软雅黑 + 英文Arial（通过 a:ea 节点设置东亚字体）
- [ ] ✅ 无 BLOCK_ARC / 无 DIAMOND（仅PPT格式）
- [ ] ✅ 使用 mck-ppt-design 布局模式（非自定义图表函数，仅PPT格式）
- [ ] ✅ 执行 full_cleanup()（正则完整移除p:style+空ln+themeShadow，仅PPT格式）
- [ ] ✅ AUDIT() 通过（PPT：图形密度≥10；DOCX/PDF：完整性校验）
- [ ] ✅ 去AI味自检通过（无空洞/浮夸表述）

**内容质量：**
- [ ] ✅ 内容充分展开：每个模块按内容深度自然分页，无因"页数限制"而压缩内容
- [ ] ✅ 用户指定页数时：已按比例压缩但保证完整性和连贯性
- [ ] ✅ 数据呈现：每个数据点获得充分展示空间，不挤在一页
- [ ] ✅ 来源标注完整（三级：用户资料/搜索来源/技能分析）
- [ ] ✅ 用户资料内容已扩增（≥1轮搜索补充）

**素材与设计（v6新增）：**
- [ ] ✅ 素材搜集已执行（素材清单 ≥ 3种类型，≥ 5个条目）
- [ ] ✅ 模板风格已确认（用户确认结果已记录在案）
- [ ] ✅ 素材引用已嵌入生成脚本（图片/图标路径正确）
- [ ] ✅ 配色主题应用正确（theme = apply_theme("xxx") 已调用）

**自进化闭环：**
- [ ] ✅ 自进化日志已写入（usage_log / template_stats 已更新）
- [ ] ✅ 技能发现扫描已执行（known_skills 已更新）
- [ ] ✅ S13 技能自修复已执行（收集问题→分级→写入SKILL.md→更新进化日志）

**文件交付（S14新增）：**
- [ ] ✅ **【v6.1】** 输出格式正确（PPT/DOCX/PDF 按用户选择，默认PPT）
- [ ] ✅ **【v6.1】** 文件扩展名正确（.pptx/.docx/.pdf 对应格式）
- [ ] ✅ **【v6.1】** 格式完整性校验通过（文件可正常打开）
- [ ] ✅ 交付 .pptx 文件（可正常打开，无 Mac 兼容问题）
- [ ] ✅ 文件已推送到微信小程序（deliver_attachments 调用成功）
- [ ] ✅ 用户已收到交付提示（含微信小程序开关引导）

---

## 十二、常见错误与修复

### 错误1：文件损坏打不开（Mac/Win提示"需要修复"）
**原因**：`p:style` 调用主题阴影引用 + 空 `a:ln` 节点 + `typeface` 属性缺失 → XML结构不完整导致PowerPoint修复提示
**修复**：
- `full_cleanup()` 必须使用 **正则表达式彻底移除**（而非字符串替换），删除所有 `<p:style>...</p:style>` 完整节点
- 清理空 `<a:ln/>` 节点（没有子元素的线条定义）
- 移除 `<a:themeShadow>` 主题阴影引用
- 确保每个 `<a:latin>` 有 `typeface="Arial"`，每个 `<a:ea>` 有 `typeface="Microsoft YaHei"`
- 每个 shape 调用 `cs(s)` 清理残留 XML

### 错误2：中文显示方块
**原因**：未设置东亚字体
**修复**：
```python
def sf(run, is_en=False):
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn('a:latin'))
    if latin is None:
        latin = rPr.makeelement(qn('a:latin'), {})
        rPr.append(latin)
    latin.set('typeface', EN if is_en else FN)
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', FN)
```

### 错误3：Mac上图形显示异常
**原因**：BLOCK_ARC 或复杂形状不被Mac PowerPoint支持
**修复**：确保没有使用 `MSO_SHAPE.BLOCK_ARC`，所有圆环/饼图改用表格或柱状图替代。

### 错误4：文字重叠
**原因**：行间距未设置或使用固定Y坐标
**修复**：
- 设置 `p.line_spacing = Pt(font_size * 1.35)` 防止中文重叠
- 多行文本动态计算高度
- 验证每个文本块的 `top + height` 不超出下一块的 `top`

### 错误5：connector 导致崩溃
**原因**：`add_connector()` 生成的 connector 在 Mac 上可能异常
**修复**：用 `add_hline()`（薄矩形）替代所有 connector 和连线

### 错误6：markitdown 未安装导致资料提取失败
**原因**：环境未安装 markitdown
**修复**：
- 方法A：尝试 `pip install 'markitdown[all]'`
- 方法B：使用 `Read` 工具直接读取（PDF/图片/文本）
- 方法C：使用 `WebFetch` 读取网页内容
- 方法D：使用 `python-pptx` 读取 PPTX 文字

### 错误7：OCR识别结果不准确
**原因**：图片质量差或文字不清晰
**修复**：
- 手动校对关键数据点
- 有疑问的数据标注"待确认"
- 建议用户提供清晰版本或核对

### 错误8：素材搜集无有效结果 【v6 新增】
**原因**：搜索关键词过于宽泛或行业特殊
**修复**：
- 方法A：缩小搜索范围，添加限定词（"报告"、"案例"、"最佳实践"）
- 方法B：使用中英双语各搜一次，互补结果
- 方法C：降级使用内置占位图标（ICON函数生成），跳过搜集
- 方法D：告知用户未找到高质量素材，建议提供参考

### 错误9：模板风格用户不满意 【v6 新增】
**原因**：自动推荐风格与用户预期不符
**修复**：
- 提供4种风格预览描述，让用户重新选择
- 记录用户选择到 usage_log 改善下次推荐
- 如果用户反复调整，最终保存用户手动选定的风格

---

## 十三、技能自进化系统

### 13.1 系统定位

这是技能持续进步的核心引擎。每次使用本技能时，自进化系统自动运行，实现三个目标：

1. **发现新能力** — 扫描系统中有无新增的相关技能，自动集成
2. **学习与改进** — 记录每次执行的结果、错误和改进建议
3. **持续优化** — 根据使用频率自动优化模板选择和布局推荐

### 13.2 技能发现引擎

每次技能被调用时，自动执行技能发现扫描：

```python
# 技能发现流程
def scan_new_skills():
    """扫描 ~/.workbuddy/skills/ 发现新技能"""
    known = load_known_skills()      # 加载已知技能列表
    all_skills = listdir_skills()     # 扫描当前所有技能

    new_skills = []
    for skill in all_skills:
        if skill not in known:
            relevance = assess_relevance(skill)  # 评估相关性
            if relevance >= threshold:
                new_skills.append(skill)
                auto_integrate(skill)   # 自动集成
    
    if new_skills:
        notify_user(new_skills)        # 通知用户
        update_known_skills(new_skills) # 更新已知列表
```

**技能发现规则：**

| 规则 | 说明 |
|:----|:------|
| **R10** | 每次技能加载时执行一次发现扫描 |
| **R11** | 相关性评估基于 SKILL.md 中的 description 关键词匹配 |
| **R12** | 发现的技能自动加入技能生态矩阵 |
| **R13** | 新技能信息存储在 `self_evolution/` 目录 |
| **R14** | 与现有技能同名的忽略（已有则跳过） |

**已发现的技能生态（当前 22 个已集成）：**

| 领域 | 技能 | 用途 |
|:----|:-----|:-----|
| 分析诊断 | ie-expert, rohoon-6sigma, kaizen, sixsigma | 工业工程/六西格玛分析 |
| 库存分析 | inventory-eye, inventory-demand-planning | 库存优化 |
| 计划物控 | planning-mc-assistant, supply-chain-bom-analyzer | 排产/物料分析 |
| 精益工具 | lean-production-toolkit, manufacturing-consulting-toolkit | 精益方法论 |
| 深度研究 | academic-deep-research, deep-research-pro, research-cog, arxiv-watcher, news-summary | 多源交叉验证/证据层次/三轮调研（v5.1新增） |
| 通用分析 | chart-visualization, data-analysis-report | 图表/数据/研究 |
| 战略规划 | cio, change-management-plan, content-factory | 战略/变革/内容 |
| 设计引擎 | mck-ppt-design | 麦肯锡风格PPT布局 |
| 进化辅助 | self-improving-agent, self-reflection, proactive-agent | 自进化框架 |
| 润色输出 | humanizer-zh, humanizer, manufacturing-expert | 去AI味/专业润色 |

### 13.3 进化数据存储

系统在 `self_evolution/` 目录中维护以下文件：

```
self_evolution/
├── known_skills.json       # 已知技能列表（含版本、发现日期）
├── usage_log.json          # 使用记录（模式频率、执行结果）
├── error_log.json          # 错误日志（错误类型、修复方案）
├── improvements.json       # 改进建议（用户反馈、自动发现）
├── template_stats.json     # 模板使用统计（频率、评分）
└── evolution_summary.md    # 进化摘要（供每次加载时参考）
```

### 13.4 自进化执行流程

每次技能被调用时，自进化系统按以下流程执行：

```
技能被调用
     │
     ▼
┌── S0: 自进化检查（与内容分析同时执行）
│     1. 加载进化数据（known_skills, usage_log）
│     2. 扫描新技能（scan_new_skills）
│     3. 检查上次错误是否已修复
│     4. 加载高频使用的布局模式偏好
│
     ▼
┌── S1-S12: 正常报告生成流程
│     （期间自动记录使用情况）
│
     ▼
┌── 执行后：写入进化日志
     │
     ├── 记录本次使用的内容类型和模板
     ├── 记录使用的布局模式及其频率
     ├── 如有错误 → 写入 error_log（含修复方案）
     ├── 更新 template_stats（优化下次推荐）
     └── 更新 evolution_summary.md
```

### 13.5 自我提升机制

```python
# 每次执行后的自我评估
def self_improve(execution_result):
    """根据执行结果进行自我改进"""
    improvements = []
    
    # 1. 布局模式使用分析
    mode_usage = analyze_mode_usage(execution_result)
    for mode, count in mode_usage.items():
        if count > 5:  # 高频使用的模式
            improvements.append(f"优化模式 {mode} 的默认参数")
    
    # 2. 错误模式分析
    errors = execution_result.get('errors', [])
    for err in errors:
        if err['type'] == 'font':
            improvements.append("字体配置需要优化")
        elif err['type'] == 'shape':
            improvements.append(f"形状 {err.get('shape')} 需要加清理守卫")
    
    # 3. 用户反馈分析
    if execution_result.get('user_satisfied') == False:
        improvements.append("用户不满意，需审查输出质量")
    
    # 4. 技能生态更新建议
    if execution_result.get('new_skills_found'):
        improvements.append("发现新技能，建议集成")
    
    return improvements
```

### 13.6 每日技能巡检自动化

配合 WorkBuddy 的自动化功能，可设置每日技能巡检：

```yaml
# 自动化配置建议
schedule: 每天 09:00
动作: 执行技能发现扫描
输出: 报告新发现的技能及集成建议
```

**执行方式**：
- 在 WorkBuddy 中创建自动化任务，定期运行巡检
- 或每次使用本技能时自动附带检查
- 发现新技能时，在报告中输出「💡 提示：发现新技能 XXX，可集成使用」

### 13.7 进化数据分析示例

| 指标 | 说明 | 使用方法 |
|:----|:-----|:---------|
| 模式使用频率 | 每种布局模式被调用的次数 | 推荐高频模式作为优先选项 |
| 模板选择准确性 | 内容类型诊断与用户反馈的一致率 | 优化 detect_content_type() 权重 |
| 错误率 | 每次执行出现错误的概率 | 优先修复高频错误 |
| 技能集成率 | 已集成技能占可用技能的比例 | 发现遗漏的技能进行集成 |
| 用户满意度 | 用户对生成结果的反馈评分 | 优化模板和内容质量 |

### 13.8 与自进化系统对接

本技能与以下自进化框架技能协同工作：

| 技能 | 用途 | 对接方式 |
|:----|:-----|:---------|
| self-improving-agent | 对话质量分析，识别改进机会 | 共享 evolution_summary.md |
| self-reflection | 结构化反思与记忆 | 共享错误日志和学习记录 |
| proactive-agent | 将 AI 从任务执行者变为主动伙伴 | 自动建议模板优化 |

### 13.9 技能自修复机制（S13）— 【v6 新增 ⭐】

#### 机制定位

**S13 是最新的一层闭环**：每次执行 PPT 生成时，如果遇到问题并找到了修复方案，该方案会被自动"写回"到 SKILL.md 中。这意味着下一次生成时，技能已经升级了——不再是"记住上次错了"，而是"技能文件本身就更新了"。

#### 闭环架构

```
生成 → 发现问题 → 分析根因 → 修复 → 写入SKILL.md → 下次直接受益
 ↑                                                            │
 └────────────────── 每次执行都在这个循环中升级 ────────────────┘
```

与传统的「错误日志」不同，S13 的修复是**持久化到技能文件本身**的：

| 对比项 | 传统错误日志 | S13 自修复 |
|:-------|:-----------|:-----------|
| 存储位置 | `self_evolution/error_log.json` | **SKILL.md + references/\*** |
| 下次生效 | 需手动翻阅日志 | **自动生效**（SKILL.md已更新） |
| 影响范围 | 仅查看 | 所有使用该技能的人 |
| 更新方式 | 追加一条记录 | **修改技能代码/文档** |
| 错误类型 | P0-P3全部记录 | 仅P0/P1级触发自动修复 |

#### 触发时机

S13 在以下场景自动触发：

1. **S11 质量审查未通过** — AUDIT() 发现图形密度不足/存在 BLOCK_ARC
2. **用户报告文件错误** — 如"打不开"、"需要修复"、"字体显示异常"
3. **用户反馈内容问题** — 如"数据不对"、"排版混乱"、"来源不清晰"
4. **生成脚本执行异常** — python-pptx 报错、脚本运行中断
5. **素材搜集失败** — 联网搜索无结果或结果质量差

#### 修复类型与对应操作

| 发现问题 | 自修复操作 | 修改SKILL.md的位置 |
|:---------|:----------|:------------------|
| PPT文件提示"需要修复" | 更新 `full_cleanup()` 实现规范 | 「常见错误1」+「助手函数：full_cleanup」|
| 中文显示方块 | 更新字体设置规范 | 「常见错误2」+「6.3字体规范」|
| 文字重叠 | 更新行间距和动态高度规则 | 「常见错误4」+「布局函数TX()规范」|
| 图片无法嵌入 | 更新图片嵌入方式 | 新增到「常见错误」|
| 用户重复选择同一风格 | 将该风格设为默认推荐 | 「6.6配色主题·自动选择逻辑」|
| 某个布局模式频繁使用 | 将该模式列为默认首选项 | 「6.1布局模式·推荐列表」|
| 搜索不到合适素材 | 更新搜索关键词方案 | 「S6.5·素材搜集·搜索词表」|

#### 配套参考文件

| 文件 | 说明 |
|:----|:------|
| `references/self_repair.py` | S13 自修复引擎脚本（问题收集→分级→自动修复→进化日志） |
| `references/repair_pptx.py` | 深度PPTX修复工具（专用于"文件损坏需修复"问题的解决方案） |

#### 自修复示例：以本次 full_cleanup() 修复为证

本次执行中，用户反馈 PPTX 在 PowerPoint 中提示"需要修复"：

1. **问题收集**：用户反馈「文件打不开」
2. **根因分析**：`full_cleanup()` 使用 `replace('<p:style', '<!-- ... -->')` 字符串替换，未完整移除 XML 节点，导致 PowerPoint 解析异常
3. **修复方案**：改为 `re.sub(r'<p:style[^>]*>.*?</p:style>', '', content, flags=re.DOTALL)` 正则彻底删除 + 清理空 `<a:ln/>` + 移除 `a:themeShadow`
4. **自修复写入**：
   - ✅ 更新「常见错误1：文件损坏打不开」的修复方案
   - ✅ 更新「助手函数：full_cleanup()」的实现描述
   - ✅ 新增 `references/repair_pptx.py` 独立修复脚本作为参考
5. **效果确认**：重新生成的文件PowerPoint可正常打开

这就是 S13 的实际运作——一次"边用边修，修完即升级"的闭环修复。

---

## 十四、参考文件

| 文件 | 说明 |
|:----|:------|
| `references/generate_pro.py` | v5 完整PPT生成脚本模板 |
| `references/generate_docx.py` | v6.1 DOCX生成脚本模板（基于python-docx） |
| `references/generate_pdf.py` | v6.1 PDF生成脚本模板（基于reportlab） |
| `references/extract_content.py` | v4 资料提取脚本模板（PDF/Word/Excel/图片OCR/PPTX） |
| `references/self_evolution.py` | v5 自进化系统脚本（技能发现+使用追踪+错误学习） |
| `references/self_repair.py` | v6 S13 技能自修复引擎（问题收集→分级→自动写入SKILL.md） |
| `references/report-templates.md` | 各类型报告详细页面结构模板 |
| `references/consulting-phrases.md` | 咨询报告专业用语模板 |
| `references/requirements-summary.md` | 完整需求规格文档 |
| `references/repair_pptx.py` | v6 深度PPTX修复脚本（正则移除p:style+空ln+themeShadow） |
| `references/generate_mindmap.py` | v6.1 PPT结构脑图PDF生成脚本（基于reportlab） |
| `references/generate_offline_content.py` | v6.1 离线内容生成引擎（Ollama/模板双回退） |
| `references/deep_research.py` | v5.1 深度研究脚本（多源交叉验证+证据层次+三轮调研） |

---

## 十五、深度研究引擎（v5.1 新增）

### 15.1 功能定位

在内容扩增子系统基础上，增加**深度研究能力**。当用户材料中的关键数据点需要行业佐证、或者报告需要更深层次的市场分析时，启用本引擎进行多源交叉验证研究。

### 15.2 研究框架（三阶段）

```
┌─ 第一阶段：需求澄清 ─────────────────────────────────┐
│  识别材料中的关键数据点 → 需要佐证的断言 → 行业空白   │
│  输出：研究需求清单（3-5个研究主题）                   │
└─────────────────────────────────────────────────────────┘
     │ 用户确认
     ▼
┌─ 第二阶段：多源调研 ─────────────────────────────────┐
│  每个主题执行：                                        │
│  ├─ 第1轮：广度搜索（5-10个来源）                     │
│  ├─ 第2轮：深度提取（关键来源详细分析）               │
│  └─ 第3轮：交叉验证（不同来源对比验证）               │
└─────────────────────────────────────────────────────────┘
     │ 自动执行
     ▼
┌─ 第三阶段：数据融合 ─────────────────────────────────┐
│  将研究结果与用户原始材料融合                         │
│  ├─ 用户数据 ✓                                        │
│  ├─ 搜索佐证 ✓                                        │
│  └─ 综合分析 ✓                                        │
└─────────────────────────────────────────────────────────┘
```

### 15.3 三级证据体系

| 等级 | 来源类型 | 可信度 | 标注格式 |
|:----|:---------|:------:|:---------|
| L1 | 用户提供的原始材料 | ★★★ | "数据来源：用户资料" |
| L2 | 权威行业报告/政府数据 | ★★★ | "来源：XXX（年份）" |
| L3 | 专业媒体报道/企业公开信息 | ★★☆ | "来源：XXX·YYYY-MM-DD" |
| L4 | 通用网络搜索结果 | ★☆☆ | "来源：网络搜索" |

### 15.4 研究触发条件

| 条件 | 自动触发 | 说明 |
|:----|:--------:|:-----|
| 材料中包含具体数字指标 | ✅ | 自动搜索行业基准对标 |
| 材料提及竞争对手或行业趋势 | ✅ | 搜索最新动态补充 |
| 材料中有政策/法规引用 | ✅ | 验证政策时效性 |
| 用户明确要求"深度研究" | ✅ | 完整三阶段执行 |
| 仅做PPT排版 | ❌ | 跳过研究 |

### 15.5 与现有工作流的集成

深度研究引擎嵌入 S3（内容扩增）阶段，在关键数据点识别后自动判断是否需要执行研究。

### 15.6 研究执行规范

```
第1轮 - 广度搜索: web_search(query, count=10) → 初始发现摘要
第2轮 - 深度提取: web_fetch(top_3_results) → 详细内容+关键数据
第3轮 - 交叉验证: web_search(alternative_terms) + web_fetch → 多源对比
```

### 15.7 研究技能生态对接

| 技能 | 用途 | 触发场景 |
|:----|:-----|:---------|
| academic-deep-research | 严谨学术级研究 | 需要APA引用、文献综述 |
| deep-research-pro | 多阶段迭代调研 | 市场调研、竞品分析 |
| research-cog | AI深度研究 | 投资研究、行业分析 |
| arxiv-watcher | ArXiv论文摘要 | 最新技术研究成果 |
| news-summary | 新闻资讯抓取 | 行业最新动态和热点 |

---

## 十六、本地与离线模式（v6.1 新增 ⭐）

> 本技能可自动适配三种运行环境：**在线模式**（标准）、**本地模型模式**（Ollama）、**完全离线模式**（无网络+无模型）。
> 无需用户手动配置，自动检测并切换。

### 16.1 三种运行模式

| 模式 | 网络 | 本地模型 | 内容来源 | 适用场景 |
|:----|:----:|:--------:|:---------|:---------|
| ☁️ **在线模式** | ✅ 有网 | — | WebSearch + API | 标准使用（默认） |
| 💻 **本地模型模式** | ❌ 无网 | ✅ Ollama | 本地模型生成 | 内网/离线但有GPU |
| 📦 **完全离线** | ❌ 无网 | ❌ 不可用 | 内置离线模板库 | 隔离网络/纯本地 |

### 16.2 自动检测逻辑

```python
def detect_mode():
    """自动检测并切换运行模式"""
    if check_network():
        return "online"        # 有网络 → 标准在线模式
    if check_ollama():
        return "local_model"   # 无网络但有Ollama → 本地模型
    return "offline"           # 完全离线 → 使用内置模板
```

### 16.3 离线内容模板库

内置 **10个行业标准章节模板** + **3个离线案例库**，确保完全离线时也能生成专业内容：

| 模板ID | 内容 | 字数 |
|:------|:-----|:----:|
| lean_intro | 精益生产概述 | ~200字 |
| seven_wastes | 七大浪费详解 | ~200字 |
| jit | 准时化JIT | ~150字 |
| jidoka | 自働化Jidoka | ~150字 |
| kaizen | 持续改善Kaizen | ~150字 |
| tpm | TPM全面生产维护 | ~150字 |
| smed | SMED快速换模 | ~150字 |
| 5s | 5S现场管理 | ~150字 |
| oee | OEE与性能衡量 | ~150字 |
| case_studies | 3个离线行业案例 | ~300字 |

### 16.4 Ollama 本地模型配置

如需使用本地模型模式，确保：

```bash
# 1. 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型（需要一次联网）
ollama pull gemma4:e2b-it-q4_K_M

# 3. 启动服务
ollama serve
```

技能自动通过 `http://localhost:11434` 调用 Ollama API。

### 16.5 离线模式工作流变更

在离线模式下，以下步骤自动降级：

| 步骤 | 在线模式 | 本地模型模式 | 完全离线模式 |
|:----|:---------|:------------|:------------|
| **S3 内容扩增** | WebSearch行业数据 | Ollama生成内容 | **离线模板库** |
| **S5 联网调研** | 多引擎搜索 | 跳过调研 | **跳过调研** |
| **S6.5 素材搜集** | WebFetch搜图 | 使用本地ICON | 使用本地ICON |
| **S9 脚本生成** | Python全量脚本 | Python全量脚本 | **Python全量脚本** |
| **S10 执行** | pip安装+执行 | pip安装+执行 | pip安装+执行 |

> **核心保障**：PPT/DOCX/PDF/Mindmap 的生成和格式输出**完全不依赖网络**，离线不影响。
> 离线仅影响内容扩增和素材搜集——降级使用内置模板和ICON占位符。

### 16.6 离线模式标记

生成的PPT在离线模式下，页面底部来源标注自动切换：

```python
# 在线模式
SR(s, "来源：Evocon全球OEE基准报告·2024")

# 离线模式
SR(s, "来源：离线内容模板库（consulting-report-generator v6.1）")
```

### 16.7 参考脚本

| 文件 | 说明 |
|:----|:------|
| `references/generate_offline_content.py` | 离线内容生成引擎（自动检测→切换模式→Ollama/模板回退） |
