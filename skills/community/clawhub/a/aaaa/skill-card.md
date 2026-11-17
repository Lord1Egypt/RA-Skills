## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, corrections, missing capabilities, and reusable workflow lessons in local markdown logs. The skill also guides review and promotion of high-value learnings into project or agent memory files after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records conversation-derived guidance and may promote it into future agent instructions with weak scoping and review safeguards.

Mitigation: Keep learning logs project-scoped, avoid global hooks, and require human review before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, Copilot instructions, or similar agent context files.

Risk: Learning logs can capture sensitive context if agents store raw transcripts, credentials, or private operational details.

Mitigation: Do not store secrets or raw transcripts in .learnings, and redact sensitive details before retaining or promoting entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gakkiismywife/skills/aaaa)
- [Publisher profile](https://clawhub.ai/user/gakkiismywife)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and template examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs and propose promotion of selected learnings into agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
