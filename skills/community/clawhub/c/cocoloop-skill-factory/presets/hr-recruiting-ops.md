# 人力与招聘运营预设

## domain_id

`hr_recruiting_ops`

## common_jobs

- 整理 JD、简历、候选人记录和面试反馈
- 生成候选人摘要、面试题、评分表和沟通邮件草稿
- 跟踪招聘漏斗、面试安排和 offer 流程
- 维护员工入职、培训、绩效和制度文档
- 分析招聘渠道、通过率、周期和岗位需求

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标场景是招聘、入职、培训、绩效，还是 HR 文档整理
- 使用的 ATS、HRIS、日历或文档系统是什么
- 需要处理哪些对象，例如 JD、简历、面试记录、评分表或 offer
- 是否允许自动联系候选人，还是只生成待审核草稿
- 是否有岗位标准、评分维度、合规要求或公平性要求
- 是否涉及个人信息、薪酬、绩效或敏感评价
- 成功标准是匹配质量、流程效率、记录完整，还是合规可追溯

## recommended_execution_planes

- `Skill-only`
  适合 JD 草稿、面试题、评分表和人工审核建议
- `Skill + API/MCP`
  适合 ATS、HRIS、日历、邮件和文档系统联动
- `Skill + CLI + API/MCP`
  适合批量简历整理、漏斗报告、面试排程和系统写回

## risk_and_gates

- 候选人和员工个人信息必须脱敏或限定访问范围
- 面试与筛选建议必须保留人工决策
- 薪酬、绩效、辞退和纪律事项需要高风险 gate
- 自动邮件、自动邀约和 offer 流程必须单独确认
- 评分标准需要可解释，避免不可追溯的黑箱判断

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.hr_recruiting_ops`
- 如果涉及候选人筛选，必须补公平性和人工复核 gate
