## Description:

Captures learnings, errors, corrections, feature requests, and reusable practices so coding agents can improve future prompt context and workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1215656](https://clawhub.ai/user/1215656)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, knowledge gaps, and reusable best practices in structured learning files, then promote durable guidance into agent memory or instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently writes and promotes agent learnings into future prompt context.

Mitigation: Require human review and redaction before promoting entries from .learnings into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Broad hook triggers can inject reminders into many agent sessions.

Mitigation: Use project-local configuration, avoid global hooks unless necessary, and restrict hook matchers instead of running them on every prompt.

Risk: Learning logs may capture sensitive or incorrect context if copied directly from conversations or tool output.

Mitigation: Review entries before reuse, remove secrets or personal data, and keep promoted guidance concise and source-appropriate.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and structured learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local learning and agent memory files when the user or host agent chooses to apply the guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact metadata version 3.0.6

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
