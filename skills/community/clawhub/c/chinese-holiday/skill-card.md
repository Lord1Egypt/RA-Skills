## Description: <br>
查询中国法定节假日、周末和调休安排，用于判断某一天是否为节假日、工作日或调休补班日。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents that need China calendar scheduling checks use this skill to classify dates as workdays or holidays and to account for statutory holidays, weekends, and make-up workdays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday and workday checks depend on timor.tech availability and accuracy. <br>
Mitigation: Verify results separately for critical scheduling, payroll, legal, or operations decisions. <br>
Risk: Date and year lookups are sent to an external API and may reveal the scheduling context being checked. <br>
Mitigation: Avoid submitting sensitive planning dates when external disclosure is not acceptable. <br>
Risk: If the API does not return a holiday record, the script falls back to weekday/weekend classification, which can miss statutory holidays or make-up workdays. <br>
Mitigation: Treat fallback-sourced results as lower confidence and confirm them against an authoritative calendar. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/chinese-holiday) <br>
- [timor.tech holiday API endpoint used by the skill](https://timor.tech/api/holiday/year/{year}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text date classifications or JSON arrays emitted by the Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more dates in YYYY-MM-DD or YYYYMMDD format and optionally emits JSON with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
