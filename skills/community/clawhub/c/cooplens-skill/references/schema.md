# CoopLens Report Schema

## Universal fields

```json
{
  "fixed_disclaimer": "重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。",
  "runtime_date_line": "检索执行日期：YYYY年MM月DD日（时区：...；通过工具获取）",
  "markdown_toc_required": true,
  "static_html_required": true,
  "document_export_required_by_default": false,
  "public_discussion_visible_boundary": "no platform names, no source groupings, no user identity, no raw comments",
  "latest_source_bundle_required": true,
  "current_year_admission_status_gate_required": true,
  "current_year_rank_reasoning_required_when_estimate_present": true,
  "personalized_family_fit_required": true,
  "cscse_authentication_required_when_foreign_degree_or_overseas_path_exists": true,
  "rank_estimation_standalone_chapter_required_when_rank_or_score_used": true,
  "admission_batch_separation_required_when_plan_score_or_rank_used": true,
  "recommendation_split_required": true,
  "manual_source_confirmation_required_for_numeric_rank_inputs": true,
  "overseas_city_living_cost_required_when_abroad_stage_exists": true,
  "task_based_artifact_filenames_required": true,
  "html_section_jump_links_required": true,
  "html_colored_mobile_cards_required": true
}
```

## Markdown report skeleton

```markdown
重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。
检索执行日期：YYYY年MM月DD日（时区：...；通过工具获取）

# {项目/对比/候选报告标题}

## 目录
- [一、结论先行](#一结论先行)
- [二、当年是否招生核验与最新官方材料核验/批次口径](#二当年是否招生核验与最新官方材料核验批次口径)
- [三、位次预估：统计、分析与预测](#三位次预估统计分析与预测)
- [四、项目身份、证书与费用](#四项目身份证书与费用)
- [五、留服认证路径与风险](#五留服认证路径与风险)
- [六、培养模式、课程与学习压力](#六培养模式课程与学习压力)
- [七、毕业成果与未来四条路径](#七毕业成果与未来四条路径)
- [八、专业与行业前景](#八专业与行业前景)
- [九、公开讨论中的担忧与核验办法](#九公开讨论中的担忧与核验办法)
- [十、家长应向学校确认的问题](#十家长应向学校确认的问题)
- [十一、参考来源与核验说明](#十一参考来源与核验说明)

## 一、结论先行

- 项目综合实力推荐度评价（项目综合实力角度）：
- 个性化推荐度评价（学生/家庭适配）：
- 两者冲突说明：

## 二、当年是否招生核验与最新官方材料核验/批次口径

## 三、位次预估：统计、分析与预测

## 四、项目身份、证书与费用

## 五、留服认证路径与风险

## 六、培养模式、课程与学习压力

## 七、毕业成果与未来四条路径

## 八、专业与行业前景

## 九、公开讨论中的担忧与核验办法

## 十、家长应向学校确认的问题

## 十一、参考来源与核验说明

重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。
```

## Function 1 schema

```json
{
  "analysis_type": "single_project",
  "must_include": [
    "non_neutral_conclusion",
    "project_strength_recommendation",
    "personalized_family_fit_recommendation",
    "personalized_family_fit",
    "rank_estimation_statistics_analysis_prediction_chapter",
    "current_year_rank_reasoning_path",
    "rank_conclusion_first",
    "latest_official_materials",
    "current_year_admission_status_gate",
    "admission_rank_reference",
    "admission_batch_and_major_group_separation",
    "identity_and_plan_status",
    "certificate_combination",
    "cscse_authentication_path_and_risk",
    "tuition_and_total_cost",
    "overseas_city_living_cost_if_abroad",
    "curriculum_plain_language",
    "learning_pressure",
    "campus_and_resource_boundary",
    "transfer_and_adjustment_rules",
    "graduate_outcomes_without_names",
    "future_four_paths",
    "major_industry_outlook",
    "public_concerns_and_consultation",
    "parent_questions",
    "source_boundaries"
  ]
}
```

## Function 2 schema

