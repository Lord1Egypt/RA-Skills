# 文件导航与依赖关系

## 1. 主入口
- `SKILL.md`：技能入口，定义触发条件、默认行为、渐进式披露路径。

## 2. 理解与原始资料
- `references/anduoduo_api_final.md`：原始 API 文档原样副本。
- `references/api_understanding_and_query_playbook.md`：整体数据模型、默认查数主干、候选路径理解，以及概览类固定模板报告的生成边界。

## 3. 已验证 SOP
- `sops/default_risk_query.md`：默认风险查数主干，也是概览类固定模板报告的优先入口。
- `sops/rule_drilldown.md`：按规则维度下钻风险。
- `sops/rules_catalog_lookup.md`：规则列表作为补充维表的定向查询方式。
- `sops/compliance_summary_and_report.md`：合规摘要与异步报告导出链路。

## 4. 约束与规则
- `references/best_practices.md`：推荐查询节奏、有效过滤键与固定模板使用原则。
- `references/pitfalls.md`：已知反例、误区与禁忌。
- `references/verification_status.md`：已验证路径、限制项与仅文档确认路径。
- `references/report_guidelines.md`：默认 HTML 报告规则与固定模板约束。
- `references/delivery_strategy.md`：文件交付策略。

## 5. 模板资源
- `assets/anduoduo_risk_report.html`：概览类风险查询必须使用的固定 HTML 彩页模板骨架。

## 6. 示例
- `examples/mock_risk_report_outline.md`：mock 报告结构示意，已统一使用“风险”展示口径。
- `examples/mock_records.json`：mock 明细数据示意，已统一使用“风险”展示口径。
