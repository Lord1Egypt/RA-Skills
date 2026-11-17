## Description:

A Chinese-language workflow for proposing newborn or adult Chinese names using Bazi, Wuxing, name-study numerology, taboo-character checks, candidate generation, and Word-document reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruokkkkk](https://clawhub.ai/user/ruokkkkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to collect birth and naming preferences, apply traditional Chinese naming analysis, compare candidate names, and prepare structured content for a formatted naming proposal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill can automatically install a Python package.

Mitigation: Review and install dependencies explicitly in an isolated environment before running the document-generation script.

Risk: The release evidence reports that the skill writes Word files using user-controlled names.

Mitigation: Provide an explicit safe output path and review generated filenames before creating documents.

Risk: The workflow may place precise birth and family details into generated local files.

Mitigation: Avoid sharing sensitive birth or family details unless the user is comfortable with those details being included in local artifacts.

## Reference(s):

- [Bazi and Wuxing Reference](references/bazi-wuxing.md)
- [Name-Study Numerology Reference](references/name-study.md)
- [Output Template and JSON Schema](references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/ruokkkkk/skills/chinese-name-craft)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance, files]

**Output Format:** [Conversational analysis and structured JSON that can be rendered into a .docx Word document.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a local Word document through the bundled Python script when provided a valid naming-analysis JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
