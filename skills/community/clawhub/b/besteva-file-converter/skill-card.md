## Description: <br>
This skill provides file format conversion capabilities for PDF to Word, Word to PDF, image format conversion, and Excel/CSV conversion, with support for single-file and batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besteva77](https://clawhub.ai/user/besteva77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to convert documents, images, and spreadsheets between common formats, including batch conversions when many files need the same treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-named source files and writes converted copies to disk. <br>
Mitigation: Specify exact input files, output formats, destination folders, and overwrite behavior before running conversions. <br>
Risk: Batch conversions can process many files and may place sensitive outputs together with unrelated files. <br>
Mitigation: Use a separate output folder for sensitive or batch conversions and review the reported file paths after completion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/besteva77/besteva-file-converter) <br>
- [Publisher Profile](https://clawhub.ai/user/besteva77) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands and converted local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create one converted file or multiple converted files during batch operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
