## Description:

AI Harness Engineering records verified OpenClaw errors, learnings, and feature requests in ledgers, then supports review, summary injection, and optional promotion workflows to help avoid repeated mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to track verified mistakes, learning items, and feature requests, query them during future work, and generate summaries or reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived content and later write it into files that shape future agent behavior.

Mitigation: Require explicit confirmation before recording or promoting entries, and inspect proposed changes to SOUL.md, AGENTS.md, TOOLS.md, and MEMORY.md before enabling promotion workflows.

Risk: Recorded ledgers may contain private conversation content or secrets because redaction is not enforced.

Mitigation: Avoid recording secrets or private content, and review ledger entries before sharing reports or enabling always-on use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moniq888/skills/ai-harness-engineering)
- [Package documentation](artifact/PACKAGE.md)
- [Error patterns reference](artifact/references/error_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands, plus JSON/JSONL ledger and report files from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist conversation-derived error, learning, and feature records and may update workspace guidance files when promotion workflows are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
