## Description:

Pre-production assistant for filmmakers that generates script breakdowns, shot lists, call sheets, production schedules, and budget estimates from scene descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidapx13](https://clawhub.ai/user/davidapx13)

### License/Terms of Use:

MIT-0

## Use Case:

External filmmakers, assistant directors, producers, and production teams use this skill to turn scene or project details into pre-production documents such as breakdown sheets, shot lists, call sheets, schedules, and budget estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional DOCX export instructions include unsafe shell command patterns.

Mitigation: Use safer export tooling that avoids shell interpolation, uses unique temporary files, and only exports when the user explicitly requests a file.

Risk: Generated call sheets can contain confidential phone numbers, addresses, access instructions, transport details, and safety-sensitive notes.

Mitigation: Treat call sheets as confidential production documents, redact unnecessary personal details, and distribute them only to authorized cast and crew.

## Reference(s):

- [Script Breakdown Structure Reference](references/script-breakdown-structure.md)
- [Shot List Structure Reference](references/shot-list-structure.md)
- [Call Sheet Structure Reference](references/call-sheet-structure.md)
- [Production Schedule Structure Reference](references/production-schedule-structure.md)
- [Film Budget Structure Reference](references/budget-structure.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown production documents with optional pandoc-based .docx export when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional document export requires pandoc; call sheets may include confidential cast, crew, location, transport, and safety details.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
