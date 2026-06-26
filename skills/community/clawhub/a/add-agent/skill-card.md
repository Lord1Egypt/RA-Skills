## Description: <br>
Add a new OpenClaw Agent, automatically configure openclaw.json, create workspace, copy auth and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[owen-ai-01](https://clawhub.ai/user/owen-ai-01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create an isolated OpenClaw agent with a dedicated Telegram bot, generated workspace files, copied skills, and agent-to-agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies persistent OpenClaw configuration and workspace files. <br>
Mitigation: Review the generated commands and openclaw.json diff before execution, and keep the documented backup available for rollback. <br>
Risk: The skill copies authentication profiles from the main agent to the new agent. <br>
Mitigation: Prefer separate least-privilege credentials for the new agent instead of copying the main agent auth profile wholesale. <br>
Risk: The skill accepts agent identifiers, Telegram bot tokens, allow lists, and role descriptions from user input. <br>
Mitigation: Use trusted parameter values only and validate the resulting JSON before restarting the OpenClaw gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/owen-ai-01/add-agent) <br>
- [Publisher profile](https://clawhub.ai/user/owen-ai-01) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and generated Markdown snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step instructions for modifying local OpenClaw configuration and creating agent workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
