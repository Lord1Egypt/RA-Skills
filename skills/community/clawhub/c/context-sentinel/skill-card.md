## Description:

Monitors session context and automatically manages model switching based on a cascading protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nietzsche247](https://clawhub.ai/user/nietzsche247)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add periodic session-health checks that recommend model switching, handoff, or no action based on context usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to automate model switching and handoff actions through referenced files that are not present in the artifact.

Mitigation: Review the missing check_context.ps1 and MEMORY.md logic before installation, and require explicit user approval before switching models or writing handoff files.

Risk: A script path could resolve outside the reviewed package content if wired into a heartbeat or scheduled job carelessly.

Mitigation: Pin the script path to reviewed package content and verify the resolved path before enabling cron or HEARTBEAT.md automation.

## Reference(s):

- [Context Sentinel ClawHub page](https://clawhub.ai/nietzsche247/skills/context-sentinel)
- [nietzsche247 publisher profile](https://clawhub.ai/user/nietzsche247)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command strings and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected action strings are STATUS_OK, SWITCH_TO:<model_id>, or HANDOFF_NOW when the referenced script is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
