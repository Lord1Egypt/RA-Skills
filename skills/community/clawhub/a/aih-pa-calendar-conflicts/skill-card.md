## Description:

将多个日历的导出数据、时区及参与者约束整理为冲突报告、调整建议和待导入的日历文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

个人或团队可用它对照多个日历，识别时间冲突并审阅尽量少改动的候选时段；如需写回日历，须另行取得连接器权限和明确授权。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 不明确的时区、夏令时回拨或全天事件可能造成错误的冲突判断。

Mitigation: 保留原始时区；单独核对夏令时及全天事件，遇到歧义先请用户确认具体时刻。

Risk: 接入 AI-HIVE 或日历连接器可能涉及敏感日程上传、费用或未经授权的写回。

Mitigation: 先核对官方域名、工具权限、上传范围、报价及预算；最小化敏感数据，并在任何付费或日历写回前取得明确授权。

Risk: 未取得工具回执或授权时，草稿可能被误当作已执行的日历变更。

Mitigation: 区分草稿与完成状态；仅凭实际执行证据和验收结果确认完成，缺少连接器时只交付待审阅文件。

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/wubin1836/skills/aih-pa-calendar-conflicts)
- [执行与验收流程](references/workflow-09.md)
- [结果与证据要求](references/output-contract.md)
- [AI-HIVE 连接与授权说明](references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Markdown 冲突报告、CSV 变更建议和待导入的 iCalendar (.ics) 文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [默认交付可审阅草稿；可附带 JSON 结果记录及证据引用，不自动写回日历。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
