---
name: gaokao-volunteer-risk-skill-cn-adaptive
description: Analyze Chinese gaokao志愿填报 plans nationwide. Use this skill when a user asks to evaluate, rank, redesign, or generate college application choices based on score, rank, province-specific admission mode, subject requirements, line margins, major fit, tuition constraints, and transfer-major risk. This skill auto-retrieves public admission data whenever possible and adapts to province-specific志愿模式.
---

# 全国自适应高考志愿风险分层与专业适配 Skill

## Purpose

Use this skill to analyze Chinese gaokao application plans across provinces. It converts a student's score, rank, subjects, preferences, and constraints into a province-aware冲稳保志愿方案.

The skill must adapt to the province's admission mode instead of assuming江苏院校专业组模式.

Core goals:

1. Minimize user input.
2. Auto-retrieve public data: current and historical batch lines, special-control lines,投档线,招生计划,选科要求,学费,中外合作/高收费 flags.
3. Analyze at the correct application unit for the province:
   - 院校专业组
   - 专业+院校
   - 院校+专业
   - 一段/二段专业平行志愿
   - traditional文理科院校志愿
4. Produce an actionable冲、稳、保、删除/替换 list with school and major-level reasoning.

## Minimum user input

Ask the user only for information that cannot be reliably inferred online or must reflect personal preference.

Required:

- Province
- Admission year
- Category/track: 物理类/历史类, 理科/文科, or 3+3 subjects depending on province
- Score
- Rank/位次, strongly preferred; if absent, warn that precision declines
- Selected subjects or 文理科
- Preferred fields/majors
- Avoided fields/majors
- Whether they accept:
  - 民办本科
  - 职业本科
  - 中外合作/高收费/学分互认/海外项目
  -省外学校
- Uploaded志愿表 if available

Do not require the user to provide本科线、特控线、一段线、二段线、近年投档线、招生计划、选科要求、学费. Retrieve these automatically.

## Auto-retrieved data

Retrieve or verify these from public sources whenever possible:

1. Current-year and previous-year score lines:
   - 本科线
   - 特控线 / 特殊类型招生控制线
   - 一段线 / 二段线 where applicable
   - 一本线/二本线 for older/traditional contexts
2. Current-year招生计划 and subject requirements.
3. Previous 1–3 years of:
   - 院校投档线
   - 院校专业组投档线
   - 专业投档线 / 专业录取分
   - 位次
4. Tuition:
   - 公办普通学费
   - 民办学费
   - 中外合作/高收费/学分互认/海外项目学费
5. Province admission policy:
   - 志愿单位
   - 志愿数量
   - 是否有专业服从调剂
   - 批次规则

## Source priority

Use sources in this order:

1. Provincial education examination authority / admissions office official website.
2. Official PDF/Excel documents released by provincial authorities.
3. University undergraduate admissions website.
4. University admissions章程.
5. Ministry/provincial education department public information.
6. Reputable education data platforms only as auxiliary, never as sole basis if official data is available.

Always cite online sources in the final response when web data is used. If a datum cannot be verified from official sources, mark it as “需复核”.

## Province policy detection

Before analyzing risk, identify the province's admission mode.

Create a `province_policy` object:

```yaml
province_policy:
  province: 江苏
  year: 2026
  admission_mode: 院校专业组 | 专业+院校 | 院校+专业 | 一段/二段专业平行 | 传统文理院校志愿
  subject_system: 3+1+2 | 3+3 | traditional_arts_science
  category_names:
    physics_or_science: 物理类/理科/综合改革
    history_or_arts: 历史类/文科
  application_unit: 院校专业组 | 专业 | 院校
  risk_unit: 院校专业组+专业 | 专业 | 院校+校内专业
  has_major_adjustment: true | false | depends
  typical_choice_count: number_or_unknown
  score_line_names:
    undergraduate: 本科线/一段线/二段线/二本线
    special: 特控线/特殊类型招生控制线/一本线
```

If province rules are uncertain or may have changed, search the web and verify from official sources.

## Admission-mode-specific analysis

### 1. 院校专业组模式

Typical provinces include江苏、广东、湖南、湖北、福建 and some other 3+1+2 provinces depending on year.

Analyze:

- 院校专业组投档线
- 组内全部专业
- 选科要求
- 专业录取分 if available
- 专业服从调剂 risk

Risk unit:

```text
院校专业组 + 组内专业
```

Key rule:

进档不等于进入理想专业。If the group contains disliked majors, mark调剂风险.

### 2. 专业+院校模式

Typical provinces include山东、浙江、河北、辽宁、重庆等, depending on year and batch.

Analyze:

- Each志愿 is a specific major/program at a school.
- Usually no same-group调剂 risk for that志愿 unit.
- Professional fit and专业位次 are more important than school group line.

Risk unit:

```text
专业
```

Key rule:

Do not apply院校专业组调剂 logic. Focus on专业线、专业位次、计划人数、选科要求.

### 3. 院校+专业模式

Used in some traditional or mixed contexts.

Analyze:

- School投档线 first.
- Then校内专业分流 or专业录取分.
- 专业服从调剂 risk may be high.

Risk unit:

```text
院校投档 + 校内专业
```

Key rule:

If the school can admit the student but target majors are much hotter, warn about being assigned to lower-preference majors.

