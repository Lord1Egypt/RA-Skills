## Description: <br>
Removes invalid characters and normalizes filenames for safe, cross-platform use in files and directories, with optional recursive cleaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to clean unsafe or invalid filenames in individual files or directories before sharing, syncing, scripting, or cross-platform use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Renaming files in important, shared, or project folders can disrupt links, scripts, imports, or workflows that depend on exact filenames. <br>
Mitigation: Run with --dry-run first and review the proposed filename changes before applying them. <br>
Risk: Recursive cleaning can apply filename changes across many nested files at once. <br>
Mitigation: Use --recursive only after narrowing the target path and confirming the expected scope. <br>


## Reference(s): <br>
- [ClawHub Clean Filename listing](https://clawhub.ai/albionaiinc-del/clean-filename) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run and recursive filename-cleaning commands; the bundled tool can rename local files selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
