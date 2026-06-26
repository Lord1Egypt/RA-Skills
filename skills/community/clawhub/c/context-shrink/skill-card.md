## Description: <br>
Auto-compress session memories when context usage exceeds 85%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this hook to reduce long-running workspace context by compressing older daily memory logs into MEMORY.md when usage crosses the configured threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook may automatically rewrite long-term memory and delete older memory logs. <br>
Mitigation: Review the release before installing, keep recoverable backups or Git history, and prefer deployments that require explicit approval before deletion. <br>
Risk: The hook may create broad Git commits after memory cleanup. <br>
Mitigation: Run it only in trusted workspaces and prefer a version that stages only known memory files before committing. <br>
Risk: The security review reports inconsistent disclosure and recommends caution before installation. <br>
Mitigation: Confirm the documented threshold, event behavior, and cleanup policy match the installed handler before enabling the hook. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/context-shrink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Plain-text hook status messages with Markdown memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, delete older daily memory logs, and create local Git commits when triggered.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
