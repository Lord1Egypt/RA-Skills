# PowerMatrix GEO Growth Orchestrator

PowerMatrix GEO Growth Orchestrator 是一个企业 AI 内容增长工作流 Skill。它把品牌母库、GEO 可见度检测、内容缺口分析、GEO 内容生成和多平台草稿助手串联起来，让企业从“一堆资料”走到“一批可人工审核发布的内容草稿、客户成果报告和内部审计报告”。

它不是某一个平台的写作助手，而是总控层：负责判断先做什么、调用什么能力、输出哪些中间结果、哪些内容需要人工确认。

## 适合什么场景

- 企业希望提升品牌在 AI 搜索、问答模型和内容平台中的可见度。
- 市场团队需要把官网、产品介绍、FAQ、案例整理成可复用内容资产。
- 内容运营需要一次性生成知乎、CSDN、掘金、今日头条等平台的草稿任务。
- AI / GEO 服务交付顾问需要一个标准交付流程，避免每次从零组织材料。
- PowerMatrix 内部团队需要把品牌母库、检测报告、内容包和复盘建议串成闭环。

## 用户如何开始

用户只需要提供四类信息：

1. 企业资料：公司介绍、产品服务、官网、FAQ、案例、联系方式、禁用说法。
2. 目标关键词：希望被 AI 和平台内容覆盖的搜索词。
3. 目标平台：例如知乎、CSDN、掘金、今日头条。
4. 任务目标：例如品牌可见度提升、AI 搜索覆盖、获客内容生成。

如果已经有品牌母库或 GEO 检测报告，可以直接提供，工作流会优先复用。

## 第一次使用需要准备什么资料

建议至少准备：

- 品牌名称、公司简介、产品和服务说明。
- 目标客户、典型场景、客户痛点。
- 核心卖点和证据来源。
- 常见问题和标准回答。
- 官网、产品页、案例页、联系方式。
- 品牌语气、禁用词、禁用承诺、合规边界。

资料不完整也可以开始，但缺失信息会被标记为 `待确认`，不会由系统编造。

## 一次完整工作流会输出什么

这个 Skill 有两类输出：

1. 客户成果报告：用于商务交付、客户沟通、复盘会议。
2. 内部审计报告：用于交付团队检查事实、合规、风险和证据等级。

对客户展示时，优先使用：

- `client_delivery_report.md`：客户可见成果报告。
- `content_asset_summary.md`：客户可读的内容资产摘要。
- `publish_plan_client.md`：客户版发布计划。

内部复盘时，使用：

- `internal_audit_report.md`：内部审计报告。
- `brand_profile.json`：标准品牌资料。
- `geo_audit_report.json`：关键词和模型维度的可见度检测结果。
- `content_gap_report.json`：内容缺口和优先补齐项。
- `content_tasks.json`：可执行的内容任务清单。
- `platform_drafts.json`：知乎、CSDN、掘金、今日头条等平台草稿。
- `publish_plan.json`：内部发布计划。

建议输出目录：

```text
geo_orchestrator_v2/
├── final_report.md
├── summary.md
├── client_delivery_report.md
├── internal_audit_report.md
├── content_asset_summary.md
├── publish_plan_client.md
├── raw_answers/
│   └── {model}/{probe_id}.md
├── model_scores/
│   └── {model}.json
├── dual_model_comparison.json
├── content_recommendations.json
├── geo_action_priorities.json
├── brand_profile.json
├── geo_audit_report.json
├── content_gap_report.json
├── content_tasks.json
├── platform_drafts.json
└── publish_plan.json
```

## OpenClaw 中的默认输出模式

默认 `output_mode` 是 `full_report`。除非用户明确要求“只要摘要”，否则 OpenClaw 执行完成后必须在聊天窗口输出完整 `final_report.md` 正文。

禁止只回复：

- “报告已生成，请查看目录”
- “已保存到本地文件”
- 只有 3 到 5 行执行摘要

如果使用脚本生成客户交付级双模型评估报告，推荐运行：

```bash
python3 scripts/generate_full_report.py examples/spanish_olive_oil_input.json --output-dir geo_orchestrator_v2
```

这个脚本会同时：

- 保存 `final_report.md`
- 保存 `summary.md`
- 保存每个模型每个探针的原始回答
- 保存每个模型评分 JSON
- 保存双模型对比 JSON
- 保存内容生产建议 JSON
- 保存 GEO 行动优先级 JSON
- 默认把完整 `final_report.md` 打印到当前对话输出

## 和单个平台 Draft Assistant 的区别

