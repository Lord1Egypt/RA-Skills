## Description:

Helps convert Markdown, plain text, HTML, RTF, LaTeX, reStructuredText, and Org-mode documents to Word files using a user-provided reference.docx style template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing Word documents use this skill to convert individual files or batches on Windows while applying their own reference.docx styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local PowerShell converter and depends on a separately installed Pandoc executable.

Mitigation: Review the bundled scripts before execution and install Pandoc from its official source.

Risk: Conversion processes local documents and saves Pandoc and template paths in config.ini.

Mitigation: Convert only documents you intend to process and check the saved paths before sharing the configuration.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zd200572/skills/docx-convert)
- [Pandoc installation](https://pandoc.org/installing.html)
- [Configuration guide](references/config.md)
- [Reference template guide](references/make-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local conversion produces .docx files styled with a user-provided reference.docx; existing outputs are skipped.]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
