## Description: <br>
智能体安全管家 is an OpenClaw and TeleClaw security patrol skill that runs local security scans, supports optional scheduled scans, and can upload summary data to Changeway threat-intelligence endpoints only after explicit user consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smbbws2](https://clawhub.ai/user/smbbws2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw and TeleClaw users, administrators, and developers use this skill to audit local agent environments, review security scan results, and optionally configure recurring local patrols. It is most appropriate when the user wants a host-level security check with clear consent gates for any remote threat-intelligence lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads host metadata, system logs, workspace files, and the installed skill inventory during local scans. <br>
Mitigation: Run it only in environments where that host-level access is acceptable, and review the local report contents before sharing them. <br>
Risk: The default local mode creates a persistent .agent-id even though documentation describes persistent identifier creation as upload-mode behavior. <br>
Mitigation: Review the generated OpenClaw state directory after execution and remove the identifier if persistent local device tracking is not acceptable. <br>
Risk: The optional --push mode sends device identifiers and the full skill list to Changeway/auth.ctct.cn. <br>
Mitigation: Use local mode by default and enable --push only after explicit user consent and trust review of the Changeway service. <br>
Risk: Scheduled scans can repeatedly access local security state and write reports. <br>
Mitigation: Enable OpenClaw cron only when recurring scans are desired, and keep --push out of scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smbbws2/ct-security-patrol) <br>
- [Cron setup guide](references/cron-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and concise scan-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report files under the OpenClaw state directory and summarizes PASS, FAIL, and SKIP counts for the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
