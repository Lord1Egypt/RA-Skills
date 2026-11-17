## Description:

Long-term memory for OpenClaw agents - auto-recall before turns, auto-capture after, tools for search/save/forget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewubundi](https://clawhub.ai/user/matthewubundi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to give agents long-term memory across sessions, including recall, explicit saves, lookup, forgetting, and Cortex setup or status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content and detailed technical decisions may be sent to Cortex and retained as cross-session memory.

Mitigation: Install only where this retention is acceptable; enable audit logging, disable autoCapture for sensitive projects, and use forget controls when stored memories should be removed.

Risk: The documented tools.profile full option grants broader tool access than the memory workflow needs.

Mitigation: Prefer the selective Cortex tool allowlist documented in the README and release security guidance.

Risk: Installing the plugin with @latest can pull behavior changes that have not been reviewed for this release.

Mitigation: Pin the Cortex plugin to a reviewed version before deployment.

Risk: The Cortex reset command is destructive.

Mitigation: Run openclaw cortex reset only after explicit confirmation in the current turn.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use Cortex memory tools and OpenClaw Cortex CLI commands when available; destructive reset requires explicit confirmation.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