```json
{
  "analysis_type": "multi_project_comparison",
  "layout": "project_cards",
  "must_include": [
    "overall_grouping_or_order",
    "project_strength_vs_personalized_fit_per_project",
    "conditions_that_reverse_order",
    "per_project_latest_official_materials",
    "per_project_current_year_admission_status_gate",
    "per_project_admission_rank_reference",
    "per_project_batch_and_major_group_separation",
    "per_project_advantages_and_disadvantages",
    "per_project_possible_rank_prediction",
    "per_project_graduate_study_and_employment",
    "overseas_city_living_cost_if_abroad",
    "certificate_cscse_and_cost_comparison",
    "graduate_outcomes_comparison_without_names",
    "future_four_paths_comparison",
    "major_industry_outlook_comparison",
    "public_concern_comparison",
    "parent_questions_by_project"
  ],
  "wide_table_policy": "avoid wide tables; use cards or narrow one-field lines"
}
```

## Function 3 schema

```json
{
  "analysis_type": "candidate_retrieval_by_province_score_rank",
  "must_include": [
    "table_of_contents_before_analysis",
    "most_important_recommendations_first",
    "search_assumptions",
    "rank_estimation_statistics_analysis_prediction_chapter",
    "current_year_plan_check",
    "current_year_admission_status_gate",
    "latest_completed_score_rank_basis",
    "candidate_cards_with_advantages_disadvantages_rank_cost_outcomes",
    "cscse_authentication_screening",
    "new_project_three_scenario_estimation",
    "current_year_rank_reasoning_path",
    "personalized_family_fit",
    "weak_evidence_watchlist",
    "non_neutral_recommendation_grouping",
    "source_boundaries"
  ],
  "candidate_card_required_fields": ["当年是否招生", "核心优势", "主要缺点或风险", "预测可能位次", "升学就业", "费用与预算", "证书与留服", "公开担忧与学校咨询"]
}
```



## Function 4 schema

```json
{
  "analysis_type": "standalone_rank_estimation",
  "must_include": [
    "rank_conclusion_first",
    "rank_estimation_important_disclaimer",
    "latest_current_year_admissions_search",
    "current_year_admission_status_gate",
    "verifiable_data_statistics",
    "manual_source_confirmation_checklist",
    "statistical_scope_and_anomaly_check",
    "rank_gap_and_line_gap_analysis",
    "current_year_rank_reasoning_path",
    "three_scenarios_for_new_or_no_history_projects",
    "confidence_level",
    "reversal_conditions",
    "project_strength_recommendation",
    "personalized_family_fit_recommendation",
    "source_boundaries",
    "overseas_city_living_cost_if_abroad"
  ]
}
```

## Recommendation split schema

```json
{
  "recommendation_split": {
    "project_strength_recommendation": "强 | 较强 | 中等 | 偏弱 | 高风险",
    "personalized_family_fit_recommendation": "高度适合 | 适合 | 边界适合 | 不太适合 | 不适合",
    "project_strength_basis": ["监管身份", "中外方实力", "专业与课程", "证书与留服", "费用回报", "毕业成果", "风险"],
    "personalized_fit_basis": ["学生分数/位次", "家庭预算", "出国偏好", "未来路径", "英语/GPA承受度", "城市/校区偏好"],
    "conflict_explanation_required": true
  }
}
```


## Current-year admission status gate schema

```json
{
  "current_year_admission_status_gate": {
    "required_before_recommendation_rank_or_candidate_sorting": true,
    "module_title": "当年是否招生核验（入场闸门）",
    "minimum_fields_per_project": ["项目/机构", "专业或大类", "当前年份", "省份", "科类/选科", "招生批次", "院校专业组", "计划类型", "当年招生状态", "学校官网或招生办来源", "教育部/CRS项目身份来源", "省级专业目录或招生计划来源", "对本报告的影响", "人工确认", "质量等级"],
    "status_labels": ["继续招生/当年招生", "未在当年招生计划中", "当年停招/暂停招生", "未核到当年招生，待学校书面确认"],
    "source_priority": ["目标省当年招生计划/专业目录", "学校本科招生网/招生办官网", "当年招生章程/招生简章", "教育部中外合作办学监管工作信息平台/CRS或教育部官网"],
    "crs_boundary": "CRS/教育部监管记录证明项目身份或审批状态，不单独证明当前年份仍招生",
    "gate_fail_effect": "no_current_year_rank_estimate_no_hard_ranking_move_to_仅关注待核验_or_暂不建议填报",
    "conflict_handling": "list_conflicting_sources_and_require_school_written_confirmation_before_formula_or_ranking"
  }
}
```

