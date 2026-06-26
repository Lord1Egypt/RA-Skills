## Description: <br>
ClawSkillShield locally scans OpenClaw and ClawHub skills for security risks such as hardcoded secrets, dangerous calls, risky imports, obfuscation, and hardcoded IP addresses, then reports risk and can quarantine threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbYousef739](https://clawhub.ai/user/AbYousef739) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security reviewers, and autonomous agents use this skill to scan local skill folders before installation or use, review reported risks, and optionally quarantine high-risk content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk labels and automatic quarantine behavior could cause unsafe or disruptive decisions. <br>
Mitigation: Review before installing or enabling automation, use scan-only mode where possible, require explicit approval before quarantine, and verify the risk-label behavior before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbYousef739/clawskillshield) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text reports with risk scores, threat findings, file paths, line numbers, and quarantine status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with no declared runtime dependencies; quarantine moves the target directory to ~/.openclaw/quarantine when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