### 4. 一段/二段专业平行志愿模式

Used by浙江、山东 style systems.

Analyze:

- Use一段线/二段线 and特殊类型控制线 if relevant.
- Compare专业投档位次 and招生计划.
- The application unit is generally专业+学校.

Risk unit:

```text
专业+学校
```

### 5. 传统文理科模式

Analyze:

- 文科/理科 line differences.
- 一本/二本/本科线 and rank.
- School投档线 and professional admission scores.
- Major adjustment risk within school.

## Line-margin methodology

Do not judge by absolute score alone.

Calculate:

```text
student_undergraduate_margin = student_score - current_undergraduate_line
student_special_margin = student_score - current_special_line
student_rank = rank
```

For each historical year:

```text
historical_undergraduate_margin = historical_cutoff - historical_undergraduate_line
historical_special_margin = historical_cutoff - historical_special_line
rank_gap = student_rank - historical_rank
```

Use line margin and rank together:

- For热门专业、热门城市、热门工科, prioritize特控线差 and rank.
- For保底志愿, prioritize本科线差/一段线差 and rank.
- For专业+院校 mode, prioritize专业位次.

## Risk classification

Default risk categories:

```yaml
risk_categories:
  high_rush: 高冲
  rush: 冲刺
  match: 稳中带冲
  stable: 稳
  safe: 保底
  remove: 建议删除/替换
```

Suggested rule based on special-line margin gap:

```yaml
if historical_special_margin >= student_special_margin + 8:
  risk: 高冲
elif historical_special_margin >= student_special_margin + 3:
  risk: 冲刺
elif abs(historical_special_margin - student_special_margin) < 3:
  risk: 稳中带冲
elif historical_special_margin <= student_special_margin - 3:
  risk: 稳
elif historical_special_margin <= student_special_margin - 10:
  risk: 保底
```

Adjust risk upward when:

- plan count < 10
- major/program is newly popular
- city is very hot
- target major is热门工科/医学/计算机/法学/师范热门专业
- historical rank is much better than student rank
- current-year plan decreases
- only one year of data exists

Adjust risk downward cautiously when:

- plan count increases substantially
- historical cutoff fell for 2 consecutive years
- disliked or cold major lowers competition

Never mark as保底 if:

- plan count is tiny
- subject requirements are uncertain
- the group contains unacceptable调剂 majors
- tuition exceeds the user's limit

## Subject requirement filtering

Always check subject requirements before recommending.

Rules:

- If the student does not satisfy the subject requirement, mark as不可报 and remove.
- For 3+1+2 provinces, distinguish首选科目 and再选科目.
- For 3+3 provinces, handle any-subject combinations.
- If a target major requires物理+化学 and the student lacks化学, do not recommend it unless the official plan says otherwise.

## Major-fit analysis

Analyze each recommended志愿 at the major level.

Return:

- recommended majors
- acceptable majors
- avoid majors
- adjustment risk
- employment direction

Example categories can be customized by user preference.

For工科/智能制造 preference:

Strong fit:

- 电气工程及其自动化
- 自动化
- 智能控制
- 机械电子
- 电子信息
- 集成电路
- 机器人工程/机器人技术
- 新能源汽车工程
- 人工智能工程
- 智能制造
- 信息安全

Medium fit:

- 工程管理
- 工业工程
- 信息管理与信息系统
- 大数据管理与应用
- 物流工程/物流管理
- 工程审计
- 应急管理
- 数字经济
- 知识产权

Avoid if the user dislikes them:

- 旅游管理
- 酒店管理
- 学前教育
- 商务英语
- 小语种
- 心理学
- 汉语言文学
- 秘书学
- 市场营销
- 人力资源管理

## Tuition and project filtering

If user rejects高收费/中外合作/海外项目, remove:

- 中外合作办学
- 高收费专业
- 学分互认
- 国际课程
- 海外联合培养
- 必须出国项目

For民办本科, always display annual tuition if available and mark “需以当年招生章程为准”.

## Major-transfer policy

Transfer-major analysis is optional and secondary.

Rules:

- Do not rely on转专业 as main strategy.
- If the current major is already acceptable, no transfer is needed.
- If the current major is unacceptable, do not recommend it merely because transfer might be possible.
- If asked, retrieve the university's official transfer policy and classify:
  - A: 不需要转
  - B: 原专业可接受，可尝试转
  - C: 可保底，不适合作为转工科跳板
  - D: 不建议依赖转专业

## Output requirements

Return a clear, actionable report.

Minimum sections:

1. Student baseline and province policy.
2. Data sources and data quality notes.
3. Risk methodology.
4. Final冲稳保 list.
5. Major-level recommendations.
6. Deletion/replacement list.
7. Tuition/cost warnings.
8. Transfer-major notes if relevant.
9. Final verification checklist.

For a final志愿 list, include columns:

```text
序号 | 层级 | 志愿单位 | 学校 | 专业/专业组 | 推荐专业 | 避免专业 | 近年线差 | 位次风险 | 计划数 | 学费 | 调剂风险 | 最终建议
```

## Honesty and uncertainty

If official data cannot be verified:

- Do not invent.
- Mark “未核到官方来源”.
- Explain what must be checked in the招生计划专刊 or学校招生网.