## Admission batch separation schema

```json
{
  "admission_batch_separation": {
    "required_when_plan_score_or_rank_present": true,
    "minimum_fields_per_record": ["年份", "省份", "科类/选科", "招生批次", "院校专业组", "计划类型", "项目/机构", "专业或大类", "招生计划人数", "最低分", "最低位次", "同批次控制线", "来源链接", "人工确认", "质量等级"],
    "same_project_multiple_batches": "split_into_separate_records_and_separate_conclusions",
    "forbidden": ["merge_plan_counts_across_batches", "average_score_lines_across_batches", "use_one_batch_control_line_for_another_batch", "use_batch_unknown_number_in_formula_or_hard_ranking"],
    "unknown_batch_handling": "mark_批次未核到_or_专业组未核到_and_downgrade_to_weak_evidence"
  }
}
```


## Rank estimation workflow schema

```json
{
  "rank_estimation_workflow": {
    "chapter_title": "位次预估：统计、分析与预测",
    "must_include": ["位次预估结论先行", "位次预估重要声明", "固定重要声明", "可验证数据统计", "招生批次与专业组拆分", "统计口径与异常值排查", "位差与线差分析", "本年位次估计的完整可核验推导", "人工确认清单"],
    "method_order": ["先结论", "先统计", "再分析", "再预测"],
    "numeric_inputs_directly_linked": true,
    "manual_confirmation_required": true,
    "data_quality_grade_required": true
  }
}
```

## Current-year rank reasoning schema

```json
{
  "current_year_rank_reasoning": {
    "required_when_rank_estimate_present": true,
    "visible_method_not_private_chain_of_thought": true,
    "must_include": ["输入数据", "招生批次", "院校专业组", "基线选择", "差值样本", "调整项", "计算过程", "置信度", "推翻条件"],
    "numeric_values_directly_linked": true,
    "final_output": "range_with_confidence_and_reversal_conditions",
    "manual_source_confirmation_checklist": true,
    "data_quality_grade_required": true
  }
}
```

## Personalized family-fit schema

```json
{
  "personalized_family_fit": {
    "budget_pressure": "宽裕 | 中等 | 紧张 | 未提供按情景；若涉及出国，加入境外城市生活成本和年度预算差额",
    "overseas_preference": "明确出国 | 可接受 | 不愿出国 | 未提供按情景",
    "future_path": "保研考研 | 海外硕士 | 就业 | 考公考编 | 国企事业单位 | 外企科技企业 | 未提供按情景",
    "english_gpa_tolerance": "高 | 中 | 低 | 未提供按情景",
    "city_campus_preference": "string | 未提供按情景",
    "decision_effect": "how these factors change 优先/备选/观察/慎选",
    "rank_safety_margin_required_when_rank_given": true,
    "budget_gap_required_when_budget_given": true
  }
}
```

