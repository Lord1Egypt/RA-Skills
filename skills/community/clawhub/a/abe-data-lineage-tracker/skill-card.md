## Description:

Track data origin, transformations, and flow through construction systems for audit trails, compliance, and debugging data issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Construction data teams, developers, and auditors use this skill to register data sources and entities, record transformations, trace upstream and downstream lineage, validate lineage consistency, and produce audit-oriented lineage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lineage exports or analysis prompts may include project names, owner names, internal system names, file locations, or transformation details sent to a third-party AI API.

Mitigation: Use local lineage functions by default, send only sanitized data to SkillBoss API Hub after explicit approval, and avoid submitting confidential, regulated, or client-restricted construction data.

Risk: The security verdict is suspicious because remote AI analysis is not scoped with enough redaction or user-confirmation guidance.

Mitigation: Review the skill before installation in confidential or regulated environments and add deployment-specific approval, redaction, and data-minimization controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/abe-data-lineage-tracker)
- [Data Driven Construction homepage](https://datadrivenconstruction.io)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, structured tables, Mermaid diagrams, JSON-style exports, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SKILLBOSS_API_KEY for AI-assisted analysis through SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
