## Description: <br>
This skill helps agents clear, remove, or clean up AI agent rules, skills, and instruction files across major AI coding platforms on Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subingshe](https://clawhub.ai/user/subingshe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify and remove AI-agent rule or skill files from project-level and user-global locations, with backup, preview, platform filtering, and scope controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can delete broad AI-tool configuration directories, not only narrow rule or skill files. <br>
Mitigation: Run with --dry-run first, prefer --mode project or a narrow --platforms list, and keep backups enabled. <br>
Risk: Non-interactive or no-backup runs can make unintended removals harder to notice or recover from. <br>
Mitigation: Avoid --yes and --no-backup unless every listed path has been reviewed and recovery is not required. <br>


## Reference(s): <br>
- [AI Agent Rule/Skill File Path Reference](references/platforms.md) <br>
- [ClawHub skill page](https://clawhub.ai/subingshe/clear-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Python cleanup script that scans, backs up, and deletes selected AI-agent rule files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
