## Description: <br>
Claw Audit scans OpenClaw skills, configuration, and host hardening for security issues and returns actionable scores, findings, and hardening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u45362](https://clawhub.ai/user/u45362) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Claw Audit to scan installed OpenClaw skills for malicious patterns, audit OpenClaw and host security posture, calculate a 0-100 security score, and get hardening or auto-fix guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive host security areas and may expose information about credentials, configuration, or host hardening if run with broad permissions. <br>
Mitigation: Run least-privileged first and grant shadow-group, Docker, or sudoers access only when that extra access is explicitly needed. <br>
Risk: Auto-fix and hardening actions can change OpenClaw configuration. <br>
Mitigation: Prefer dry-run or interactive auto-fix and require explicit confirmation before applying changes. <br>
Risk: The .claw-audit-trusted scan-skip marker is not a reliable trust boundary. <br>
Mitigation: Do not treat skip markers as proof of safety; review and scan skills before deployment. <br>


## Reference(s): <br>
- [Claw Audit ClawHub listing](https://clawhub.ai/u45362/claw-audit) <br>
- [ClawHavoc campaign analysis](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) <br>
- [malicious-patterns.json](references/malicious-patterns.json) <br>
- [scan-rules.json](references/scan-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with command snippets and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create integrity baselines, report security scores, and propose or apply configuration fixes after confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, RELEASE-NOTES-v1.1.0.md, and clawhub.json; package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
