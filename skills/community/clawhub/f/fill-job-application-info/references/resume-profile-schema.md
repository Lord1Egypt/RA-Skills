# 候选人资料结构 Schema

在从简历提取候选人资料、修复字段映射、或把资料写回招聘表单时，使用这份结构作为统一工作形态。

## 规范工作结构

```yaml
candidate:
  full_name:
  first_name:
  last_name:
  email:
  phone:
  location:
    city:
    state_or_region:
    country:
  headline:
  summary:
  links:
    linkedin:
    github:
    portfolio:
    website:
experience:
  - company:
    title:
    location:
    start_date:
    end_date:
    current:
    bullets: []
education:
  - school:
    degree:
    field_of_study:
    start_date:
    end_date:
certifications:
  - name:
    issuer:
    date:
skills: []
languages: []
projects:
  - name:
    role:
    date:
    bullets: []
application_overrides:
  work_authorization:
  sponsorship_needed:
  desired_salary:
  notice_period:
  relocation:
  preferred_work_arrangement:
  custom_answers: {}
missing_fields: []
ambiguities: []
```

## 规范化规则

- 保留姓名、公司名、学校名、学位名称的原始拼写和大小写
- 内部日期统一为 `YYYY-MM` 或 `YYYY-MM-DD`
- 把 `Present`、`Current`、`至今` 等值转换为 `current: true`，并把 `end_date` 留空
- 仅在拆分非常明确时，才把 `full_name` 拆成 `first_name` 和 `last_name`
- 链接尽量保留完整 URL，包括 `https://`
- 手机号在必要时保留一份规范化数字版本，但原始格式也要保留，便于按目标表单格式输出

## 映射提示

- `Current company` 映射到 `experience` 中 `current: true` 的条目；若没有，则映射到最近一段经历
- `Current title` 采用同样规则
- `State`、`Province`、`Region` 都映射到 `state_or_region`
- `Portfolio` 或 `Website` 字段优先映射到个人作品站；不要静默用 LinkedIn 代替，除非表单明确允许
- 只有在规则明确且无重叠歧义时，才计算工作年限；存在兼职、重叠任职或时间不清晰时，先标为歧义并向用户确认

## 默认不要推断的值

- work authorization
- sponsorship requirement
- expected compensation
- notice period
- relocation preference
- EEO 或人口统计字段
- 身份证、护照、证件号等法定身份信息

## 允许占位数据的例外

- 仅当用户明确要求“自动生成”“占位填写”“先随便填一版”时，才生成演示用虚构资料
- 占位资料必须与真实候选人资料分开管理，避免覆盖真实值
- 交付时明确说明哪些字段是占位数据

## 核对清单

- 按结构化候选人资料逐项核对姓名、手机号、邮箱
- 复核每一段工作经历和教育经历的年月
- 复核所有链接，尤其是 LinkedIn、GitHub、个人网站
- 复核用户后来补充或修正过的覆盖字段
- 针对中文招聘报名表，额外复核出生年月、籍贯、民族、政治面貌、身份证号等敏感字段
