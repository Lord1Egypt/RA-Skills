## Description:

Records AI failures and misoperations in a local JSONL incident ledger and summarizes incidents for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and incident responders use this skill to record AI errors, affected models, and response actions in a local ledger, then review entries or generate summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident records may contain sensitive details.

Mitigation: Choose an approved ledger location and avoid secrets or raw breach evidence unless that location is approved.

Risk: Declared permissions understate the local file access and CLI execution this skill requires.

Mitigation: Review the permissions and local execution needs before installation in a security or compliance workflow.

Risk: Documented recording flags differ from the script's accepted arguments.

Mitigation: Check the script's --help output and use --add with a numeric severity from 1 to 3 before relying on incident capture.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-incident-log)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, JSON, Files]

**Output Format:** [CLI text or JSON summary and local JSONL incident ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records include time, severity, model, incident description, action, and owner; reports count incidents by severity and model.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; included skill frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
