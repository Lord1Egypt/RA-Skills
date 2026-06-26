## Description: <br>
Claw Config helps OpenClaw agents identify their own configuration scope, inspect schema and docs, diagnose setup issues, and plan or apply scoped configuration changes without guessing field names or paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhili1004](https://clawhub.ai/user/zhili1004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw agents use this skill to inspect an agent's own OpenClaw configuration, diagnose setup problems, and make schema-validated configuration changes after reviewing a dry-run plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents persistent power to change OpenClaw configuration. <br>
Mitigation: Require a human-reviewed plan diff before apply, and use apply only for intentional operator-approved changes. <br>
Risk: Shared configuration changes can affect more than the calling agent. <br>
Mitigation: Do not allow --force-shared except under direct operator control. <br>
Risk: Documentation lookups can be stale or unsafe if pointed away from OpenClaw documentation. <br>
Mitigation: Use the docs command for OpenClaw documentation and avoid non-OpenClaw URLs. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text or JSON command output, with markdown reports where supported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can change local OpenClaw configuration; apply is intended to follow a reviewed dry-run plan and is blocked in cron context.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
