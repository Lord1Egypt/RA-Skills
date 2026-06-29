# Admission Mode Reference

This reference guides the skill to switch analysis mode by province and year. Always verify current-year policy from official sources.

## Common modes

### 院校专业组
The志愿 unit is a school + major group. Analyze group cutoff, all majors inside the group, and adjustment risk.

### 专业+院校
The志愿 unit is a specific major at a school. Focus on professional cutoff/rank and subject requirements. Same-group调剂 risk is usually lower.

### 院校+专业
The志愿 unit starts with school. Analyze school投档线 and校内专业分流/调剂.

### 一段/二段专业平行
Usually direct to major/program. Compare professional rank and line margins to一段/二段/特殊类型线.

### 传统文理科
Use理科/文科 lines, school投档线,专业录取分, and adjustment risk.

## Province policy object

```yaml
province_policy:
  province:
  year:
  admission_mode:
  subject_system:
  application_unit:
  risk_unit:
  has_major_adjustment:
  typical_choice_count:
  score_line_names:
    undergraduate:
    special:
```
