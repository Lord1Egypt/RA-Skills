## Description:

Set up, verify, or repair EverMe memory for OpenClaw. Use when the user asks to install EverMe or the EverMe memory plugin, wants OpenClaw to share the work memory they already use in other AI tools, or reports that EverMe is not recalling or not saving in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everme](https://clawhub.ai/user/everme)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to install and verify EverMe memory, repair common recall or saving problems, and manage the plugin's settings or removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The uninstall guidance removes the EverMe integration and restarts the OpenClaw gateway without a documented post-removal check or restoration step.

Mitigation: Before running uninstall commands, review the active context-engine and memory settings with the user, then verify the gateway and intended memory setup after restart.

Risk: The security assessment is incomplete because referenced paths were missing during scanning.

Mitigation: Review the complete referenced source material before installation; do not treat the benign assessment as proof that the skill is risk-free.

## Reference(s):

- [EverMe OpenClaw plugin source](https://github.com/EverMind-AI/EverMe/tree/main/plugins/openclaw)
- [EverMe account and memory management](https://everme.evermind.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup, verification, troubleshooting, settings, and uninstall guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
