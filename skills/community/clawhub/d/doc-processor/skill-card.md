## Description:

Doc Processor helps agents handle local document workflows for Word, Excel, PDF, CSV, text, and Markdown files, including reading, writing, converting, merging, extracting data, and filling templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mo-yuhua](https://clawhub.ai/user/mo-yuhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate local document processing tasks such as inspecting document metadata, extracting content, converting between supported formats, merging files, generating Word or Excel outputs, and filling document templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, overwrite, convert, and merge local documents.

Mitigation: Review target paths before running file-writing commands and use a working copy or backed-up documents for conversion and merge operations.

Risk: Template learning and generation behavior can persist document-derived templates under a user-templates directory.

Mitigation: Avoid using confidential documents with generation or template-learning APIs unless persistent local template copies are acceptable.

Risk: Optional PDF generation backends have noted HTML escaping and temporary-file handling concerns.

Mitigation: Avoid optional PDF generation backends until those issues are fixed, or use trusted content and inspect generated files before sharing.

Risk: The setup script installs Python dependencies and supports custom package indexes.

Mitigation: Review setup.sh before running it, use trusted package indexes, and confirm any system package installation commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mo-yuhua/skills/doc-processor)
- [Release Notes v2.7.13](artifact/RELEASE-v2.7.13.md)
- [Security Notes](artifact/SECURITY.md)
- [API Documentation](artifact/references/api-docs.md)
- [Best Practices](artifact/references/best-practices.md)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [pandas Documentation](https://pandas.pydata.org/docs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples, Python API examples, and generated or transformed local document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, overwrite, convert, merge, extract, cache, and template local files in the configured workspace.]

## Skill Version(s):

2.7.13 (source: SKILL.md frontmatter, release evidence, _meta.json, RELEASE-v2.7.13.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
