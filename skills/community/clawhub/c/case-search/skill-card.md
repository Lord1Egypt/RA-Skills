## Description: <br>
案例查询检索，根据用户实际场景检索并匹配最相关的案例数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuwano1](https://clawhub.ai/user/zhuwano1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal researchers, lawyers, and users seeking comparable Chinese legal cases can use this skill to match a described scenario against the bundled case categories and return up to three relevant case details. If no local match is found, the skill may look up related cases through configured helper tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal queries can include sensitive personal, business, or case details, and unmatched queries may be sent to a web-search helper. <br>
Mitigation: Share only details needed for case matching, review helper-tool configurations before use, and avoid entering private legal or personal information unless the deployment is trusted. <br>
Risk: Matched case numbers may be queried through a database helper, so results depend on the availability and correctness of that configured data source. <br>
Mitigation: Confirm database access, validate returned case details against authoritative legal sources, and review the output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuwano1/case-search) <br>
- [Case category index](case_info/case_index.md) <br>
- [Traffic accident cases](case_info/traffice_accident.md) <br>
- [Personal injury cases](case_info/human_hurt.md) <br>
- [Divorce property division cases](case_info/finance_divorce.md) <br>
- [Property misappropriation cases](case_info/finance_eat.md) <br>
- [Theft cases](case_info/finance_steal.md) <br>
- [Corruption and bribery cases](case_info/corruption_bribery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown-style legal case fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to three matched cases with case number, court, hearing time, facts and reasons, legal basis, court reasoning, and judgment fields; returns empty field values when no relevant case is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
