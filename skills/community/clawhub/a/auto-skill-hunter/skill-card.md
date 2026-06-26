## Description: <br>
Automatically discovers and installs high-value skills from ClawHub based on unresolved issues, user profile, and skill compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to discover, rank, preview, and optionally install ClawHub skills that address unresolved tasks or capability gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read prior user context and profile signals. <br>
Mitigation: Run it only in environments where that context is approved for skill discovery. <br>
Risk: The skill can install, clone, scaffold, and self-test new skills. <br>
Mitigation: Start with --dry-run, keep --max-install low, and manually review recommended skill source before live installs. <br>
Risk: The skill can send recommendation reports outside the workspace. <br>
Mitigation: Set SKILL_HUNTER_NO_REPORT=1 unless external reporting has been explicitly approved. <br>
Risk: Scheduled auto patrol can repeatedly change the skill stack in shared or sensitive environments. <br>
Mitigation: Avoid cron scheduling in those environments or require human approval for each live install. <br>


## Reference(s): <br>
- [Auto Skill Hunter - ClawHub](https://clawhub.ai/wanng-ide/auto-skill-hunter) <br>
- [Memory Mesh Core - ClawHub](https://clawhub.ai/wanng-ide/memory-mesh-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendation report with install status, selection reasons, and optional generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May clone or scaffold selected skills and run self-tests unless --dry-run is used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
