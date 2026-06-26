## Description: <br>
Query and manage GitHub repositories, including listing repositories, checking CI status, creating issues, searching repositories, and viewing recent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect GitHub repositories, monitor workflow status, search repository metadata, and perform repository write actions such as creating issues, repositories, and pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub token that may permit repository changes. <br>
Mitigation: Use a fine-grained token limited to the specific repositories and permissions needed for the task. <br>
Risk: The skill can create repositories, issues, and pull requests without a built-in confirmation step. <br>
Mitigation: Manually confirm the owner, repository, visibility, title, body, branches, and target before executing write actions. <br>
Risk: GitHub credentials may be exposed if stored or shared incorrectly. <br>
Mitigation: Keep tokens out of source control, prefer a credential store for shared or production environments, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yesong-hue/agent-github-workflow) <br>
- [GitHub Personal Access Tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Markdown or structured tool results describing repository data, CI status, issues, pull requests, and setup values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub credentials via GITHUB_TOKEN or github.token and may use GITHUB_USERNAME or github.username.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
