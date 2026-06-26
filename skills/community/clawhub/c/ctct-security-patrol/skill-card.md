## Description: <br>
CTCT Security Patrol guides OpenClaw and TeleClaw users through a local security audit, with an optional consent-gated mode that uploads audit summaries to Changeway threat-intelligence endpoints for scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsyjx0115](https://clawhub.ai/user/zsyjx0115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw and TeleClaw users use this skill to run local security checks, review summarized audit results, and optionally set up recurring local patrols through OpenClaw cron. Users who explicitly choose the full detection mode can also request remote threat-intelligence scoring from the publisher-operated auth.ctct.cn service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the release as suspicious because a persistent device ID may be created and stored locally even when the skill describes that behavior as upload-mode only. <br>
Mitigation: Install only after reviewing this behavior, prefer a disposable or controlled OpenClaw state directory for evaluation, and remove the local agent ID if you do not accept persistent device identification. <br>
Risk: The audit reads sensitive local information and stores reports and baselines under ~/.openclaw. <br>
Mitigation: Run the skill only on systems where local security-report storage is acceptable, protect the ~/.openclaw directory, and review saved reports before sharing them. <br>
Risk: The optional --push mode can send MAC address, hostname, persistent agent ID, installed skill inventory, and scan summaries to auth.ctct.cn, creating device fingerprinting and history-correlation risk. <br>
Mitigation: Use local mode by default, enable --push only after explicit informed consent, avoid --push in scheduled jobs, and proceed only if the user trusts the publisher-operated endpoint. <br>
Risk: Security guidance says to treat the script integrity hash as stale until the publisher fixes it. <br>
Mitigation: Do not rely on the embedded integrity comment as proof of script integrity; verify the published file hash against trusted release evidence before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zsyjx0115/ctct-security-patrol) <br>
- [OpenClaw security patrol cron setup guide](references/cron-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Analysis] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise audit summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks for user choices before optional cron setup or upload mode, then summarizes scan counts, score when available, and the local report path.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
