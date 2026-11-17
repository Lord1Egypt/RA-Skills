---
name: report-builder
version: 2.1.1
description: |
  📥 openclaw skill install dabin0927/executive-briefing
  ——
  给老板汇报不用写 PPT，一页纸让他 3 分钟拍板。
  自动把几十页方案压缩成决策摘要：结论直接给、数据会说话、行动能落地。
  BLUF 一页纸 + So What 叙事 + 脚本化工具链（init/bump/validate/density）。
  适合：向 CEO/董事会/投资人汇报、决策备忘录、管理简报。
  不适合：技术文档、数据分析图表、PPT 排版。
  (EN) One-page executive briefing factory — BLUF + scripts + templates.
tags:
  - 高管汇报
  - 决策支持
  - 一页纸
  - executive
  - reporting
author: claude-learning-project 📚
metadata:
  openclaw:
    cacheBoundary: on-demand
    emoji: "📋"
    tier: "application"
    maturity: "stable"
    requires:
      bins: [python3]
      env: []
      config: []
    dependencies:
      - markdown-to-html
  pattern: "Executive Report Builder"
  output-format: "md + html"
  upstream: solution-architect, digital-research
  downstream: markdown-to-html
  clawhub:
    tags:
      - "executive"
      - "decision-support"
      - "reporting"
      - "briefing"
    language: "zh,en"
triggers:
  - "高管汇报"
  - "executive briefing"
  - "executive summary"
  - "一页纸"
  - "one-pager"
  - "board report"
  - "决策摘要"
  - "向领导汇报"
  - "管理层报告"
  - "report builder"
  - "简报"
  - "decision memo"
  - "董事会汇报"
---

> 🚀 **一键安装：** `openclaw skill install dabin0927/executive-briefing`

---

# Report Builder — 高管汇报内容工厂 V2.1

**定位：** 输入详细方案/参考资料 → 提炼→分层→转译→叙事→校验 → 输出面向高层的决策导向报告。

**核心差异化：** 业界唯一有自动化脚本链的高管报告 SKILL。竞品（Anthropic Executive Briefing 等）全是纯 Prompt 驱动，我们是 Prompt + 脚本 + 模板 + 校验四层体系。

---

## 🚦 使用决策表

| 场景 | 用 report-builder？ | 替代方案 |
|------|:--:|------|
| 需要把 30 页详案压缩为一页纸 | ✅ 核心场景 | — |
| 需要向高管/董事会做决策汇报 | ✅ 核心场景 | — |
| 需要写技术文档/API 文档 | ❌ 不适用 | technical-writer SKILL |
| 需要做数据分析图表 | ❌ 不适用 | data-analysis SKILL |
| 需要生成 PPT | ❌ 不适用 | → markdown-to-html (presentation 模板) |
| 需要写完整调研报告（>5页） | ❌ 不适用 | solution-architect SKILL |
| 只是排版美化 | ❌ 不适用 | markdown-to-html SKILL |
| 输入材料 <500 字 | ⚠️ 收益低 | 直接阅读原文档即可 |

### 报告质量状态生命周期

```
Draft → Validate → Fix → Re-validate → A级 → 定稿
  ↑                                      ↓
  └──────── 修复后重走 ─────────── B/C级 ←
                                        ↓
                                      D级 → 重写
```

| 评级 | 条件 | 动作 |
|:--:|------|------|
| A | 7项校验全通过 | ✅ 可定稿发布 |
| B | ≥5项通过 | ✅ 可发布，标注改进项 |
| C | 3-4项通过 | ❌ 需整改，重新 validate |
| D | <3项通过 | ⛔ 重写，结构性缺陷 |

---

## 5 步处理流水线

```
输入详案（md/doc/pdf）
    │
    ▼
[Step 1] 信息提取 → 提取结论/数据/决策点，剔除过程描述
    │
    ▼
[Step 2] 分层映射 → 按高管阅读习惯重排：结论→论据→背景（BLUF）
    │
    ▼
[Step 3] 语态转译 → 技术术语→业务影响，段落→要点+表格
    │
    ▼
[Step 4] 叙事构建 → 应用标准模板，一页纸强制产出
    │
    ▼
[Step 5] 质量校验 → 结论清晰度/数据支撑度/行动明确性自动检查
    │
    ▼
  输出：高管报告（md + html）
```

---

## 输出结构（Anthropic BLUF 格式）

```
═══════════════════════════════════════════════════════════
高层汇报：[主题]
日期：[日期] | 呈送：[受众]
═══════════════════════════════════════════════════════════

核心结论（BOTTOM LINE）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2-3句：必须知道什么 + 需要做什么决策]

关键发现（KEY FINDINGS）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [发现1 — 附数据支撑]  [置信度：HIGH]
• [发现2 — 附数据支撑]  [置信度：MEDIUM]
• [发现3 — 附数据支撑]  [置信度：LOW]

业务影响（IMPLICATIONS）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[So What — 对收入/成本/风险/竞争的具体影响]

建议行动（RECOMMENDED ACTIONS）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
按 预期影响 ÷ 所需投入 排序：
1. [行动] — [负责人] — [时间线]
2. [行动] — [负责人] — [时间线]

需要您决策的事项（DECISION REQUIRED）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[明确列出需要高层拍板的事项]

风险与考量（RISKS & CONSIDERATIONS）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [风险/考量]
• [不作为的后果]

═══════════════════════════════════════════════════════════
来源：[简要引用] | 联系人：[问题找谁]
═══════════════════════════════════════════════════════════
```

