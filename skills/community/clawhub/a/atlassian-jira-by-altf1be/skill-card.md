## Description: <br>
Atlassian Jira Cloud CRUD skill - manage issues, comments, attachments, workflow transitions, and JQL search via Jira REST API v3 with email and API token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, project administrators, and support teams use this skill to let an agent inspect and manage Jira Cloud issues, comments, attachments, workflow transitions, and JQL searches from a configured Jira account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Jira email and API-token credentials to read and modify Jira data, including write, delete, attachment, and workflow-transition actions. <br>
Mitigation: Use a least-privileged Jira account or token, verify JIRA_HOST points to the intended Atlassian site, keep tokens out of shared files, and require review before write, delete, attachment, or transition commands. <br>
Risk: Incorrect issue keys, JQL queries, project defaults, or workflow transition selections can affect the wrong Jira records. <br>
Mitigation: Review generated commands and query scope before execution, especially when using default projects, delete confirmations, or transition names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdelkrim/atlassian-jira-by-altf1be) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>
- [Jira Cloud](https://www.atlassian.com/software/jira) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can trigger Jira REST API reads and writes through user-provided credentials; command output depends on Jira permissions and API responses.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
