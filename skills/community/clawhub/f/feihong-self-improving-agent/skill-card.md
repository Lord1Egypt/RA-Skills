## Description:

Captures agent learnings, command errors, user corrections, and feature requests in markdown logs for later review, promotion, or skill extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyue1977](https://clawhub.ai/user/sunyue1977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record errors, corrections, knowledge gaps, and feature requests so future sessions can reuse the learning. It also provides optional hook guidance and a helper script for extracting durable learnings into reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can retain conversation details, errors, and corrections longer than intended.

Mitigation: Keep .learnings local by default and redact secrets, personal data, and business-sensitive details before logging.

Risk: Promoting unreviewed learnings into agent instruction files can introduce incorrect or misleading guidance.

Mitigation: Require explicit human approval before promoting any learning into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Broad or global hook activation can create unwanted persistent memory behavior.

Mitigation: Use minimal, project-scoped hooks unless the scripts and configuration have been fully reviewed and trusted.

## Reference(s):

- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to create or update persistent .learnings markdown files and optional skill scaffolds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
