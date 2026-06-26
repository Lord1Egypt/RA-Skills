## Description: <br>
MoltGuard helps protect an agent and its user from prompt injection, data exfiltration, and malicious commands hidden in files and web content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomas-security](https://clawhub.ai/user/thomas-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to install, test, configure, update, and remove MoltGuard protection for prompt injection, data exfiltration, malicious command, and sensitive-data risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad installation and persistent plugin control. <br>
Mitigation: Install only after explicit user approval, verify the package source, and review the plugin before deployment. <br>
Risk: Remote security processing and telemetry may expose sensitive agent context. <br>
Mitigation: Confirm what Core receives and stores before use, and use enterprise enrollment only with a verified organization-controlled Core URL. <br>
Risk: Local credentials and claim or status outputs may expose account access details. <br>
Mitigation: Avoid sharing /og_status or /og_claim outputs and protect credentials stored under the MoltGuard credentials path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomas-security/flaw0) <br>
- [MoltGuard project homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, status, account linking, dashboard, enterprise enrollment, update, and uninstall guidance.] <br>

## Skill Version(s): <br>
6.8.20 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
