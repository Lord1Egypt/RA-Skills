## Description: <br>
Shared OpenClaw skill for guiding ClawMover backup and restore workflows with explicit confirmation, input validation, and a manual-command-first execution policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tubo70](https://clawhub.ai/user/tubo70) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and guide OpenClaw backup, simulated restore, and restore workflows through ClawMover. It emphasizes explicit confirmation, input validation, sensitive-data handling, and manual command review before environment-changing operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install, backup, restore, and migration commands can change the host environment or live OpenClaw state. <br>
Mitigation: Review commands before execution, require explicit confirmation, and prefer simulated restores or dry-run style checks before real restores. <br>
Risk: Migration identifiers, verification codes, local paths, and dataSecretKey values may expose sensitive information. <br>
Mitigation: Validate inputs, mask sensitive values in displayed commands, and avoid logging or repeating full secrets. <br>
Risk: ClawMover migrations may involve a purchase or paid service flow. <br>
Mitigation: Confirm the user has intentionally created the migration on ClawMover before using the resulting migration identifier. <br>


## Reference(s): <br>
- [ClawMover](https://clawmover.com) <br>
- [OpenClaw Migration ClawHub Page](https://clawhub.ai/tubo70/clawmover-migration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked sensitive values and confirmation prompts before installs, backups, or restores.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
