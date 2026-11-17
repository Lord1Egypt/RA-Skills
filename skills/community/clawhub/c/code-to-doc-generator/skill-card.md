## Description:

Generates or synchronizes project documentation by reverse-extracting business logic from code and UI, with templates for BRD/MRD, PRD, HLD, DDD, LLD, coding guides, test documentation, operations manuals, SLI/SLO monitoring documents, and CI/CD documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suifei](https://clawhub.ai/user/suifei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, product managers, QA engineers, SREs, DevOps engineers, and operations teams use this skill to create or refresh project documentation from an implementation source of truth. It is especially useful when documentation has drifted from code or when a project needs structured delivery documents for different software lifecycle audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository code and project documentation to generate or synchronize documentation, which may expose sensitive implementation details to the active agent session.

Mitigation: Install and run it only in repositories where that level of code and documentation access is acceptable.

Risk: Generated documentation can contain incorrect inferences or stale observations if the implementation is ambiguous.

Mitigation: Review generated documents before committing them, especially OBSERVATIONS.md and content marked with inference or observation labels.

Risk: The artifact includes an SVG with clickable prompt actions.

Mitigation: Avoid opening the SVG in environments where clickable prompt actions can run unless those prompt suggestions are intended.

## Reference(s):

- [Analysis Dimensions](references/analysis-dimensions.md)
- [Document Structure](references/document-structure.md)
- [Document Types](references/document-types.md)
- [Exploration Strategy](references/exploration-strategy.md)
- [Reverse Sync](references/reverse-sync.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with tables, Mermaid diagrams, command snippets, and inline fact or inference markers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create new documentation under docs/ or update existing documentation during reverse sync; generated material should be reviewed before commit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
