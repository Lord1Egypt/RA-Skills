## Description: <br>
Diagnose and fix gateway token mismatches causing 401 errors. Align tokens across config, service, and CLI surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose 401 Unauthorized errors caused by mismatched OpenClaw gateway tokens and to align token values across configuration, service startup, and CLI surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose live gateway tokens if token-printing lines are run or copied into shared chats or logs. <br>
Mitigation: Do not print or share full token values; redact secrets and rotate the gateway token if it has already been exposed. <br>
Risk: The workflow modifies OpenClaw configuration and gateway startup files that control authentication. <br>
Mitigation: Back up the OpenClaw config and gateway startup script before editing, then verify gateway status and CLI authentication after changes. <br>


## Reference(s): <br>
- [Privacy Checklist](references/privacy-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides diagnostic and configuration guidance; users should redact token values before sharing any output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
