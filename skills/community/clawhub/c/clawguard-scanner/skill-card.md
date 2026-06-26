## Description: <br>
Security scanner for OpenClaw skills that helps agents check for prompt injection, data exfiltration, permission overreach, suspicious URLs, dangerous commands, and metadata mismatches before installation or use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Frrrrrrrrank](https://clawhub.ai/user/Frrrrrrrrank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan third-party OpenClaw skills before installation or safety review. It guides the agent to run ClawGuard, report findings by severity, and proceed only when risks are clear to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run a third-party npm CLI through npx or recommend a global npm install. <br>
Mitigation: Verify the intended ClawGuard package before first use, prefer a pinned or isolated npx invocation, and require explicit approval before any global install. <br>
Risk: A clean ClawGuard result may be treated as proof that a skill is fully safe. <br>
Mitigation: Treat scan results as warning signals for known patterns and continue reviewing skill behavior, permissions, and external links before installation. <br>


## Reference(s): <br>
- [ClawGuard Scanner on ClawHub](https://clawhub.ai/Frrrrrrrrank/clawguard-scanner) <br>
- [ClawGuard homepage](https://github.com/Frrrrrrrrank/clawguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and severity-grouped scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request explicit user approval before installation when scan findings indicate high or critical risk.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
