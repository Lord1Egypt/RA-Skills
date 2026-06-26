## Description: <br>
Batch converts Office documents and PDFs into Markdown while preserving directory structure and recording conversion failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byteuser1977](https://clawhub.ai/user/byteuser1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge-base maintainers, and operations teams use this skill to convert legacy Office, modern Office, and PDF document collections into searchable Markdown. It is suited to local archive migration and document-library normalization where source folders and output folders can be scoped deliberately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk conversion can process sensitive or untrusted documents through local conversion tools. <br>
Mitigation: Use a narrow source folder, write to a private output folder, and sandbox conversion when files come from untrusted people or locations. <br>
Risk: A broad source path or cleanup operation can affect more files than intended. <br>
Mitigation: Run with --dry-run first, review matched files and paths, and avoid copying cleanup commands unless the target directory has been verified. <br>
Risk: External conversion dependencies affect both security posture and output quality. <br>
Mitigation: Install LibreOffice and markitdown from trusted sources and avoid administrator or root privileges unless they are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byteuser1977/document-organizer) <br>
- [Reference index](references/INDEX.md) <br>
- [API reference](references/API_REFERENCE.md) <br>
- [Supported formats](references/FORMATS.md) <br>
- [Configuration guide](references/CONFIGURATION.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [LibreOffice](https://zh-cn.libreoffice.org/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with terminal status output and optional conversion logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves the source directory structure in the output folder and writes failed conversions to a configurable log file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
