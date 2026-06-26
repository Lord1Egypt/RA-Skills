## Description: <br>
Monitors session context and automatically manages model switching based on a cascading protocol. Use as part of a heartbeat or cron job to maintain session health and optimize token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nietzsche247](https://clawhub.ai/user/Nietzsche247) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add context-health checks to heartbeat or scheduled workflows and decide whether to switch models, trigger a handoff, or continue the current session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to run check_context.ps1, but that PowerShell script is not included in the package. <br>
Mitigation: Do not add the skill to cron or an agent heartbeat until the script is present, reviewed, and tested. <br>
Risk: Automated model switching or handoff actions can change an active agent session unexpectedly. <br>
Mitigation: Limit script outputs to known-safe model IDs and keep model changes or handoffs under clear user control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Nietzsche247/context-sentinel) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown instructions with PowerShell and command snippets; referenced script output is plain string commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected action strings are SWITCH_TO:<model_id>, HANDOFF_NOW, or STATUS_OK.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
