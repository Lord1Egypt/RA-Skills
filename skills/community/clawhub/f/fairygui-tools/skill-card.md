## Description:

Helps agents analyze FairyGUI projects and UI screenshots, create HTML/CSS mockup screenshots, generate importable FairyGUI graybox XML packages, and validate generated XML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slinkz](https://clawhub.ai/user/slinkz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical UI designers use this skill to analyze FairyGUI UI structures, produce prototype visuals, generate complete FairyGUI graybox XML packages, and validate package/component XML before editor import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated XML or prototype files may be written to local project paths and may not match production UI expectations without review.

Mitigation: Review generated XML and local files before importing them into production FairyGUI projects.

Risk: The workflow can run a local validator or screenshot tool on paths supplied by the user.

Mitigation: Run validation and screenshot steps only on intended local directories and inspect outputs before use.

## Reference(s):

- [FairyGUI XML Specification](references/fairygui-xml-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML/CSS, XML, and shell command snippets; may also produce local files for mockups and FairyGUI packages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local review and validation before importing generated XML into FairyGUI projects.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
