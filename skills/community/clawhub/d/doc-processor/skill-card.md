## Description: <br>
Doc Processor is a local document-processing skill for reading, writing, converting, merging, and extracting content from Word, Excel, PDF, CSV, text, and Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mo-yuhua](https://clawhub.ai/user/mo-yuhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to perform local document workflows such as content extraction, format conversion, templated document generation, and batch processing without relying on an external AI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user documents or templates outside the active workspace through template-history behavior. <br>
Mitigation: Avoid using generate or template-history features with confidential documents unless the user-templates directory is managed, reviewed, or deleted after use. <br>
Risk: The setup script installs Python dependencies from the configured pip index. <br>
Mitigation: Review requirements.txt and the selected pip index before running setup.sh, especially in controlled or commercial environments. <br>
Risk: System dependency installation may require privileged package-manager commands. <br>
Mitigation: Run apt, yum, or brew installation commands only from trusted system repositories after reviewing the requested packages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mo-yuhua/doc-processor) <br>
- [API Documentation](references/api-docs.md) <br>
- [Best Practices](references/best-practices.md) <br>
- [Security Notes](SECURITY.md) <br>
- [python-docx Documentation](https://python-docx.readthedocs.io/) <br>
- [openpyxl Documentation](https://openpyxl.readthedocs.io/) <br>
- [pandas Documentation](https://pandas.pydata.org/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, Python code examples, and generated local document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and may read, write, convert, merge, extract, or generate supported document formats.] <br>

## Skill Version(s): <br>
2.7.13 (source: frontmatter, release evidence, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
