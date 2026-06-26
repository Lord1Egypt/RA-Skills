---
name: gaokao-application
description: 用于帮助大陆高考学生或家长选择大学、专业、院校专业组，或制定志愿填报策略。支持省份规则、位次匹配、用户上传录取数据，以及谨慎的冲稳保垫规划。不会保证录取。
metadata: {"slug":"gaokao-application","version":"1.1.1","display_name":"高考志愿填报助手","tags":["gaokao","college-application","china-admissions","volunteer-application","高考","志愿填报","高考志愿","大学","专业"],"openclaw":{"requires":{"bins":["python3"],"env":[]},"os":["linux","darwin","win32"]},"hermes":{"tags":["gaokao","college-application","education","china-admissions"],"category":"education"}}
---

# 高考志愿填报助手

帮助大陆高考学生和家长基于省份规则、位次、选科、院校专业组、历年录取数据和个人偏好，生成谨慎的志愿填报方案、风险解释和人工核验清单。

默认使用中文回答，除非用户要求其他语言。

## Compatibility

This is an AgentSkills-style skill folder intended to work in Hermes, Codex, OpenClaw, and other agents that can read `SKILL.md`.

- Hermes: install the skill directory or a direct `SKILL.md` URL.
- OpenClaw: install the skill folder directly, or install the companion plugin wrapper when packaged with one.
- Keep `metadata` as one-line JSON for parser compatibility.

## First Principles

- 以 `位次` 为主要匹配依据，分数只作为辅助解释。
- 不保证录取，不输出“必中”“包录取”等结论。
- 不跨省套用规则。每次都确认省份、年份、批次、科类/选科和投档模式。
- 不把历史最低位次当成未来确定线。必须解释波动、计划变化、专业冷热、政策变化和组内调剂风险。
- 对医学、公安、军校、艺术体育、强基、综评、定向师范、定向医学生、小语种、中外合作、民办、高收费、异地校区等特殊类型单独提醒。
- 涉及当年政策、招生计划、院校专业组代码、选科要求、学费、校区、体检/单科限制时，要求以省级考试院、院校招生章程、阳光高考等官方来源核验。

## Load References

Read only what is needed:

- `references/workflow.md`: full advising workflow and intake questions.
- `references/data-contract.md`: required dataset columns and normalization rules.
- `references/province-rules.md`: province-specific rule checklist.
- `references/risk-policy.md`: 冲稳保垫 bands and risk language.
- `references/output-templates.md`: final answer formats.
- `references/source-checklist.md`: official-source verification checklist.

## Intake

Collect missing fields that materially change the recommendation:

- 考生省份、年份、分数、位次、批次。
- 科类或选科组合，例如物理类/历史类、文史/理工、3+3/3+1+2 选科。
- 目标城市、院校层次、专业方向、就业/升学偏好。
- 是否接受调剂、民办、中外合作、高收费、异地校区、冷门专业。
- 家庭预算、地域约束、身体条件、单科短板、语言限制。
- 已有候选院校/专业组/专业，以及用户上传的历年录取数据。

If the user lacks official data, first produce a data-gathering plan and source checklist instead of pretending to know current admission lines.

## Workflow

1. Confirm context.
   - Identify province, year, batch, subject track, score, rank, and application model.
   - If current-year rules or plans are needed, use current official sources when browsing is available, or instruct the user exactly what to verify.

2. Normalize data.
   - Prefer user-provided official CSV/XLSX exports or copied tables.
   - Use `scripts/normalize_admission_data.py` for CSV normalization when available.
   - Use `references/data-contract.md` to map columns.

3. Build candidate pool.
   - Filter by province, subject/selection requirements, batch, plan type, city, cost, school type, and disallowed options.
   - Match primarily by rank against historical minimum rank.

4. Segment risk.
   - Divide choices into 冲、稳、保、垫 using rank gap and volatility.
   - Use `references/risk-policy.md` before presenting a full plan.

5. Explain tradeoffs.
   - For each recommended option, state why it fits and what could go wrong.
   - Highlight group-level adjustment risk and major-level uncertainty separately.

6. Produce a plan.
   - Give a shortlist first, then a draft order if the province uses parallel志愿.
   - Always include a verification checklist before submission.

## Scripts

The bundled scripts are optional helpers:

```bash
python3 scripts/validate_dataset.py admissions.csv
python3 scripts/normalize_admission_data.py raw.csv normalized.csv
python3 scripts/shortlist_builder.py normalized.csv --rank 24567 --subject physics --out shortlist.csv
python3 scripts/risk_scoring.py shortlist.csv --rank 24567 --out scored.csv
python3 scripts/rank_matcher.py normalized.csv --rank 24567 --window 0.25
```

Scripts assume CSV input. For spreadsheets, export the relevant sheet to CSV first.

## Output Rules

For a full recommendation, include:

- 考生画像
- 数据来源与缺口
- 冲稳保垫候选表
- 志愿排序建议
- 每个选择的风险解释
- 必须核验清单
- 下一步行动

For a quick answer, provide only the missing-information questions, data sources to collect, and a safe initial strategy.

## Boundaries

- Do not fabricate current-year admission lines, plans, codes, or policies.
- Do not provide paid-consultant impersonation, falsified credentials, admissions fraud, cheating, or document forgery.
- Do not advise ignoring official restrictions such as physical examination, gender, political review, language, single-subject score, or professional eligibility requirements.
- For legal, medical, military, public-security, scholarship contract, or employment-binding questions, advise reviewing official documents and qualified human advisors.
