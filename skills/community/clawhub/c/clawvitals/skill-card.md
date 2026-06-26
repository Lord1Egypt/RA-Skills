## Description: <br>
Security vitals checker for OpenClaw. Scans your installation, scores your setup, and shows you exactly what to fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bk-cm](https://clawhub.ai/user/bk-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use ClawVitals to run point-in-time security checks for self-hosted OpenClaw installations, review scored findings, and get remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detailed reports may reveal OpenClaw configuration weaknesses or security posture information. <br>
Mitigation: Run detailed reports in private or administrator-only channels and display only the fields permitted by the skill instructions. <br>
Risk: The update-status check may cause the OpenClaw CLI to contact its update registry. <br>
Mitigation: For fully offline scans, skip the update-status step and mark dependent version controls as N/A. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bk-cm/clawvitals) <br>
- [ClawVitals website](https://clawvitals.io) <br>
- [ClawVitals docs](https://clawvitals.io/docs) <br>
- [ClawVitals controls](https://clawvitals.io/docs/controls) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with a scored controls table, findings, remediation text, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports PASS, FAIL, N/A, and experimental notes from declared OpenClaw and Node CLI checks.] <br>

## Skill Version(s): <br>
1.4.8 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
