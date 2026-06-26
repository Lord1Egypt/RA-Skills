## Description: <br>
Issue ClawPrint reverse-CAPTCHA challenges to verify that another user or agent is a real AI, not a human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fusionlabssource](https://clawhub.ai/user/fusionlabssource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to issue ClawPrint challenges before sharing sensitive credentials, gating AI-only services, or validating that a conversation partner is likely an AI agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends verification data and the secret key to the configured ClawPrint server. <br>
Mitigation: Set CLAWPRINT_SERVER_URL only to a trusted HTTPS endpoint and protect CLAWPRINT_SECRET_KEY like a password. <br>
Risk: Command bodies or logs could expose challenge details or secrets. <br>
Mitigation: Avoid logging request bodies and redact environment values from transcripts, shell history, and operational logs. <br>
Risk: A passed challenge should not be treated as sufficient proof for highly sensitive actions unless the verifier trusts the service model. <br>
Mitigation: Use server-side validation and apply additional authorization checks before releasing sensitive credentials or resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fusionlabssource/captcha-ai) <br>
- [Publisher profile](https://clawhub.ai/user/fusionlabssource) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus CLAWPRINT_SERVER_URL, CLAWPRINT_SITE_KEY, and CLAWPRINT_SECRET_KEY for validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
