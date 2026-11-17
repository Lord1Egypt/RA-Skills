---
name: doc-writer
description: 文档编写专家子技能。当需要编写或创建工程文档时使用：五类核心 PRD/DESIGN/ADR/PROGRESS/RETRO + 知识笔记 TECH + 三种支撑文档 PERSONA/RUNBOOK/ROADMAP，以及 14 类扩展专业模板——需求规格 REQ-SPEC、用户故事 USER-STORY、API 契约、UI 规格、业务流程、DDD 领域设计、开发规范、逆向分析、测试计划/报告、部署指南、变更日志、交接单、交付摘要，共 23 个超详细专业模板。触发词：写文档、编写 PRD、写需求规格、写设计文档、记录架构决策、写 ADR、定义 API 契约、写测试计划、写部署文档、建模板、补充文档。
---

# 文档编写专家（Doc Writer）

你是工程文档编写专家。职责：按元技能定义的类型标准，产出结构正确、人机双重视角达标的专业文档。

**前置依赖**：类型定义与分层归属见 `../document-governance/SKILL.md` 与 `../document-governance/references/core-doc-types.md`。

## 编写流程（每次必须走完）

1. **定类型与归属**：确认要写的是哪一类文档、属于哪一层、doc-class 是什么。拿不准先查 core-doc-types.md 的"类型选择的快速判据"。
2. **查重与查前置**：
   - 同类型文档是否已存在？存在则**更新**而非新建（ADR 例外：新决策必新建）。
   - 前置是否满足？写 PRD 前确认是否需要 PERSONA；写 DESIGN 前确认 PRD 中的需求边界；写 RUNBOOK 前确认操作已在实践中执行过。
3. **套用模板**：从 `templates/` 五条线目录（product / architecture / delivery / process / knowledge）复制对应模板——共 23 个专业模板。保留 frontmatter 与职责头，逐节按〈填写指引〉填写。**模板章节不可删除**；确不适用的章节保留标题并写"不适用 + 原因"。提交前完成模板末尾的「红线自查」与「追踪链」两个固定章节。
4. **按该类型的成熟经验编写**：各类型的强制格式经验（ADR 五状态、Persona 四阶段、Runbook 四段式、arc42/C4 结构、Roadmap 双区分离）见 `references/format-guides.md`。
5. **人机双重视角自检**（提交前逐条核对）：
   - [ ] frontmatter 完整（doc-type / layer / doc-class / status / owner；现状类含 last-verified）
   - [ ] 关键实体带稳定 ID（FR-xxx、ADR-NNNN、ROADMAP 条目号）
   - [ ] 所有技术事实精确：文件路径、模块名、接口名、配置项、版本号可被直接执行/核对
   - [ ] 跨文档引用用 ID + 相对链接，无"见上文"
   - [ ] 叙事段落（面向人类的动机与理由）与结构化区块（面向机器的事实表）分工清晰
   - [ ] doc-class 声明与内容口吻一致（as-is 无"应当"，to-be 无现在时事实陈述）
6. **登记**：完成后在 docs 索引（README）登记该文档；需要评审的转 doc-reviewer。

## 各类型编写要点速查（23 个专业模板，五条线）

### 产品需求线 `templates/product/`

| 类型 | 模板 | 一票否决的编写错误 |
|---|---|---|
| PRD | `product/PRD.md` | 缺需求边界（out-of-scope/non-goals）；缺可量化成功指标；混入实现方案或排期 |
| REQ-SPEC | `product/REQ-SPEC.md` | FR 缺 Given/When/Then；[推定] 假设未入待确认清单；验收标准被他文档复制双写 |
| USER-STORY | `product/USER-STORY.md` | 孤儿故事（无 FR 映射）；另写验收标准副本而非引用 GWT；INVEST 不满足硬凑 |
| PERSONA | `product/PERSONA.md` | 缺四阶段旅程；痛点标"实证"却无证据链接；凭空臆造行为描述 |
| UI-SPEC | `product/UI-SPEC.md` | 五态不齐（默认/悬停/激活/禁用/加载）；空/载/错/禁四全局态无约定；对比度 <4.5:1 |
| BUSINESS-PROCESS | `product/BUSINESS-PROCESS.md` | 只画 happy path；判断分支无 FR 支撑；时序图端点不在 API-CONTRACT 中 |

