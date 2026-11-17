## Description:

Routes LLM requests to local providers first, validates local response quality, escalates to cloud only when needed, and tracks local, escalated, and cloud outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelnishanth](https://clawhub.ai/user/joelnishanth)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to prefer local LLM execution, validate whether local output is good enough to keep, and fall back to cloud execution when local routing is unavailable, too complex, or fails validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive prompts may be sent to cloud fallback paths without clear consent.

Mitigation: Require explicit approval before cloud fallback for sensitive prompts, verify the destination provider, and keep output redaction enabled.

Risk: The local provider setup documentation includes a remote curl-to-shell installer pattern.

Mitigation: Use a verified package manager or vendor-provided installation path instead of piping remote installer output directly to a shell.

Risk: Routing history stores operational metadata such as timestamps, token counts, model names, outcomes, and estimated savings.

Mitigation: Treat the savings ledger as local operational data and apply appropriate access controls and retention practices.

## Reference(s):

- [Adaptive Routing ClawHub Release](https://clawhub.ai/joelnishanth/skills/adaptive-routing)
- [Routing and Validation Logic](references/routing-logic.md)
- [Local LLM Provider Setup](references/local-providers.md)
- [Token Estimation and Cloud Cost Reference](references/token-estimation.md)
- [LM Studio](https://lmstudio.ai)
- [llamafile Releases](https://github.com/Mozilla-Ocho/llamafile/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routing tools may produce local/cloud decisions, validation scores, escalation flags, provider status, and a persistent local savings summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
