## Description:

A documentation skill set for generating README and project documentation, changelogs and release notes, API documentation, and PlantUML or Mermaid diagrams, with deterministic checks for Markdown links and code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create and maintain project documentation, release notes, API specifications, and technical diagrams. It also provides repeatable checks for Markdown links and code block labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API documentation may expose private API details when shared.

Mitigation: Review generated documentation and remove sensitive details before uploading or publishing it.

Risk: Setup examples use external tools, and the mmdc package shorthand can be ambiguous.

Mitigation: Review and pin external tools, avoid the ambiguous package shorthand, and choose deliberately between local and global installation.

Risk: Using `|| true` in rendering checks can let CI pass despite rendering errors.

Mitigation: Remove `|| true` when rendering errors must fail CI.

## Reference(s):

- [Documentation lifecycle and pipeline](references/doc-lifecycle-and-pipeline.md)
- [API documentation authoring playbook](references/api-doc-authoring-playbook.md)
- [Diagram selection guide](references/diagram-selection-guide.md)
- [Project documentation source skill](https://skills.sh/jezweb/claude-skills/project-docs)
- [Changelog writer source skill](https://skills.sh/patricio0312rev/skills/changelog-writer)
- [API documentation source skill](https://skills.sh/sickn33/antigravity-awesome-skills/api-documentation-generator)
- [Diagram source skill](https://skills.sh/markdown-viewer/skills/uml)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown documents, OpenAPI or Swagger specifications, PlantUML or Mermaid diagrams, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documentation should be reviewed for accuracy and sensitive details before sharing; included check scripts produce reports.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