---

## 受众适配指南

> 不同受众关心不同问题。一个模板不行。

| 受众 | 第一句话问什么 | 篇幅 | 核心关注 | 推荐模板 |
|------|---------------|:--:|------|---------|
| **CEO/总经理** | 对营收/利润的影响？ | 1页 | 财务影响、战略定位、竞争格局 | `executive-summary` |
| **董事会** | 治理风险？是否符合战略？ | 1-2页 | 风险、合规、长期价值 | `board-briefing` |
| **投资人** | 回报率？为什么现在？ | 1页 | ROI、市场规模、退出路径 | `one-pager` |
| **部门负责人** | 对我团队的影响？要做什么？ | 1页 | 资源需求、时间线、跨部门协调 | `decision-memo` |
| **政府/公共部门** | 公众利益？政策对齐？ | 1-2页 | 社会效益、合规、成本效益 | `executive-summary` |

### 受众适配检查清单

- [ ] 报告第一句是否直接回答了该受众最关心的问题？
- [ ] 数据呈现是否用了该受众熟悉的语言（CFO 看财务指标，CTO 看技术指标）？
- [ ] 决策建议是否具体到该受众有权拍板的范围？
- [ ] 篇幅是否控制在受众的阅读耐心内（CXO ≤3分钟，董事会 ≤5分钟）？

---

## 报告评分量表（0–40）

> 此评分系统对标 ClawHub 头部竞品 `executive-summary`（210 安装），提交给受众前必须自评 ≥32 分。

| 维度 | 0分 | 5分 | 10分 |
|------|-----|-----|------|
| **结论前置** | 结论埋在最后或缺失 | 有结论但被背景铺垫稀释 | 核心结论在前 3 句内，一眼可见 |
| **独立可读** | 必须读原文才能理解 | 基本自包含，但有未解释的术语 | 无需任何背景材料即可理解并决策 |
| **可行动性** | 只有"建议考虑"，无 Owner/日期 | 建议具体但缺执行细节 | 每项行动有 Owner + 日期 + 不作为后果 |
| **受众适配** | 同一份报告发给所有人 | 针对某个角色但不够精准 | 针对具体受众的决策场景量身定制 |

**评级：**
- 🏆 **36-40 分**：A 级 — 可直接发给 CEO
- ✅ **32-35 分**：B 级 — 可发送，有小改进空间
- ⚠️ **24-31 分**：C 级 — 需整改
- ❌ **<24 分**：D 级 — 重写

> 也可以用 `scripts/validate.py <file>` 自动校验，输出结构化评分 JSON。

---

## ⚠️ 常见反模式

> 以下做法会让高管直接跳过你的报告。对标竞品 `executive-update`/`executive-summary`（均已明确列出反模式）。

| 反模式 | 为什么致命 | 正确做法 |
|------|----------|------|
| **按时间顺序复述原文** | 高管不关心"先做了什么后做了什么"，只关心结论 | 结论文本前置（BLUF），背景放附录 |
| **把建议埋在段落中间** | 高管只读第一段就跳走，错过关键决策信息 | 决策事项独立成节，加粗标注 |
| **没有对比基准的数据** | "增长 15%" 无意义 — 跟什么比？目标是多少？ | 每个数据附对比基准（同比/环比/目标值） |
| **粉饰或弱化风险** | 高管依赖报告做决策，美化的风险 = 错误决策 | 坏消息不延迟、不粉饰。"风险：客户可能流失 15%" |
| **决策项没有推荐方案** | 让高管自己做分析工作，等于没写报告 | 每项决策给 2-3 个方案 + 明确推荐 + 理由 |
| **超过 500 词** | 长度说明作者没做好压缩工作。超线 = 没读 | 500 词硬上限，超出部分裁剪入附录 |
| **技术术语堆砌** | 高管不是工程师，"QPS 下降 30%" vs "系统慢了 1/3" | 用业务语言翻译所有技术概念 |
| **被动语态**"被建议" | 显得缺乏信心，不敢担责 | 用主动语态："我们建议"，"推荐 X 方案" |

### ✅ 必须做

