## Description:

The Exploration Mode Skill enables an agent to autonomously perform research, maintenance, security review, reflection, knowledge, and optimization tasks during idle time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzh0916](https://clawhub.ai/user/yzh0916)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an OpenClaw-based agent switch between user collaboration and idle-time autonomous exploration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous idle-time work can cover broad maintenance, cleanup, security review, and optimization tasks without sufficiently documented controls.

Mitigation: Define local rules before use: read-only exploration by default, explicit approval for file writes, cleanup, installs, configuration changes, security changes, memory updates, and clear limits on paths, time, tools, and cancellation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzh0916/skills/exploration-mode-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses, potentially with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode switching prompts, status responses, and autonomous task proposals; execution should follow local approval limits.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
