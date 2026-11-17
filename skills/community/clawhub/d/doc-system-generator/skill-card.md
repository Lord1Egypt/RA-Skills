## Description:

Analyzes software projects and generates structured Markdown documentation systems using Intent, Contract, and Constraint tracks, intelligent grouping, template derivation, and completeness self-checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create or redesign repository documentation systems, including project analysis, document grouping, Markdown templates, entry files, and completeness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist future agent-reading rules in generated entry files, including strong prohibition language.

Mitigation: Review generated AGENTS.md or equivalent files before accepting them, and remove or soften highest-priority prohibition language that conflicts with local governance.

Risk: The bundled md-sections.sh helper has a confirmed command-execution flaw when automation passes untrusted --line values.

Mitigation: Harden or replace md-sections.sh before using it with untrusted inputs, and require approval before copying it into scripts/.

Risk: Repository-wide documentation generation may create or modify central documentation and helper-script locations.

Mitigation: Run the skill in a reviewable working tree and require approval before modifying AGENTS.md, docs/, or scripts/.

## Reference(s):

- [Doc System Generator on ClawHub](https://clawhub.ai/leonardo-lb/skills/doc-system-generator)
- [Grouping Detection](references/grouping-detection.md)
- [Template Derivation](references/template-derivation.md)
- [Three-Track Philosophy](references/three-track-philosophy.md)
- [Completeness Checklist](references/completeness-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, JSON project profiles, self-check reports, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates repository documentation structure and can copy a Markdown section helper script into a target project's scripts directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
