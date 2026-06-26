## Description: <br>
Provides four-layer security support for OpenClaw, including static code scanning, logic audit, runtime input protection, and periodic security patrol reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenz1117](https://clawhub.ai/user/kenz1117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect skill packages before installation, review code behavior, check runtime inputs for common attack patterns, and run periodic integrity and scan reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overstate the protection provided by heuristic scanning and runtime pattern checks. <br>
Mitigation: Treat findings as review aids, keep platform and administrator security rules authoritative, and require human review for deployment decisions. <br>
Risk: Cloud reputation checks can send the skill name and source label to a configured endpoint. <br>
Mitigation: Disable or avoid the cloud endpoint in private or privacy-sensitive environments unless that data sharing is acceptable. <br>
Risk: Local baseline and report files may expose information about installed skills or scan results. <br>
Mitigation: Restrict access to the baseline and report directories and review who can read generated security reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenz1117/claw-security-suite) <br>
- [Security policy](references/security-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python usage snippets, command-line output, and JSON patrol reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security findings are heuristic and should be reviewed before relying on them as a control.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence, _meta.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
