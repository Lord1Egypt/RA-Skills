## Description: <br>
Batch desensitize docx/xlsx files via keyword and regex rules, with one-click reversible restoration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longjf25](https://clawhub.ai/user/longjf25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and document-processing teams can use this skill to sanitize Word and Excel workspaces with exact-match and regex rules, then restore content and filenames from the generated mapping record when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reversible _sanitize_record.json file can reveal original sensitive text and filenames. <br>
Mitigation: Keep the record private, do not distribute it with sanitized outputs, and delete it when restoration is no longer required. <br>
Risk: Legacy .doc/.xls conversion relies on a separate converter skill and may process untrusted Office files. <br>
Mitigation: Use --auto-convert only after trusting the converter dependency and preferably in an isolated workspace with trusted documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longjf25/document-sanitizer) <br>
- [Publisher profile](https://clawhub.ai/user/longjf25) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sanitized and restored document files, plus a reversible _sanitize_record.json mapping file in the target workspace.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
