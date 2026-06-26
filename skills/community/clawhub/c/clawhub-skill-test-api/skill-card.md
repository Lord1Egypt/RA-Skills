## Description: <br>
Weaver E10 API helps agents call Weaver E10 workflow APIs to create requests, query todos, approve submissions, reject workflows, inspect workflow state, and manage OAuth2 token refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xfnet](https://clawhub.ai/user/xfnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to automate Weaver E10 workflow actions from an agent environment while relying on configured OAuth2 credentials and cached tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, approve, and reject Weaver E10 business workflows using stored credentials without built-in confirmation controls. <br>
Mitigation: Require explicit human confirmation before running create, approve, or reject commands, and restrict allowed users and workflows in Weaver where possible. <br>
Risk: The skill depends on Weaver credentials and cached OAuth tokens stored outside the skill files. <br>
Mitigation: Use least-privileged Weaver credentials, protect the env file and token cache, and avoid logging authentication output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xfnet/clawhub-skill-test-api) <br>
- [Publisher profile](https://clawhub.ai/user/xfnet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can produce JSON responses from Weaver E10 API calls and may read configured credentials and cached tokens.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
