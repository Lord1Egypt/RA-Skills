## Description: <br>
Captures learnings, errors, and corrections so agents can maintain local improvement notes and promote durable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suncrespo](https://clawhub.ai/user/suncrespo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record failures, user corrections, knowledge gaps, and feature requests in local markdown logs, then promote broadly useful lessons into agent guidance files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture sensitive details if used carelessly. <br>
Mitigation: Keep entries concise and redacted; do not store secrets, tokens, environment dumps, raw transcripts, or full command output. <br>
Risk: Optional hooks can add automatic reminders or inspect command outcomes in sensitive workspaces. <br>
Mitigation: Leave hooks disabled unless needed, prefer project-level activation, and avoid global or user-level hook activation for sensitive work. <br>
Risk: Promoting notes into agent guidance can preserve incorrect or overly broad lessons. <br>
Mitigation: Review promoted guidance before use and keep project memory focused on validated, broadly useful lessons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suncrespo/12123123123) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Entry examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .learnings markdown files and may provide optional hook setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
