## Description: <br>
Issue ClawPrint reverse-CAPTCHA challenges to verify that another user or agent is a real AI, not a human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fusionlabssource](https://clawhub.ai/user/fusionlabssource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to issue, present, verify, and validate ClawPrint challenges before allowing AI-only access or continuing a gated workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-verification pass or fail results may be overused to justify sharing credentials, API keys, protected resources, or privileged access. <br>
Mitigation: Treat ClawPrint as one signal only; require normal identity checks, authorization, and policy or human approval before sensitive actions. <br>
Risk: The skill depends on an external ClawPrint service and requires local keys for challenge issuance and validation. <br>
Mitigation: Install only when the external service is intentionally approved, protect CLAWPRINT_SECRET_KEY, and avoid exposing secret values in prompts, logs, or challenge messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fusionlabssource/clawprint-verify) <br>
- [ClawPrint API endpoint](https://dependable-adventure-production-44e3.up.railway.app/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, CLAWPRINT_SERVER_URL, CLAWPRINT_SITE_KEY, and CLAWPRINT_SECRET_KEY for validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
