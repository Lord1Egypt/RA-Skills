---
name: gaokao-volunteer
description: >
  高考志愿填报AI助手。基于位次法和线差法，提供分数匹配、
  院校推荐、冲稳保方案生成、志愿梯度检查。覆盖全国31省新老高考模式。
  Triggers: 填志愿, 高考志愿, 能上什么大学, 志愿填报, 冲稳保,
  一分一段, 位次换算, gaokao, gaokao volunteer, 志愿推荐,
  查分数线, 院校推荐, 专业推荐, 志愿方案
agent_created: true
---

# 高考志愿填报技能 (Gaokao Volunteer Filling)

AI-powered college application assistant for Chinese Gaokao. Combines ranking-based matching
(位次法), score-difference analysis (线差法), and reach/match/safety classification (冲稳保)
to generate personalized college application plans.

## When to Use

Activate this skill when the user mentions any of:
- "帮我填志愿" / "高考志愿填报" → full guided workflow
- "XX分能上什么大学" / "能报哪些学校" → quick score matching
- "冲稳保怎么填" / "帮我排志愿梯度" → strategy guidance
- "XX大学XX专业多少分" → single-point lookup
- "检查这份志愿方案" → plan review and gradient analysis
- "XX省高考志愿规则" → province-specific rules
- 查询历年分数线 / 一分一段表 / 位次换算

## Core Workflow

### Phase 1: Information Collection (multi-turn dialogue)

Collect the following from the user in a structured, conversational way:

1. **Province (省份)** — REQUIRED. Determines filling rules template.
2. **Score (分数)** — REQUIRED. Total Gaokao score.
3. **Subject Type (科类)** — REQUIRED. Physical (物理类) / History (历史类) / Comprehensive (综合).
   For new Gaokao provinces, also collect selected subjects (选科).
4. **Rank (位次)** — HIGHLY RECOMMENDED. Provincial ranking from 一分一段表.
   If not provided, estimate from score using batch line difference.
5. **Interests (兴趣方向)** — Optional. Preferred major categories (e.g., 计算机, 医学, 金融).
6. **Location Preference (城市偏好)** — Optional. Preferred cities or regions.
7. **School Level (院校层次)** — Optional. 985 / 211 / 双一流 / 不限.
8. **Batch (批次)** — Default to 本科批 unless specified.

If the user provides incomplete info, ask for missing REQUIRED fields.
Do NOT proceed to Phase 2 until province + score + subject_type are available.

### Phase 2: Data Collection

After gathering user profile, search for relevant data:

#### 2.1 Batch Lines (批次线)
Search for the current year's batch lines for the user's province:
```
WebSearch: "2026年{省份}高考{科类}批次线 本科线"
```
Also search for the previous 2 years for comparison:
```
WebSearch: "2025年{省份}高考{科类}批次线"
WebSearch: "2024年{省份}高考{科类}批次线"
```

#### 2.2 Ranking Data (一分一段表)
If the user has a score but no rank:
```
WebSearch: "2026年{省份}高考一分一段表 {科类} {分数}"
```
Extract the corresponding cumulative rank.
Also find equivalent scores for previous years.

#### 2.3 Admission Scores (院校投档线)
Search for universities matching the user's score range:
```
WebSearch: "2025年{省份}{科类}本科批投档线 {分数范围}"
WebSearch: "2024年{省份}{科类}本科批投档线 {分数范围}"
```
If the user has specific universities in mind, search those specifically.

### Phase 3: Algorithm Processing

Execute the scripts in order:

#### 3.1 Score Delta Calculation
```bash
python scripts/score_delta.py --score {score} --batch-line {line} \
  --prev-lines "{2025_line},{2024_line}"
```
This computes line differences and equivalent scores for previous years.

#### 3.2 Risk Classification
```bash
python scripts/risk_classifier.py --rank {rank} \
  --admissions-data references/admission_sample.json \
  --target-count {max_volunteers}
```
Classifies universities into 冲(Reach) / 稳(Match) / 保(Safety) tiers.

#### 3.3 Ranking Matcher
```bash
python scripts/ranking_matcher.py --rank {rank} --province {province} \
  --subject {subject_type} --interests "{interests}"
```
Matches the user's rank against historical admission data.

#### 3.4 Plan Generation
```bash
python scripts/plan_generator.py --profile references/user_profile.json \
  --matches references/matches.json --template assets/report_template.html \
  --output gaokao_plan_2026.html
```
Generates the final HTML report.

### Phase 4: Report Delivery

1. Render the HTML report using `report_template.html` and the computed data.
2. Open with `open_result_view` or `preview_url` for HTML.
3. Offer to `deliver_attachments` for export/sharing.
4. Provide summary in text: tier counts, top recommendations, risks.

**Key reminders in the report:**
- Data source date — remind user to verify against official sources
- 冲/稳/保 explanation in plain language
- Disclaimer: AI-generated recommendation, final decision belongs to user
- Common risks: 退档, 滑档, 调剂

## Province Rules Quick Reference

Load `references/province_rules.json` for the full rules. Key differences:

| Province | Model | Max Volunteers | Parallel? | Notes |
|----------|-------|---------------|-----------|-------|
| 湖北, 湖南, 广东, 江苏 | 院校专业组 | 45 | Yes | 组内调剂 |
| 山东 | 专业+院校 | 96 | Yes | 无调剂 |
| 浙江 | 专业+院校 | 80 | Yes | 无调剂 |
| 河北, 辽宁, 重庆 | 专业+院校 | 96/112 | Yes | 无调剂 |
| 四川 | 院校+专业 | 9 | Yes | 传统模式 |
| 河南 | 院校+专业 | 12 | Yes | 传统模式 |

Always check `references/province_rules.json` before generating plans for a specific province.

## Important Notes

- **Data freshness**: Gaokao data changes yearly. Always WebSearch for current-year data first.
  Use the scripts only after collecting current data.
- **User privacy**: Do NOT store user scores or ranks permanently. Process in-memory only.
- **Disclaimer**: Always include a disclaimer that this is AI-assisted reference only.
  The user bears full responsibility for final decisions.
- **Fallback**: If WebSearch fails or data is unavailable, guide the user to manually input
  data from official sources (各省教育考试院官网).
- **File paths**: All scripts use absolute paths. Construct paths dynamically using the skill
  directory: skill_dir = `C:\Users\PC\.workbuddy\skills\gaokao-volunteer\`
