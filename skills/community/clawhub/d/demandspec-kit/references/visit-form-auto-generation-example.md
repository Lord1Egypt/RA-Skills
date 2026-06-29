# 完整案例：AI 自动生成拜访单草稿

本案例演示如何把一句话需求转为可评审的 full 变更包。示例内容可直接作为执行粒度参考，但不能在其他项目中照抄业务结论。

## 1. 原始输入

> 希望 AI 根据拜访录音、图片和邮件自动生成 CRM 拜访单，减少一线填写时间。

## 2. 路由判断

- 当前成熟度：L1，只有问题方向和粗略方案。
- 目标成熟度：L5，可进入研发评审。
- 类型：AI + UI + 跨系统，因此使用 full profile。
- 需要先确认：输入格式、目标字段、提交权限、质量阈值、数据合规和失败回退。

CLI 可用时：

```bash
demandspec init --project .
demandspec change new "拜访单自动生成" --domain crm --type ai --owner "算法团队"
```

## 3. 事实、假设与阻塞项

### 已确认事实

- 当前拜访单由销售人员手工填写。
- MVP 的 AI 输出只作为草稿。
- 正式提交前必须由当前拜访人员人工确认。

### 当前假设

- 首期输入包括录音、现场图片和邮件正文。
- CRM 能提供客户 ID、拜访人 ID 和拜访单保存接口。
- 置信度阈值暂定 0.70，试点后按误判成本校准。

### 阻塞项

| 问题 | 影响 | 负责人 | 截止点 |
|---|---|---|---|
| 支持哪些录音格式与时长 | 上传校验、成本和处理时延 | 语音平台负责人 | 技术评审前 |
| 哪些字段允许 AI 生成 | PRD、字段权限和验收范围 | CRM 产品负责人 | 需求评审前 |
| 原始录音保存多久 | 合规、存储与删除策略 | 数据合规负责人 | 方案评审前 |

## 4. Proposal 摘要

```markdown
# Change Proposal

## Problem
一线人员需要手工整理拜访录音、图片和邮件，再重复填写拜访单，
耗时且容易遗漏关键信息。

## Intent
使用 AI 生成可追溯、可人工修订的拜访单草稿，降低填写成本并提高记录完整性。

## Scope
支持材料上传、内容提取、字段草稿、置信度提示、人工确认和修改结果回流。

## Non-Goals
不自动提交拜访单，不替代人工确认，不修改客户主数据。
```

## 5. Delta Spec

文件：`changes/<change-id>/specs/crm/spec.md`

```markdown
## ADDED Requirements

### Requirement: CRM-VISIT-001 Generate a reviewable visit form draft
The system MUST generate a visit form draft from supported visit materials and
require human confirmation before submission.

#### Scenario: Draft generated from visit materials
- GIVEN a sales user has selected a customer and uploaded supported materials
- WHEN the user requests a visit form draft
- THEN the system displays extracted fields with source and confidence information
- AND the system prevents submission until the user confirms the draft

#### Scenario: Low-confidence field requires review
- GIVEN a generated field is below the configured confidence threshold
- WHEN the draft is displayed
- THEN the system marks the field for mandatory human review
```

`CRM-VISIT-001` 是稳定追踪 ID；要求使用 MUST，场景使用 GIVEN / WHEN / THEN，并定义了用户可观察结果。

## 6. AI 适配与回退

- 适配结论：中高，适合“语音转写/OCR + LLM 信息抽取 + 规则校验”，不适合无人审核直接提交。
- 输入：录音转写、图片 OCR、邮件正文、客户基础信息、拜访单填写规则。
- 输出：拜访主题、时间、对象、摘要、客户诉求、商机线索、下一步行动、字段来源和置信度。
- 模型指标：试点标注集上关键字段 micro-F1 目标不低于 0.85。
- 业务指标：单次填写中位时长相对基线降低至少 40%，草稿采纳率不低于 70%。
- 风险指标：未经人工确认的提交数必须为 0。
- 低置信度处理：置信度低于 0.70 的字段突出显示，必须人工确认或修改。
- 失败回退：转写、OCR 或生成失败时保留用户材料，允许重试；连续失败后切换为手工填写，不阻断正常业务。
- 数据飞轮：记录人工修改前后值、退回原因和最终提交结果，用于阈值校准、Prompt 优化和评估集更新。

## 7. 页面与状态

拜访单编辑页新增：

- 材料上传区：显示格式、大小、时长限制。
- “生成草稿”按钮：只有选择客户且至少有一份有效材料时可用。
- 处理状态：上传中、转写中、抽取中、生成成功、部分失败、全部失败。
- 字段卡片：显示生成值、来源片段、置信度、人工修改和确认状态。
- 提交控制：存在未确认的必填字段或低置信度字段时禁用。
- 回退入口：重试生成或切换为手工填写。

## 8. 验收标准

```markdown
### CRM-VISIT-001 Draft generated from visit materials
- GIVEN a sales user uploads a supported recording, image, or email text
- WHEN the user requests a visit form draft
- THEN the system displays extracted fields, their sources, and confidence values
- AND submission remains disabled until confirmation

### CRM-VISIT-001 Low-confidence field requires review
- GIVEN a generated field is below the configured confidence threshold
- WHEN the draft is displayed
- THEN the field is visibly marked and requires 人工确认

### CRM-VISIT-001 Generation failure falls back safely
- GIVEN material processing fails after the configured retries
- WHEN the failure result is returned
- THEN the system retains the uploaded materials
- AND offers manual entry without creating a formal visit record
```

## 9. 研发任务

```markdown
- [ ] FE / CRM-VISIT-001 实现材料上传、处理状态、来源与置信度展示。
- [ ] FE / CRM-VISIT-001 实现人工修改、确认和提交禁用逻辑。
- [ ] BE / CRM-VISIT-001 提供异步生成任务、状态查询和结果保存接口。
- [ ] ALG / CRM-VISIT-001 实现转写/OCR 后的信息抽取、置信度和来源定位。
- [ ] DATA / CRM-VISIT-001 定义修改回流表、脱敏、留存和删除策略。
- [ ] QA / CRM-VISIT-001 覆盖正常、低置信度、超时、重复请求、权限和手工回退。
```

每项任务都引用 `CRM-VISIT-001`，因此可以从要求追踪到实现和测试。

## 10. 验证与完成报告

```bash
demandspec change set-status <change-id> clarifying
demandspec change set-status <change-id> review
demandspec change approve <change-id> --approver "需求委员会"
demandspec change validate <change-id> --strict
```

验证通过后的报告：

```markdown
完成：
- 成熟度：L1 -> L5
- 需求类型：AI / UI / 跨系统，full profile
- 写入文件：proposal、CRM Delta Spec、AI 评估、原型规格、验收、任务
- 关键决策：AI 仅生成草稿；低置信度字段必须人工确认；失败可回退手工填写
- 待确认项：录音限制、字段白名单、数据留存期限
- 验证：`demandspec change validate <change-id> --strict` -> 通过
```

如果验证未通过，应逐项修复后重跑；如果业务阻塞项未确认，应报告为“结构验证通过、业务确认未完成”，不能宣称需求已批准。

