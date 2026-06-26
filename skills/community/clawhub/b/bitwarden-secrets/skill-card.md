## Description: <br>
Safely access Bitwarden or Vaultwarden secrets via the bw CLI with redacted outputs by default for vault sync, item search, metadata retrieval, and explicitly confirmed single-field reveal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClawBow](https://clawhub.ai/user/ClawBow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query Bitwarden or Vaultwarden through the bw CLI while keeping default output limited to redacted item metadata. It supports sync, search, item metadata lookup, and narrowly scoped reveal of one secret field only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional bootstrap and environment-export flows can expose full vault credentials in shell output, environment variables, or temporary files. <br>
Mitigation: Prefer the redacted vw_cli.py workflow; avoid bootstrap/env-export unless that exposure is acceptable, run as a non-root user, and delete generated export files immediately. <br>
Risk: Reveal mode can output an actual username, password, or TOTP value after both guards are enabled. <br>
Mitigation: Reveal only one required field after explicit approval, then remove VW_REVEAL_ALLOW and avoid sharing the resulting secret in chat or logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ClawBow/bitwarden-secrets) <br>
- [Setup checklist](setup-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default item views are redacted; reveal output is gated by an environment flag and explicit confirmation token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
