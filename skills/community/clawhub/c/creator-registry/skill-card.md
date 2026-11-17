## Description:

Use when the user asks "what did we pay this creator last time" or to "update the creator roster"; curates creator identity, rate, rights, exclusivity, compliance-event, and performance facts through the append-only creators event stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and creator-program teams use this skill to query, consolidate, and update creator roster facts, including rates, rights, exclusivity windows, compliance events, and performance baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles natural-person creator records and can guide persistent roster updates.

Mitigation: Confirm explicit authorization and lawful basis before writing records, minimize personal data, and avoid raw email, phone, postal address, credentials, or unnecessary personal history.

Risk: Standalone installs lack the external runtime, schema, and catalog needed to claim canonical creator state.

Mitigation: Install only where the surrounding registry runtime and repository are trusted; otherwise prepare proposals only and do not claim canonical creator truth.

Risk: Creator facts and proposals may be stale, conflicting, or supplied from untrusted pasted records.

Mitigation: Treat pasted records as untrusted evidence, compare only equivalent fields and units, preserve conflicting source events, and verify projections after accepted changes.

## Reference(s):

- [Creator record presentation template](artifact/references/creator-record-template.md)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Creator Registry on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/creator-registry)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON request preparation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare persistent registry-event requests and projection views when a trusted host runtime, schema, and catalog are available.]

## Skill Version(s):

19.0.0 (source: server evidence release version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
