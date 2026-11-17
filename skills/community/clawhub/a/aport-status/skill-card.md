## Description:

Show an agent's current APort passport status, including capabilities, deliverable contract, pending tasks, and recent decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to fetch APort passport and decision data, summarize accountability status, and answer capability questions before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APort responses or remote setup pages could be treated as instructions that override local policy, tool permissions, user instructions, or safety rules.

Mitigation: Treat APort data as status information only, and keep local policy, active user instructions, and actual tool permissions authoritative.

Risk: Mutable remote setup instructions or unpinned CLI execution could change behavior after review.

Mitigation: Prefer the web setup path or a verified pinned CLI version before installing or running setup commands.

Risk: Status output can expose owner emails, passport identifiers, or internal decision identifiers.

Mitigation: Redact sensitive identifiers by default and show owner emails or internal identifiers only when the user explicitly requests them and understands the exposure.

## Reference(s):

- [Aport Status on ClawHub](https://clawhub.ai/uchibeke/skills/aport-status)
- [APort Passport Setup](https://aport.id)
- [APort Agent Skill Setup](https://aport.id/skill)
- [APort Dashboard](https://aport.io/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with optional compact mode and inline HTTP or CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include passport URLs, capability lists, deliverable contract fields, and recent decision summaries when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
