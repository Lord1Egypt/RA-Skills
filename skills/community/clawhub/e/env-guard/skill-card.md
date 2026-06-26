## Description: <br>
Scan repos and workspaces for leaked secrets. API keys in code, passwords in configs, tokens in logs. Catches them before they hit git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security-conscious teams use Env Guard to scan local repositories and workspaces for leaked credentials before committing or deploying code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A clean result may be misleading if the documented command scans the wrong path instead of the intended project. <br>
Mitigation: Run the target path directly, for example `node src/env-guard.js ./my-project`, and confirm the findings or exit code correspond to the intended directory. <br>
Risk: Scan output may include snippets from lines that contain secrets. <br>
Mitigation: Keep scan results local and redact findings before sharing logs, tickets, or reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/env-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text or JSON report data from a local scan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include file path, line number, severity, secret type, and a redacted snippet; scan results should stay local unless intentionally shared.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
