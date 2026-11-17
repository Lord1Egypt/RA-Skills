## Description:

Lightweight self-improvement loop for AI agents that captures errors, corrections, and discoveries in local one-line logs, deduplicates them, queues recurring or critical lessons for human-approved promotion, and reviews relevant learnings before major work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents a lightweight workspace-local memory loop for recording mistakes, corrections, requested capabilities, and reusable lessons without automatically modifying instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning notes may preserve workspace observations longer than intended.

Mitigation: Install only in workspaces where local learning notes are desired and review `.learnings/` periodically.

Risk: Logged entries could be mistaken for higher-priority agent instructions.

Mitigation: Do not let logged entries override system, developer, security, or current-user instructions.

Risk: External content could become unsafe guidance if treated as promotable learning.

Mitigation: Keep external content labeled as `source:external`; the artifact blocks external-source entries from promotion and requires human review for promotions.

## Reference(s):

- [Agent Memory Loop on ClawHub](https://clawhub.ai/zurbrick/skills/agent-memory-loop)
- [ClawHub homepage metadata](https://clawhub.ai/agent-memory-loop)
- [Logging Format Reference](references/logging-format.md)
- [Operating Rules Reference](references/operating-rules.md)
- [Promotion Queue Format Reference](references/promotion-queue-format.md)
- [Detail File Template](references/detail-template.md)
- [Design Tradeoffs](references/design-tradeoffs.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reviews local .learnings/ Markdown files; evidence.security reports no network access, credential use, hidden execution, or automatic promotion into instruction files.]

## Skill Version(s):

2.1.1 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