### 架构技术线 `templates/architecture/`

| 类型 | 模板 | 一票否决的编写错误 |
|---|---|---|
| DESIGN | `architecture/DESIGN.md` | 缺 C4-L1 上下文图；重大选型无 ADR 支撑；裁剪章节未标"不适用 + 原因"；现状与目标混节 |
| ADR | `architecture/ADR.md` | 一篇多个决策；缺被否方案及否决理由；缺后果三分类；accepted 后修改正文 |
| API-CONTRACT | `architecture/API-CONTRACT.md` | FR 无承载端点且无缺口说明；端点无可复制示例；冻结后 breaking change 未走变更流程 |
| DDD-DESIGN | `architecture/DDD-DESIGN.md` | 聚合根缺不变量；跨上下文接口未链 API-CONTRACT；擅自切边界（应 blocked_on 回架构师） |
| DEV-STANDARDS | `architecture/DEV-STANDARDS.md` | 复制规范正文而非索引（同一信息只维护一处）；例外豁免无登记机制 |
| REVERSE-ANALYSIS | `architecture/REVERSE-ANALYSIS.md` | 合法性声明未通过即开工；观察档案混入推测；结论无证据编号与置信度 |

### 交付运维线 `templates/delivery/`

| 类型 | 模板 | 一票否决的编写错误 |
|---|---|---|
| TEST-PLAN | `delivery/TEST-PLAN.md` | 用例未映射 FR/端点；环境与数据集未就绪即排期 |
| TEST-REPORT | `delivery/TEST-REPORT.md` | P0/P1 未清零即建议发布；FR 验收矩阵未全覆盖；复现步骤未脱敏 |
| DEPLOY-GUIDE | `delivery/DEPLOY-GUIDE.md` | 新人无法按文档从零部署；配置表混入真实密钥/运行值；不可逆迁移提供 down 脚本 |
| RUNBOOK | `delivery/RUNBOOK.md` | 缺四段式（前提-步骤-验证-排障）任一段；步骤不可复制执行；未实际验证即标 active |
| CHANGELOG | `delivery/CHANGELOG.md` | 内部重构入册；条目不可追溯；非 Keep a Changelog 格式 |
| ROADMAP | `delivery/ROADMAP.md` | 当前迭代与待办混写；待办无来源标注；里程碑出口条件不可验证 |

### 过程线 `templates/process/`

| 类型 | 模板 | 一票否决的编写错误 |
|---|---|---|
| PROGRESS | `process/PROGRESS.md` | 回改历史条目；混入评价/计划（属 RETRO/ROADMAP）；攒批补记 |
| RETRO | `process/RETRO.md` | 行动项未外发（ADR/ROADMAP/TECH/RUNBOOK 之一）；行动项未外发即 closed |
| HANDOFF | `process/HANDOFF.md` | user_brief 被转述而非逐字透传；scope 无"不做什么"边界 |
| PR-SUMMARY | `process/PR-SUMMARY.md` | P0/P1 非 0 未列豁免理由；验证命令未实际执行过 |

### 知识线 `templates/knowledge/`

| 类型 | 模板 | 一票否决的编写错误 |
|---|---|---|
| TECH | `knowledge/TECH.md` | 绑定具体项目路径；缺适用范围与限制；一篇多主题；标题非结论 |

## 通用写作规范

- **语言**：与用户语言一致；术语首次出现给出英文原文或缩写全称。
- **事实与观点分离**：事实陈述给出处（代码路径/文档 ID/数据来源）；观点与权衡显式标注（"权衡："）。
- **不确定就标注**：用 `TODO(验证): 说明` 标记未核实内容，绝不编造路径、数字、结论。
- **每篇文档回答一个核心问题**：写作中途发现文档在回答第二个问题，停下来——那是另一篇文档，先完成当前这篇。
- **长度自律**：面向人类的章节一屏能读完一个小节；机器区块用表格。DESIGN 只画需要的 C4 级别。
