## Description: <br>
Convert Word documents (.docx) to PDF format while preserving embedded images, formatting, and document structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmed181283](https://clawhub.ai/user/ahmed181283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document-processing users can use this skill to choose a local conversion method, install required tools, and convert single or multiple DOCX files to PDF while preserving images, tables, and layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill suggests installing local tools and Python packages such as LibreOffice, Pandoc, python-docx, reportlab, pillow, and docx2pdf. <br>
Mitigation: Install software only from trusted sources, prefer a Python virtual environment for packages, and review commands before running them. <br>
Risk: Batch conversion can overwrite or misplace outputs if run in a broad working directory. <br>
Mitigation: Run batch conversion in a dedicated folder, set an explicit output directory, and verify generated PDFs before deleting original Word files. <br>
Risk: Converted PDFs may lose fidelity for complex macros, custom fonts, very large files, or advanced Word features. <br>
Mitigation: Test on a sample document first, make sure required fonts are installed, and compare the output PDF against the source document before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ahmed181283/docx-to-pdf) <br>
- [LibreOffice Command Reference](references/libreoffice-reference.md) <br>
- [Python docx2pdf Documentation](references/python-docx2pdf.md) <br>
- [Common Conversion Issues](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local conversion commands, setup options, batch-processing examples, troubleshooting steps, and quality checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
