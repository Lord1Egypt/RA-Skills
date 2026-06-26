## Description: <br>
Generates TikTok product trend reports from FastMoss daily and weekly rankings, including analysis and sourcing recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ISLCY1208](https://clawhub.ai/user/ISLCY1208) <br>

### License/Terms of Use: <br>


## Use Case: <br>
E-commerce and merchandising teams use this skill to collect FastMoss TikTok daily and weekly Top 10 data for a configured category and region, then generate a shareable report with product insights and sourcing suggestions. <br>

### Deployment Geography for Use: <br>
Global; report data defaults to the United States unless FASTMOSS_REGION is configured. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored FastMoss credentials during login. <br>
Mitigation: Use scoped credentials, avoid shared or hard-coded passwords, and rotate or revoke credentials if exposure is suspected. <br>
Risk: The skill can deploy generated reports externally. <br>
Mitigation: Require manual review of report content and destination before publishing or sharing a deployed report. <br>
Risk: The skill can post report links to private messages and a configured Feishu group. <br>
Mitigation: Leave FEISHU_GROUP_ID unset unless group posting is intended, and confirm recipients before sending report links. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown progress updates plus an HTML report and deployed report URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send the report link to private messages and a configured Feishu group.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