单个平台 Draft Assistant 负责把已有素材改写成某个平台的草稿。例如知乎助手偏问答和观点，CSDN 助手偏技术教程，掘金助手偏开发者实践，今日头条助手偏通俗商业场景。

本 Orchestrator 负责更上游的编排：

- 判断是否已有品牌母库。
- 规划 DeepSeek、豆包、通用环境的 GEO 检测。
- 从检测结果中找内容缺口。
- 把内容缺口拆成不同平台的内容任务。
- 汇总草稿、发布计划和复盘建议。

## 如何识别相邻 Skill

当前 `Skills/` 目录下的各个 Skill 是平行文件夹，不是本 Skill 的子目录。Orchestrator 通过 `registry/geo_skill_registry.json` 识别相邻能力，所有路径都使用相对于本目录的 `../` 形式，例如：

- `../AI-geo-content-generator`
- `../geo-analysis-doubao`
- `../deepseek-geo-audit-skill`
- `../zhihu-geo-draft-assistant`
- `../toutiao-geo-draft-assistant`
- `../csdn-geo-draft-publisher`
- `../juejin-geo-draft-publisher`
- `../GEO tool-deepseek`

Registry 每个条目都会说明：

- 这个 Skill 负责什么；
- 什么时候应该调用；
- 需要哪些输入；
- 应该产出哪些文件；
- 什么时候跳过；
- 调用失败时如何补救。

注意：Orchestrator 不移动、不复制、不内嵌这些相邻 Skill。当前环境如果不能直接调用相邻 Skill，则输出“编排指令 + 预期交付物合同”，并在最终报告中标记执行状态。

## 标准编排流程

标准流程定义在 `workflow/geo_orchestration_workflow.md`：

1. Stage 0：Intake / 任务识别。
2. Stage 1：Brand Knowledge Base 构建或检查。
3. Stage 2：DeepSeek + Doubao GEO 初始评估。
4. Stage 3：GEO Gap Matrix 生成。
5. Stage 4：Content Task Plan 生成。
6. Stage 5：调用 AI-geo-content-generator 生成通用内容资产。
7. Stage 6：根据行业和平台路由调用知乎、头条、CSDN、掘金等平台草稿 Skill。
8. Stage 7：汇总所有输出为客户交付包。
9. Stage 8：生成 7 / 14 / 30 天复测计划。

平台路由规则见 `workflow/platform_routing_rules.md`，输出验收规则见 `workflow/output_validation_rules.md`。

## 如何运行一次完整 GEO 编排

在 OpenClaw 或 Codex 中，可以用自然语言要求：

```text
请基于 examples/spanish_olive_oil_orchestration.md 的输入，按 GEO Orchestrator 完整流程生成客户交付包。默认 output_mode=full_report，并在当前对话输出完整报告正文。
```

也可以针对西班牙火腿：

```text
请基于 examples/spanish_ham_orchestration.md 的输入，按 GEO Orchestrator 完整流程生成客户交付包。请列出相邻 Skill 调用顺序、阶段状态、GEO Gap Matrix、Content Task Plan、Platform Distribution Plan 和 30 天复测计划。
```

如果使用已有脚本生成双模型正式报告，仍可运行：

```bash
python3 scripts/generate_full_report.py examples/spanish_olive_oil_input.json --output-dir geo_orchestrator_v2
```

如果当前环境不能直接调用相邻 Skill，Orchestrator 应输出每个相邻 Skill 的“建议调用指令”和 `expected_outputs`，等待用户或交付人员执行后再汇总。

## 为什么需要人工确认

GEO 内容会涉及企业事实、客户案例、效果描述、平台规则和行业合规。系统可以生成草稿和建议，但不能替用户确认事实、承诺效果或点击发布。

默认规则：

- 所有平台草稿都必须人工审核。
- 不自动点击发布按钮。
- 未执行真实 GEO 检测时，只能输出检测计划或推理预估，不能写成确定排名、分数或已覆盖结论。
- 门票/价格、营业时间、安全资质、竞品数据、案例、第三方背书等关键事实缺失时，发布计划必须标记为 `blocked` 或 `needs_review`。
- 不承诺排名第一、100% 收录或一定被大模型引用。
- 不伪造客户案例、第三方背书或业务数据。
- 遇到医疗、金融、法律等敏感行业，必须由专业人士复核。

## 客户报告和内部报告怎么分工

客户报告强调“本轮交付成果”和“下一步增长动作”。它会展示已梳理的品牌信息、发现的内容机会、生成的知乎/头条/CSDN/掘金草稿、推荐发布顺序和客户需要补充的资料。客户报告不会暴露 API 配置、schema 校验、版本变更、内部字段名或调试信息。

