## Description: <br>
Connect Claude to external apps like Gmail, Slack, GitHub so users can send emails, create issues, post messages, and take actions in external services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to install and configure Composio Tool Router so Claude can operate connected services such as email, chat, developer, docs, and data apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes users into a broad third-party integration that can perform real actions across external accounts. <br>
Mitigation: Review Composio and app-level OAuth practices, start with limited or test accounts, and grant the narrowest scopes available. <br>
Risk: Connected services may send, post, create, update, or delete data if the agent is allowed to proceed unchecked. <br>
Mitigation: Require explicit confirmation before any send, post, create, update, or delete action and know how to revoke both Composio and app-level access. <br>


## Reference(s): <br>
- [Connect Apps on ClawHub](https://clawhub.ai/sohamganatra/connect-apps) <br>
- [sohamganatra ClawHub profile](https://clawhub.ai/user/sohamganatra) <br>
- [Composio Platform](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and example prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of a third-party integration that can execute actions in connected external accounts after authorization.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