| 规则 | 来源 |
|------|------|
| **结论前置**：第一句就给出结论，不铺垫 | Anthropic / zhasty007 |
| **500 词硬上限**：全篇不超过 500 词 | zhasty007 |
| **用数字说话**：能用量化就不用形容词 | Anthropic |
| **建议含 Owner + Timeline**：不说"建议考虑"，说"XX 负责，Q3 前完成" | Anthropic |
| **标注置信度**：每项关键发现标注 HIGH/MEDIUM/LOW | Anthropic |
| **So What 检查**：每段读完能回答"所以呢？" | Recipe-060 |
| **受众先行**：开始前确认"谁读、做什么决策、已有多少上下文" | zhasty007 |

### ❌ 禁止做

| 规则 | 来源 |
|------|------|
| **不发明数字**：源材料没有的数据绝对不编 | zhasty007 |
| **不用被动语态**：不说"被建议"，说"我们建议" | Anthropic |
| **不用术语**：技术概念必须用业务语言翻译 | Anthropic |
| **不要过程描述**：不说"我们分析了 47 个品类"，说"采购成本可降 1200 万" | zhasty007 |
| **不要副词**：significantly/potentially/approximately 除非确有必要，一律删除 | zhasty007 |
| **不堆砌背景**：详细内容放附录，主体只放结论 | Anthropic |

---

## 数据呈现规则

| 规则 | 示例 |
|------|------|
| 数字四舍五入 | "$2.3M" 而非 "$2,347,892" |
| 对比基准 | "同比增长 15%" 而非 "增长 15%" |
| 用 relatable 比较 | "3 倍快" 而非 "200% 提升" |
| 突出 delta | "从 3.8% 升至 4.2%（↑0.4pp）" |

---

## 自动化工具链

| 脚本 | 用途 | 用法 |
|------|------|------|
| `scripts/init.py` | 新建报告脚手架 | `python3 init.py "报告名称" --template executive-summary` |
| `scripts/bump.py` | 版本升级+新文件生成+变更摘要 | `python3 bump.py --major\|--minor\|--patch` |
| `scripts/validate.py` | 内容质量校验（结论/数据/行动/篇幅/置信度） | `python3 validate.py <file> [-o report.json]` |
| `scripts/density.py` | 内容密度分析（段落长度/数据占比/空洞检测） | `python3 density.py <file>` |

---

## 模板体系

| 模板 | 适用场景 | 阅读时长 |
|------|---------|---------|
| `templates/executive-summary.md` | 通用高管摘要（BLUF 格式） | ≤3 分钟 |
| `templates/decision-memo.md` | 决策备忘录（需要拍板的事项） | ≤5 分钟 |
| `templates/one-pager.md` | 一页纸汇报（极简版） | ≤2 分钟 |
| `templates/board-briefing.md` | 董事会汇报 | ≤5 分钟 |

---

## 工作目录约定

```
reports/{报告名称}/
├── README.md                     # 版本索引
├── VERSION.md                    # 版本历史
├── 01-{报告名称}-v1.0.0.md       # 文件名三段式：序号-主题-版本
├── 01-{报告名称}-v1.0.0.html     # 定稿 HTML
├── 01-{报告名称}-v2.0.0.md
├── 01-{报告名称}-v2.0.0.html
└── appendix/                     # 附录（详细数据/方法论/技术细节）
```

---

## 与其他 SKILL 协作

| SKILL | 触发条件 | 协作方式 |
|-------|---------|---------|
| `solution-architect` | 详案来源 | 接收方案文档作为输入 |
| `digital-research` | 需要行业数据 | 委托调研，结果注入报告 |
| `markdown-to-html` | 报告定稿 | 输出 HTML 版本 |
| `plantuml-generator` | 需要架构图 | 生成图表嵌入报告 |

> 详见 `references/collaboration-workflow.md`

---

## 📂 参考文档索引

| 文档 | 内容 |
|------|------|
| `references/style-guide.md` | 高管语态手册（中英文写作规范） |
| `references/narrative-methodology.md` | 叙事方法论（BLUF/金字塔/So What框架） |
| `references/structure-validation.md` | 校验规则详解与 JSON 输出格式 |
| `references/edge-cases.md` | 边界情况处理策略 |
| `references/collaboration-workflow.md` | 与其他 SKILL 的协作流程 |
| `templates/executive-summary.md` | 通用高管摘要模板 |
| `templates/decision-memo.md` | 决策备忘录模板 |
| `templates/one-pager.md` | 一页纸汇报模板 |
| `templates/board-briefing.md` | 董事会汇报模板 |

---

## 约束

- ✅ 任何内容变更 = 升版 + 新文件
- ✅ 默认「注入」模式，旧内容不删不改
- ❌ 禁止覆盖旧版本文件
- ❌ 禁止手动修改版本号（统一通过 `scripts/bump.py`）
- ❌ 禁止 `pip install` / `npm install` / `apt install`
- ❌ 不要把 md→html 转换逻辑放进本 SKILL（用 markdown-to-html）
- ❌ 不要输出超过 500 词的报告主体（附录不计算在内）

---

*V2.1 — 基于 Anthropic Executive Briefing 框架。新增受众适配指南、评分量表(0-40)、反模式清单(8条)、ClawHub运营标签。*
