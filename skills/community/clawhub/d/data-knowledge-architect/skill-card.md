## Description:

Builds semantic models from API, CLI, and database contracts with an HTML review and OKF/YAML export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data architects use this skill to turn supplied API, CLI, or database contracts into evidence-backed semantic models, review modeling decisions, and export approved models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied contracts or schemas may contain sensitive information.

Mitigation: Provide only the contracts and schemas needed for the modeling task.

Risk: Generated models may misstate grain, measures, or source relationships.

Mitigation: Review and approve decisions, then inspect the exported files before relying on them.

## Reference(s):

- [Skill homepage (listed in release metadata)](https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/data-knowledge-architect)
- [Ingest workflow](references/ingest.md)
- [Decision review workflow](references/review.md)
- [OKF export guidance](references/emit-okf.md)
- [YAML export guidance](references/emit-yaml.md)
- [Verification guidance](references/verify.md)

## Skill Output:

**Output Type(s):** [HTML, Markdown, YAML]

**Output Format:** [HTML decision review and approved OKF Markdown bundle or repository YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports require user approval and include evidence citations and verification checks.]

## Skill Version(s):

1.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
