## Description:

Generate Word (.docx) documents from Jinja2 templates using python-docx and Jinja2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation teams use this skill to create Word templates with Jinja2 tags, render .docx files from Python, JSON, or CSV data, and inspect missing template variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch rendering from CSV or TSV data can allow ID column values to influence output paths and write outside the intended output directory.

Mitigation: Use trusted data, inspect or constrain ID column values, avoid --overwrite with untrusted input, and run the scripts in a limited working directory or sandbox.

Risk: Unescaped template values containing XML-special characters can break rendering or produce unintended document content.

Mitigation: Use RichText, template escaping, escaped Python values, or the autoescape option when rendering untrusted or free-form text.

## Reference(s):

- [docxtpl documentation](https://docxtpl.readthedocs.io/en/latest/)
- [Official docxtpl Documentation Reference](references/official-docs.md)
- [ClawHub skill page](https://clawhub.ai/killgfat/skills/docxtpl)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate .docx files when the bundled scripts are run.]

## Skill Version(s):

0.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
