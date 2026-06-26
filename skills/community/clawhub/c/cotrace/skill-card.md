## Description: <br>
Cotrace helps an agent collect and query a user's work-activity history through Pieces OS, Cotrace, and the ftc CLI to retrieve personal work context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyqqj0](https://clawhub.ai/user/tyqqj0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to let an agent check recent or date-bounded work records, summarize what they worked on, and retrieve detailed Cotrace entries with AI annotations. It is also used to guide setup and health checks when Cotrace or the ftc CLI is not yet available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive work-activity history and personal context. <br>
Mitigation: Ask for explicit user approval before querying records, prefer narrow time ranges, and avoid broad or empty filters unless the user clearly requests them. <br>
Risk: Setup adds and authenticates an external ftc bridge and may install a global CLI package. <br>
Mitigation: Get explicit approval before installing packages, adding endpoints, logging in, or sending data through the configured bridge. <br>
Risk: The security scan verdict is suspicious due to broad external access and limited privacy and scope disclosure. <br>
Mitigation: Install only when the user trusts the Cotrace/Pieces setup, the ftc CLI package, and the listed bridge with work-activity data. <br>


## Reference(s): <br>
- [Cotrace install and configuration guide](references/install.md) <br>
- [Cotrace user setup documentation](https://nxwu5gzs9f9.feishu.cn/wiki/DsVrwc2QMiVhR4kigdMct8XKntg) <br>
- [Cotrace skill page](https://clawhub.ai/tyqqj0/cotrace) <br>
- [Cotrace ftc bridge](https://ftc-bridge.apiservice.autolab-server.site) <br>
- [Cotrace ftc bridge alias endpoint](https://ftc-bridge.apiservice.autolab-server.site/api/80noahia7rhpdoipbihqe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ftc CLI calls to return workstream summaries and detail records; timestamps returned by the tool are UTC and should be converted for the user.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
