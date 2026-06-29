---
name: demandspec
description: Use when analyzing, clarifying, specifying, reviewing, validating, approving, or archiving product and business requirements, including PRDs, AI scenarios, prototypes, acceptance criteria, requirement changes, and development handoffs.
---

# DemandSpec

将业务想法、会议纪要、口述需求、已有 PRD、系统截图或 AI 场景设想，转化为写入工作区、可评审、可追踪、可验证的需求资产。不要只在对话中给建议或输出空模板。

## Core Workflow

```text
Intake -> Clarify -> Diagnose -> Model -> Prototype -> Specify -> Validate -> Handoff -> Archive
```

## Execution Workflow

1. **检查现状。** First inspect the workspace：查找 `demandspec/`、`demands/`、`changes/`、现有 PRD、会议纪要、原型、接口文档、测试和业务规则。优先复用真实材料，不凭空补全。
2. **判断入口。** 确定需求成熟度 L0-L6、类型（普通、AI、UI、跨系统、高风险）以及是新需求、已有 PRD 修订还是变更包。
3. **分离信息。** 将内容分为：
   - 已确认事实：有来源支撑，可直接进入规格。
   - 当前假设：为推进工作暂时采用，必须标注验证方式。
   - 阻塞项：不确认就无法定义范围、规则或验收标准。
4. **创建或定位需求包。** CLI 可用时执行：

   ```bash
   demandspec init --project .
   demandspec new "<需求名称>" --type <normal|ai|ui|cross-system|high-risk> --owner "<负责人>"
   demandspec change new "<变更名称>" --domain <domain> --type <type> --owner "<负责人>"
   ```

   CLI 不可用时，按 Output Layout 手工创建同等目录和 Markdown 文件。
5. **只读取本次需要的模板。** 先看 [模板填写指南](references/template-filling-guide.md)，再读取 `templates/` 中对应模板。不要一次生成所有文档；输出应与成熟度和交付目标匹配。
6. **填入具体内容并落盘。** 使用真实角色、动作、字段、规则、阈值、异常、来源和责任人，write the files 到目标需求目录。禁止留下无解释的空标题、通用占位语或只复制模板。
7. **建立追踪关系。** 为需求分配稳定 ID，例如 `CRM-VISIT-001`。同一 ID 必须出现在 Delta Spec、PRD/设计、验收标准、测试用例和研发任务中。
8. **验证并修正。** 对变更包执行：

   ```bash
   demandspec change validate <change-id> --strict
   ```

   修复结构、必填内容和追踪错误后再次执行，直到通过。没有 CLI 时，至少按 `templates/review-checklist.md` 检查完整性、一致性、可实现性和可验收性。
9. **报告完成结果。** 列出写入文件、成熟度、关键结论、未决问题、验证命令和验证结果，不把“文档已生成”当成“需求已确认”。

## Quick Paths

| 用户输入 | 推荐路径 | 最小输出 |
|---|---|---|
| 只有一句话想法 | Intake -> Clarify -> Scope | 需求卡片、澄清问题、范围边界 |
| 已有 PRD 需要补全或评审 | Inspect -> Review -> Repair -> Validate | 修订后的 PRD、评审清单、验收标准 |
| AI 场景 | Intake -> Clarify -> AI Fit -> Model -> Validate | 需求卡片、AI 评估、数据/规则、人工兜底、AI 验收 |
| 页面或交互需求 | Scope -> Process -> Prototype -> Acceptance | 范围、流程、页面/状态/交互、验收标准 |
| OpenSpec 风格变更 | Proposal -> Delta Spec -> Acceptance -> Tasks -> Validate | `proposal.md`、Delta Spec、`acceptance.md`、`tasks.md` |

需求仍处于 L0-L2 时，不要直接伪造完整 PRD。先产出足以推动确认的材料，并明确下一步负责人。

## Output Layout

完整需求档案：

```text
demands/<demand-id>/
  00_intake/
  01_clarify/
  02_diagnose/
  03_model/
  04_prototype/
  05_spec/
  06_validate/
  07_handoff/
  08_archive/
```

OpenSpec 风格变更包：

```text
changes/<change-id>/
  metadata.yaml
  proposal.md
  design.md
  specs/<domain>/spec.md
  acceptance.md
  tasks.md
  approval.md
```

如果仓库已有其他约定，匹配现有路径，不为统一目录而移动用户文件。

## Maturity Levels

| Level | 可观察状态 | 下一步 |
|---|---|---|
| L0 原始想法 | 只有一句话或零散材料 | 形成需求卡片 |
| L1 问题描述 | 有痛点，目标和用户不清 | 澄清问题与成功指标 |
| L2 需求雏形 | 有目标和场景，边界不完整 | 范围、流程、假设 |
| L3 可建模需求 | 角色、流程、数据基本明确 | 原型、规则、AI 评估 |
| L4 可成文需求 | 可生成 PRD 和原型说明 | 验收与评审 |
| L5 可交付需求 | 需求、验收、任务可追踪 | 审批、实施、验证 |
| L6 可沉淀需求 | 已上线并有反馈或指标 | 归档与复盘 |

## Template Usage

模板是检查清单，不是成品。按 [references/template-filling-guide.md](references/template-filling-guide.md) 的最低完成条件填写。核心规则：

- 事实写明来源；未知项写“待确认：问题 / 负责人 / 截止时间”。
- 范围必须同时写 In Scope、Out of Scope 和边界条件。
- 功能要求使用“系统 MUST/SHALL + 可观察行为”，避免“支持、优化、智能化”等无验收口径的词。
- 验收标准使用 GIVEN / WHEN / THEN，并覆盖正常、异常、权限、数据和非功能场景。
- AI 场景必须定义输入、输出、效果指标、业务指标、低置信度处理、人工确认和失败回退。
- UI 场景必须定义页面、组件、交互、空态、加载态、成功态、失败态和权限态。

## Worked Example

需要了解如何执行或内容应写到什么粒度时，读取 [拜访单自动生成完整案例](references/visit-form-auto-generation-example.md)。案例展示：

- 从一句话输入判断为 AI/full 需求；
- 将事实、假设和阻塞项分离；
- 使用 `CRM-VISIT-001` 串联规格、验收和研发任务；
- 定义低置信度字段的人工确认与提交阻断；
- 执行严格验证并报告结果。

## Common Mistakes

- **只复制模板。** 有标题没有决策、数据或验收口径，不算完成。
- **跳过澄清直接写 PRD。** 未确认内容会被伪装成事实。
- **只写理想流程。** 漏掉空数据、重复提交、接口失败、权限不足和人工回退。
- **AI 只写模型方案。** 没有业务收益、基线、阈值、人工确认和错误成本。
- **原型只列页面名。** 没有组件、状态、交互和跳转，无法交付设计或前端。
- **验收与任务不带需求 ID。** 无法证明需求已被测试和实现。
- **验证失败仍宣布完成。** 应列出失败项并继续修复，或明确阻塞原因。
- **只回复对话不写文件。** 除非用户明确只要建议，否则必须将资产写入工作区。

## Completion Report

最终回复使用以下结构：

```markdown
完成：
- 成熟度：Lx -> Ly
- 需求类型：...
- 新增/修改文件：...
- 关键决策：...
- 待确认项：...
- 验证：`demandspec change validate ... --strict` -> 通过/失败
```

不得把假设、模板生成或未通过验证的内容描述为已获业务确认。

