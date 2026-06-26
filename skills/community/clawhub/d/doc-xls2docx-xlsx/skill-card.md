## Description: <br>
Batch converts legacy Microsoft Office .doc and .xls files to modern .docx and .xlsx formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longjf25](https://clawhub.ai/user/longjf25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert individual files or batches of legacy Office documents into current Office formats. It is intended for local conversion workflows where the user controls the source files and output locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch conversion can replace existing .docx or .xlsx outputs. <br>
Mitigation: Run the skill on copies or backed-up folders and prefer a separate output directory. <br>
Risk: Word opens .doc files during conversion, which increases risk when documents are untrusted. <br>
Mitigation: Avoid converting untrusted Office documents on sensitive machines; use an isolated environment for higher-risk files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longjf25/doc-xls2docx-xlsx) <br>
- [Publisher profile](https://clawhub.ai/user/longjf25) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with command examples and generated .docx or .xlsx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversion runs locally on user-specified files or directories; .doc conversion requires Windows with Microsoft Word installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
