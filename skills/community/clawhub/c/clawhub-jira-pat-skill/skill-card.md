## Description: <br>
Manage Jira issues on self-hosted or enterprise Jira instances using Personal Access Tokens in SSO/SAML environments where Basic Auth fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dejanb](https://clawhub.ai/user/dejanb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, search, comment on, update, create, and transition Jira issues on trusted self-hosted or enterprise Jira instances that require Personal Access Token authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can create, comment on, update, or transition Jira issues. <br>
Mitigation: Review write commands before execution and use a least-privilege Jira Personal Access Token. <br>
Risk: The configured Jira URL and token determine which Jira instance and permissions the commands use. <br>
Mitigation: Install this only for trusted Jira instances, set JIRA_URL carefully, and store JIRA_PAT securely. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dejanb/clawhub-jira-pat-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and shell helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require JIRA_PAT and JIRA_URL and may read or modify Jira issues depending on the operation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
