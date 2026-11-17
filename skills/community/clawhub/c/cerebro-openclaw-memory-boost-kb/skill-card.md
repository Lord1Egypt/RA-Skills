## Description:

Enforce a Cerebro-first operating protocol for continuity across sessions by requiring domain identification, authoritative document review, cited decision basis, and durable write-backs before operational action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ptaramona](https://clawhub.ai/user/ptaramona)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and project teams use this skill to make agents read project knowledge first, route work to the right domain, preserve continuity across sessions, and record decisions or process changes in durable Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Cerebro documents can control future agent behavior.

Mitigation: Keep Cerebro files in a trusted workspace and review proposed authoritative-rule changes before relying on them.

Risk: The skill may create or update memory or policy documents during execution.

Mitigation: Require explicit user approval and exact file diffs before creating or modifying authoritative documents or daily memory.

Risk: Private project domains can be routed into shared workflows if domain handling is unclear.

Mitigation: Use the domain-routing reference and keep private-context details in private owner or admin channels.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ptaramona/skills/cerebro-openclaw-memory-boost-kb)
- [Cerebro Index v2.1](references/cerebro-index-v2.1.md)
- [Domain Routing v2.1](references/domain-routing-v2.1.md)
- [Scenario Profiles v2.1](references/scenario-profiles-v2.1.md)
- [Enforcement Checklist v2.1](references/enforcement-checklist-v2.1.md)
- [Done Schema v2.1](references/done-schema-v2.1.md)
- [Startup Checklist](references/startup-checklist.md)
- [Decision Log Template](references/decision-log-template.md)
- [Missing Doc Bootstrap Template](references/missing-doc-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with source-of-truth paths, decision basis, write-back status, checklists, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update durable Markdown knowledge and memory files when the user approves authoritative changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact docs describe Cerebro protocol version 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
