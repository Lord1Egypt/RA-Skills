## Description:

Captures learnings, errors, and corrections to enable continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record corrections, command failures, knowledge gaps, and recurring improvements as structured markdown logs that can later be promoted into project or agent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently record conversation-derived learnings and promote them into future agent context, which may capture private or incorrect information.

Mitigation: Redact secrets and private data before logging, keep learning files local or intentionally reviewed, and require human review before promoting entries into persistent agent instruction files.

Risk: Broad hook examples may add reminders across more sessions than intended.

Mitigation: Keep hooks project-local, avoid global always-on settings, and use restrictive matchers or explicit enablement for the contexts where the workflow is desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cs995279497-byte/skills/chen-self-improvement)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, templates, and optional hook or script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning logs and promotion guidance; optional hooks inject reminders into agent context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
