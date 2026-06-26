## Description: <br>
Helps agents edit Word (.docx) files by enabling track changes, adding insertion and deletion revisions, and adding, removing, or viewing comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HanselXie](https://clawhub.ai/user/HanselXie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when a user asks to revise Word documents, add redline edits, or manage comments in .docx files. It supports both scripted edits and XML-level guidance for local document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Word documents can be changed or overwritten during scripted or manual editing. <br>
Mitigation: Work on copies or explicit output files, and review the generated document before sharing it. <br>
Risk: Manual cleanup commands can remove the wrong temporary directory if run from an unexpected location. <br>
Mitigation: Verify the current directory and target path before running cleanup commands such as rm -rf. <br>
Risk: The helper script depends on python-docx when used for scripted edits. <br>
Mitigation: Install python-docx only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HanselXie/docx-trackchanges-and-comments) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown with inline bash, Python, and XML snippets; local .docx files when the script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works on local Word documents and may create or overwrite output .docx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
