## Description:

Routes user requests for ACP or external coding agents such as Codex, Claude Code, Gemini CLI, and OpenCode into non-blocking OpenClaw background ACP runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambition0802](https://clawhub.ai/user/ambition0802)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-assistant users use this skill to delegate ACP, Codex, Claude Code, Gemini CLI, or OpenCode work to background runs while keeping the current conversation available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A background run may act on the wrong project if the cwd or target agent is selected incorrectly.

Mitigation: Confirm the intended repository path and requested external agent before submitting the background run.

Risk: Falling back from ACP to another runtime could change how the delegated work is executed.

Mitigation: Use ACP when available and tell the user explicitly before using a subagent fallback.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown guidance with JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Background runs are submitted asynchronously and are expected to report results through completion notifications.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
