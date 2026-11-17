## Description:

Triage and persist work outside the explicit active objective when a message contains multiple requests, an item is unrelated or deferred, the user asks to remember, track, log, or handle something later, or invokes dev-inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to separate active work from deferred or unrelated items, classify those items, and persist them to a discoverable follow-up destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session content may be saved or published to GitHub issues, agent memory, or TODO.md without enough destination-specific confirmation.

Mitigation: Review the workflow before installing and add explicit confirmation for durable or remote writes where required.

Risk: Secrets, customer data, private vulnerability details, or sensitive internal plans could be persisted if they appear in deferred work items.

Mitigation: Avoid using the skill with sensitive content unless the workflow is modified to require redaction before records are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/dev-inbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with record templates, optional shell commands, and concise confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update GitHub issues, agent memory entries, or TODO.md records depending on the available environment.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
