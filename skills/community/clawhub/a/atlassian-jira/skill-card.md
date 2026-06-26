## Description: <br>
Manage Jira Cloud issues: search, create, update, comment, transition, assign, and list project and user data through Jira Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pejovicvuk](https://clawhub.ai/user/pejovicvuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and project teams use this skill to manage Jira Cloud issues from an agent workflow, including searching issues, creating tickets, commenting, updating fields, assigning users, and changing workflow status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change live Jira Cloud records using configured credentials. <br>
Mitigation: Install only in trusted workspaces, use a least-privileged Jira API token limited to intended projects, and require explicit human approval before create, comment, transition, assign, or update commands. <br>
Risk: User and project enumeration can expose Jira account and project metadata. <br>
Mitigation: Limit broad user searches and project listing to cases where the task needs them, and avoid sharing returned account details outside the authorized workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pejovicvuk/atlassian-jira) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses from a bash CLI wrapper, with Markdown setup and command guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN, curl, and python3; write commands can modify live Jira Cloud records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
