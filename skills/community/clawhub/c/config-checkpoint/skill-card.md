## Description: <br>
Creates Git checkpoints and guides rollbacks for OpenClaw configuration changes while requiring checks for ignored and sensitive files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welkeyever](https://clawhub.ai/user/welkeyever) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create Git checkpoints before configuration changes and to choose safer rollback commands when recovery is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A hard reset can permanently discard uncommitted OpenClaw configuration changes. <br>
Mitigation: Prefer soft or mixed reset options and require explicit confirmation after showing the changes that would be lost. <br>
Risk: A checkpoint could accidentally include credentials or other sensitive local files. <br>
Mitigation: Verify .gitignore, scan modified and untracked paths for sensitive filenames, and prefer targeted git add commands before committing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended to be reviewed before execution, especially rollback operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