## Static HTML schema

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="format-detection" content="telephone=no">
  <meta name="color-scheme" content="light">
  <title>{任务型报告标题}</title>
  <style>
    * { box-sizing: border-box; }
    html { -webkit-text-size-adjust: 100%; }
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.75; background: linear-gradient(180deg,#eef2ff,#f8fafc 220px); }
    main { max-width: 920px; margin: 0 auto; padding: 16px; }
    section, article, nav { overflow-wrap: anywhere; word-break: break-word; }
    a { min-height: 44px; text-underline-offset: 3px; }
    .hero { background: linear-gradient(135deg,#1d4ed8,#7c3aed); color: #fff; border-radius: 22px; padding: 18px 16px; }
    .card { border: 1px solid #e5e7eb; border-radius: 18px; padding: 16px; margin: 14px 0; background: #fff; box-shadow: 0 10px 28px rgba(15,23,42,.08); }
    .card-rank { background: linear-gradient(180deg,#fff7ed,#ffffff); border-color: #fed7aa; }
    .card-auth { background: linear-gradient(180deg,#ecfdf5,#ffffff); border-color: #bbf7d0; }
    .notice { background: #fff7ed; border-left: 5px solid #f97316; border-radius: 14px; padding: 12px; }
    .toc a { display: block; min-height: 44px; padding: 10px 12px; border-radius: 12px; background: #eef2ff; margin: 8px 0; }
    @media (min-width: 760px) { main { padding: 28px; } }
  </style>
</head>
<body>
  <main>
    <nav class="card toc" aria-label="目录">...</nav>
    <section class="card">...</section>
  </main>
</body>
</html>
```

Structural rendering requirements:

- Every `section` and `nav` tag must be explicitly closed.
- TOC links like `[一、结论先行](#一结论先行)` must become `<a href="#一结论先行">一、结论先行</a>` and must jump to the matching section on phone screens.
- No raw Markdown link syntax may remain in the final HTML.
- Long project names, source links and tables must wrap or scroll horizontally on phone screens.
- The fixed important statement must be visible near the top and inside `附录：重要声明与人工确认提醒`; if rank estimation exists, `位次预估重要声明` must also be visible and must be followed by the fixed important statement.

## Static HTML forbidden items

- No JavaScript.
- No external stylesheet.
- No component library or framework dependency.
- No CDN.
- No images or background images.
- No iframe, canvas or hidden request.
- No extra visible facts absent from Markdown.
- Markdown table-of-contents and source links must render as clickable anchors; raw Markdown link syntax must not remain visible.
- Final HTML ids and internal hrefs must be ASCII-only `sec-...` values generated by the renderer, never raw Chinese heading text.
- External href values must be WebView-safe ASCII http(s) URLs with accidental Chinese/full-width trailing punctuation removed.
- HTML document structure must be complete and structural containers must be closed.
- Every internal anchor in the table of contents must have a matching element id in the HTML.
- Repeated headings must receive unique ids; duplicate ids are a validation failure.
- The file must include the current safe-renderer meta marker, a visible hero title, a task-derived title, and no visible internal version wording.
- The browser `<title>` and hero `<h1>` must not be `## 目录`, `目录`, `正文`, `重要声明`, `CoopLens Report`, or raw Markdown heading syntax. If this appears, treat it as HTML 解析失败 and rebuild from Markdown with a task title.
- Use `safe-html-build` as the default generation command. Then run `html-syntax-check`, `html-report-check`, and `html-render-gate-check`. If any gate fails, the assistant must show the HTML 渲染失败原因, correct Markdown/TOC/anchors/title/links, and 不通过就重新生成 until all gates pass; failed HTML must be withheld.



## Critical data source gate schema

```json
{
  "critical_data_source_gate": {
    "critical_fields": ["招生人数", "招生计划人数", "计划数", "分数线", "投档线", "录取线", "最低分", "最低位次", "分位数", "排位", "位次", "升学率", "深造率", "出国率", "境外升学率", "就业率", "毕业去向落实率", "保研率", "推免率"],
    "visible_number_rule": "every critical numeric value must start with 约 and carry a source hyperlink, preferably on the value itself",
    "source_evidence_rule": "the source hyperlink must open and the page content must contain matching field/value evidence for the same year/province/subject/batch/group/project口径",
    "unknown_rule": "if search fails, the link cannot be opened, the value is not present, or the口径 cannot be verified, output 未知（未核到可打开且内容对应的来源链接）",
    "no_guessing": true,
    "required_local_gate": "python scripts/cooplens_core.py critical-data-source-check <report.md>",
    "required_link_evidence_gate_when_network_available": "python scripts/cooplens_core.py critical-source-evidence-check <report.md>"
  }
}
```

## Pure report file gate schema

```json
{
  "pure_report_file_gate": {
    "required_script_gate": "python scripts/cooplens_core.py pure-report-file-check <task-name>.html <task-name>.md",
    "html_must_be": ["literal .html filename suffix", "UTF-8 text", "not ZIP/archive magic bytes", "complete <!doctype html> document", "contains <html and </html>"],
    "markdown_must_be": ["literal .md filename suffix", "UTF-8 text", "not ZIP/archive magic bytes", "not HTML content"],
    "forbidden": [".zip", ".rar", ".7z", ".tar.gz", "a ZIP containing HTML", "an extensionless file inside a ZIP", "a folder link", "a packaged artifact whose display name says HTML"],
    "failure_rule": "content looking like HTML is not enough; if the delivered target is not a direct pure .html file and direct pure .md file, regenerate until this gate passes"
  }
}
```

## Final artifact delivery schema

```json
{
  "final_delivery": {
    "normal_success_requires": ["direct_pure_task_named_markdown_file_download_link", "direct_pure_task_named_html_file_download_link", "visible_delivery_download_block", "exactly_two_report_download_targets", "no_zip_or_archive_delivery_link"],
    "required_visible_block_title": "交付文件下载链接",
    "required_download_lines": ["静态网页（HTML）下载链接", "Markdown 文件下载链接"],
    "download_link_target_rule": "each link must point directly to one standalone .html file or one standalone .md file; zipped HTML/Markdown is failure",
    "forbidden_delivery_targets": [".zip", ".rar", ".7z", ".tar.gz", "archive package", "compressed bundle", "folder link", "打包下载", "压缩包", "打包文件", "合集", "ZIP 下载"],
    "archive_or_zip_link_as_substitute": "failure_and_regenerate_until_delivery_gate_passes",
    "required_file_gate": "python scripts/cooplens_core.py pure-report-file-check <task-name>.html <task-name>.md",
    "required_script_gate": "python scripts/cooplens_core.py strict-final-delivery-check <final-answer.md>",
    "mentioning_html_without_html_download_link": "failure",
    "mentioning_markdown_without_md_download_link": "failure",
    "function3_extra_gate": "python scripts/cooplens_core.py function3-delivery-gate-check <final-answer.md>",
    "html_failure_fallback_requires": "not_allowed_for_normal_delivery; keep_regenerating_until_html_passes",
    "silent_html_omission": "forbidden"
  }
}
```

## HTML render gate schema

```json
{
  "html_render_gate": {
    "applies_to_functions": [1, 2, 3, 4],
    "build_command": "python scripts/cooplens_core.py safe-html-build <report.md> --out <task-name>.html --error-out <task-name>_html_audit.json",
    "syntax_check_command": "python scripts/cooplens_core.py html-syntax-check <task-name>.html",
    "report_check_command": "python scripts/cooplens_core.py html-report-check <task-name>.html",
    "final_check_command": "python scripts/cooplens_core.py html-render-gate-check <report.md> <task-name>.html",
    "must_check": ["doctype", "single html/head/body/main shell", "HTML syntax parser stack", "head/body/main order", "safe-renderer marker", "visible hero title", "task-derived title", "closed structural tags", "clickable TOC anchors", "ASCII-only internal anchors", "WebView-safe external hrefs", "matching anchor targets", "no duplicate ids", "visible fixed important statement", "visible appendix important statement", "no custom important statement", "visible rank-estimation heading with fixed statement when rank appears", "no raw Markdown links", "no visible separator artifacts", "same visible facts as Markdown"],
    "on_failure": "explain the failure reason, correct Markdown, and regenerate until html-syntax-check/html-report-check/html-render-gate-check all pass",
    "fallback": "failed HTML is never delivered; if a single command reaches its safety cap, correct Markdown and run the gate again"
  }
}
```


## CSCSE / 留服认证 schema

```json
{
  "cscse_authentication": {
    "required_when_foreign_degree_or_overseas_path_exists": true,
    "must_include": ["认证对象", "认证路径", "项目模式", "境外学习记录", "计划内/计划外", "国内证书兜底", "认证结果预期", "传统海归/留学生待遇边界", "风险等级", "家长书面提问"],
    "official_source_targets": ["教育部留学服务中心", "CSCSE", "国家政务服务平台", "CRS", "招生章程", "学校书面答复"],
    "forbidden_claims": ["保证认证", "一定能认证", "包认证", "等同海归"],
    "decision_effect": "unclear authentication path downgrades to 观察/慎选/仅关注待核验"
  }
}
```

## Public discussion schema

```json
{
  "public_discussion": {
    "neutral_search_terms": ["string"],
    "positive_themes": ["string"],
    "negative_concerns": ["string"],
    "rebuttal_or_clarification": ["string"],
    "signal_strength": "反复出现 | 有一些讨论 | 样本很少 | 未形成有效信号",
    "officially_verifiable_answers": ["string with source"],
    "questions_for_school_written_confirmation": ["string"]
  }
}
```

## Graduate outcomes schema

```json
{
  "cscse_analysis": {
    "authentication_object": "foreign degree/diploma or none",
    "project_mode": "4+0/2+2/3+1/1+3/mixed/unknown",
    "overseas_study_record": "required/optional/absent/unknown",
    "plan_in_or_outside": "plan-in/plan-outside/unknown",
    "official_sources": [],
    "expected_result_boundary": "do not overpromise",
    "risk_level": "低/中/高/待核验",
    "school_written_questions": []
  },
  "graduate_outcomes": {
    "cohort_status": "已有毕业生 | 暂无毕业生 | 未核到公开信息",
    "evidence_scope": "项目级公开材料 | 学院/机构级公开材料 | 学校级公开材料，仅作背景 | 外方院校公开材料，仅作外方背景 | 暂无本项目毕业生公开成果",
    "selective_graduate_study": "string | 未核到可打开且内容对应的官方/权威原文",
    "known_employers_or_industries": "string | 未核到可打开且内容对应的官方/权威原文",
    "undergraduate_research_or_first_author_papers": "string | 未核到可打开且内容对应的官方/权威原文",
    "competitions_patents_awards": "string | 未核到可打开且内容对应的官方/权威原文",
    "privacy_rule": "do not reveal names or personal identifiers"
  }
}
```


## Overseas-city living-cost schema

```json
{
  "overseas_city_living_cost": {
    "required_when_abroad_stage_exists_or_user_wants_abroad": true,
    "must_include": ["外方大学所在城市", "住宿/租金", "餐饮", "交通", "保险/医疗", "签证/许可", "教材/学习材料", "汇率", "年度预算差额", "人工确认"],
    "source_targets": ["外方大学官方生活成本页面", "政府/移民或签证资金要求", "官方学生预算页面", "当前汇率来源"],
    "decision_effect": "cost confidence and budget gap must affect 个性化推荐度评价"
  }
}
```

## Completion gate

A completed Function 1/2/3/4/4 delivery has:

1. fixed disclaimer first;
2. runtime date line second;
3. direct parent-facing answer;
4. Markdown report with a visible `## 目录`;
5. mobile-first static HTML generated from the Markdown;
6. final answer includes `交付文件下载链接` with clickable download links for both the generated `.html` static webpage and `.md` Markdown file;
7. final answer draft passes `python scripts/cooplens_core.py strict-final-delivery-check final-answer.md`; no ZIP/archive/bundle/folder link may appear as a report delivery target;
8. important numeric values linked directly, prefixed with `约`, and passed through `critical-data-source-check`; if a critical link cannot be verified with `critical-source-evidence-check`, write unknown;
9. latest official admissions/charter/score-line source search reflected in the report;
10. public discussion handled without exposing platforms or identities;
11. negative concerns converted into official answers or school questions;
12. 留服认证路径与风险 checked when foreign degree or overseas path exists;
13. graduate outcomes checked without names;
14. final consolidated `参考来源与核验说明`;
15. latest QS official edition checked when QS ranking is mentioned;
16. separate project-strength and family-fit recommendation ratings;
17. final fixed disclaimer at the end of full reports;
17. task-based Markdown/HTML filenames;
18. overseas-city living cost checked when an abroad stage exists.
