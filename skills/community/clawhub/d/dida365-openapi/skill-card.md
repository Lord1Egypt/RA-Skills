## Description: <br>
Dida365 Openapi helps an agent manage Dida365 tasks, projects, tags, reminders, and repeat rules through the official OpenAPI and OAuth2 using a bundled zero-dependency Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[workingcoder](https://clawhub.ai/user/workingcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to let an agent authenticate with Dida365, read task and project data, and perform task-management actions such as create, update, complete, move, filter, and delete through the documented OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Dida365 tasks and projects after OAuth login. <br>
Mitigation: Require user confirmation before deletes, moves, project edits, and bulk task changes. <br>
Risk: OAuth credentials and tokens are stored in local configuration files. <br>
Mitigation: Protect local config and token files and avoid exposing DIDA365_CLIENT_SECRET or access tokens in logs or shared terminals. <br>
Risk: Overriding OAuth or API base URLs could send credentials or task data to an untrusted endpoint. <br>
Mitigation: Keep OAuth and API base URLs pointed at trusted Dida365 endpoints unless the user has explicitly validated an alternative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/workingcoder/dida365-openapi) <br>
- [Dida365 developer platform](https://developer.dida365.com) <br>
- [Dida365 OpenAPI GitHub documentation](https://github.com/workingcoder/dida365-openapi) <br>
- [API Reference Notes](references/api-reference.md) <br>
- [Auth And Config](references/auth-and-config.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; bundled CLI commands return JSON on stdout and structured JSON errors on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and DIDA365_CLIENT_ID / DIDA365_CLIENT_SECRET for OAuth setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
