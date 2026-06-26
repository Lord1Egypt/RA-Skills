## Description: <br>
C-drive space analysis and cleanup skill for scanning Windows C-drive usage, identifying junk and large files, and helping the user run confirmed cleanup actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjflydudu](https://clawhub.ai/user/jjflydudu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and support agents use this skill to inspect C-drive storage pressure, identify temporary files, caches, large files, and migration candidates, and produce cleanup recommendations or commands after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect broad local folders and guide cleanup actions on Windows systems. <br>
Mitigation: Start with read-only or dry-run scanning, review every listed path and command, and proceed only after explicit user confirmation. <br>
Risk: Aggressive cleanup can cause irreversible removal of data or system state such as recycle bin contents, WSL distributions, Docker data, or shadow copies. <br>
Mitigation: Avoid aggressive cleanup unless the user explicitly intends those effects, and prefer the documented safe cleanup level for routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jjflydudu/c-cleaner) <br>
- [C-drive cleanup guide](references/cleanup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scan summaries, cleanup reports, path lists, and user-confirmed cleanup recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
