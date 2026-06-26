## Description: <br>
Determines whether today or a specified date is a working day in mainland China by querying holiday-cn yearly JSON from jsDelivr and applying holiday and makeup-workday rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sube-py](https://clawhub.ai/user/Sube-py) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People and workflows that need China calendar checks use this skill to determine whether a current or specified date is a workday, holiday, or makeup workday and to return a clear reason with the data source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday and makeup-workday decisions depend on a third-party public holiday dataset. <br>
Mitigation: For important scheduling, payroll, legal, or operational decisions, verify results against an official source. <br>
Risk: The skill requires outbound access to fetch public holiday data. <br>
Mitigation: Run it only in environments where the jsDelivr holiday data request is expected and allowed. <br>


## Reference(s): <br>
- [holiday-cn yearly JSON data](https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from a Python command, usually summarized in Markdown by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes queried date, is_workday boolean, reason, and data source URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
