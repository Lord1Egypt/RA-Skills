## Description:

Add self-sustaining autonomous loop capability to an OpenClaw agent. The agent keeps working after each reply until a stop file is placed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasye378](https://clawhub.ai/user/lucasye378)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or convert OpenClaw agents that continue working across repeated task cycles until paused by a stop file or stop token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep an agent running unattended with broad, persistent authority.

Mitigation: Install it only in workspaces where unattended activity is intended, use narrow per-agent messages, create stop files before sensitive work, and monitor the loop logs.

Risk: Autonomous loops can amplify harm when paired with agents that can deploy, delete data, access secrets, or take irreversible actions.

Mitigation: Avoid using the skill with those agents unless a human review gate or similarly strong control is in place.

Risk: Running this plugin with another reply-trigger loop for the same agent can send duplicate follow-up messages.

Mitigation: Enable only one loop plugin per agent ID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasye378/skills/autonomous-loop)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and plugin code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw on macOS according to artifact metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact plugin manifests report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
