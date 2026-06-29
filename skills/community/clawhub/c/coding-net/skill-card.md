## Description: <br>
Queries and manages Tencent Coding DevOps workspace data on e.coding.net, including iterations, issues, requirements, defects, tasks, and team members, with support for creating requirements and defects through the Coding Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyin717](https://clawhub.ai/user/wangyin717) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to inspect Coding.net project iterations, issue lists, individual issue details, defect types, and team members, then create requirements or defects after confirming project-specific fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Coding.net bearer token and can access workspace data. <br>
Mitigation: Set CODING_TOKEN as a secure environment variable, avoid pasting tokens into chat, and grant only the minimum token permissions needed. <br>
Risk: Create-issue and create-defect actions can mutate project data. <br>
Mitigation: Review issue names, assignees, dates, labels, custom fields, issue types, and defect types before sending create actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyin717/coding-net) <br>
- [Coding.net Open API endpoint](https://e.coding.net/open-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Coding.net bearer token supplied through CODING_TOKEN or an explicit token parameter.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
