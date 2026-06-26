## Description: <br>
Legal/compliance guardrails for outbound OpenClaw actions (anti-spam, defamation, privacy, financial claims). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lawyered0](https://clawhub.ai/user/lawyered0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check outbound posts, comments, messages, market commentary, HR-sensitive text, and privacy-sensitive content before publishing or sending it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command wrapper can execute outbound commands after a REVIEW result. <br>
Mitigation: Use --strict for real posting, email, messaging, or publishing workflows so REVIEW results block execution. <br>
Risk: The --allow-any-command override can bypass command allowlist controls. <br>
Mitigation: Use narrow --allowed-command values in normal operation and reserve --allow-any-command for audited exceptions with an approval token and reason. <br>
Risk: Outbound commands may inherit more environment data than needed. <br>
Mitigation: Enable --sanitize-env and keep only explicit variables or prefixes required by the outbound tool. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lawyered0/enterprise-legal-guardrails) <br>
- [Guardrail Policy Map](references/guardrail-policy-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON checker output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checker decisions include PASS, WATCH, REVIEW, and BLOCK; wrapper execution is validation-only unless explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.20 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
