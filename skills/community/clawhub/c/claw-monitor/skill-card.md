## Description:

Use the `clawmonitor` CLI/TUI to inspect OpenClaw sessions, model health, token usage, and gateway service health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawq](https://clawhub.ai/user/openclawq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw session state, troubleshoot delivery or feedback issues, check model/provider health, review token usage windows, and decide when to export reports or nudge a running session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running `clawmonitor` reads local OpenClaw session state and depends on a trusted package source.

Mitigation: Install it only from a trusted source, preferably in an isolated environment, and run it on the host where OpenClaw state is expected.

Risk: The `nudge` command sends a progress request into a running session.

Mitigation: Use `nudge` only when the user intends to prompt that specific session for progress.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawq/skills/claw-monitor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended `clawmonitor` CLI commands, status summaries, report guidance, and caution around active session nudges.]

## Skill Version(s):

0.1.3 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