内部审计报告保留完整质量控制信息，包括证据等级、事实依赖、发布前置条件、风险清单、禁用表达检查、API 状态、schema 校验和结构化 JSON 文件路径。它用于交付团队复盘，不建议直接发送给客户。

## 示例输入

```json
{
  "brand_materials": "PowerMatrix 为企业提供 AI Agent 工作系统，包含品牌母库、GEO 内容生成、DeepSeek / 豆包可见度检测、AI 客服、OpenClaw 数字员工和企业 AI 咨询。",
  "target_keywords": ["企业 AI Agent 落地方案", "AI 客服系统", "企业 GEO 优化"],
  "target_platforms": ["zhihu", "csdn", "juejin", "toutiao"],
  "target_models": ["deepseek", "doubao", "generic"],
  "campaign_goal": "提升 PowerMatrix 在 AI 搜索和内容平台中的可见度，生成可人工审核发布的 GEO 内容草稿。",
  "tone": "专业、克制、企业服务导向",
  "compliance_constraints": ["不承诺排名第一", "不伪造客户案例", "不承诺 100% 被模型收录"]
}
```

完整示例见 `examples/sample_input.json`。

## 示例输出

一次交付会形成：

- 完整双模型评估报告：`final_report.md`
- 简短摘要：`summary.md`
- 客户成果报告：`client_delivery_report.md`
- 内容资产摘要：`content_asset_summary.md`
- 客户版发布计划：`publish_plan_client.md`
- 内部审计报告：`internal_audit_report.md`
- 品牌母库：`brand_profile.json`
- GEO 检测结果：`geo_audit_report.json`
- 内容任务：`content_tasks.json`
- 平台草稿：`platform_drafts.json`
- 内部发布计划：`publish_plan.json`

客户报告示例见 `examples/sample_client_delivery_report.md`。内部报告示例可参考 `examples/sample_final_report.md`。

双模型评估示例输入：

- `examples/spanish_olive_oil_input.json`
- `examples/spanish_ham_input.json`

## 如何验证不是摘要型输出

运行 smoke test：

```bash
python3 scripts/smoke_test_full_report.py
```

运行 Orchestrator 合同校验：

```bash
python3 scripts/validate_orchestrator_contracts.py
```

通过标准：

- `final_report.md` 包含执行摘要、评估方法、探针问题列表、双模型总评分表、分场景检测结果、竞品格局、GEO 优化建议、30天内容行动清单、原始数据附录等必需章节。
- `final_report.md` 开头包含“老板能看懂的3句话结论”。
- `final_report.md` 包含知乎、小红书、抖音、官网 FAQ 和 GEO 文章选题建议。
- 所有建议包含影响程度、执行难度、见效速度和优先级分。
- 报告结尾包含复测时间、复测指标和 GEO 优化有效性的判断方式。
- 标准输出中也包含这些章节，说明 OpenClaw 聊天窗口能拿到完整报告。
- `summary.md` 只是辅助摘要，不替代 `final_report.md`。
- `model_scores/{model}.json` 包含提及率、排名位置、情感倾向、回答深度、事实准确性、购买决策辅助、本地化适配、商业转化价值。
- `registry/geo_skill_registry.json` 存在，且所有 `relative_path` 都以 `../` 开头。
- 缺失下游输出时，状态会被标记为 `partial` 或 `failed`，不会假装成功。
- 客户交付模板包含相邻 Skill 状态、GEO 盲区、内容资产、发布顺序、30 天复测计划和完整文件路径清单。

## 常见问题

### 没有品牌母库能不能用？

可以。工作流会先进入 Brand Profile Resolve 阶段，根据企业资料生成初版品牌母库。缺失字段会标记为 `待确认`。

### 已经有 GEO 报告还要重新检测吗？

不一定。已有报告可以复用。工作流会检查报告是否覆盖目标关键词、目标模型和目标问题，缺口部分再补测。

### 会自动发到知乎、CSDN、掘金、今日头条吗？

不会。输出以草稿、发布建议和复制用内容为主。平台发布前默认需要人工确认。

### 能保证 AI 搜索排名提升吗？

不能保证。工作流能提升内容结构化、可解释性和覆盖完整度，但不承诺排名第一、100% 收录或一定被模型引用。

### 适合敏感行业吗？

可以作为资料整理和草稿辅助，但医疗、金融、法律等行业必须由专业人士审核，且不能生成绝对化效果承诺。
