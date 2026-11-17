## Description:

Run a customer support desk on DeskCrew by drafting knowledge-base-grounded replies for human approval; the release also describes an x402 bounty-board payment capability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webmilmind1](https://clawhub.ai/user/webmilmind1)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and agents use this skill to triage DeskCrew tickets, search the company knowledge base, and file reply drafts for human approval. It is intended for first-line support workflows where customer-facing sends, resolves, and assignments remain disabled unless a workspace admin explicitly enables them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release description includes an x402 bounty-board/payment capability that is not explained by the support-desk workflow.

Mitigation: Review the payment-related language before installing or using the skill and do not enable it unless the operator understands and intends that behavior.

Risk: A DeskCrew credential with send, resolve, or assign permissions could allow drafts or actions to reach customers without the intended review gate.

Mitigation: Use a fresh draft-tier DeskCrew credential and keep send, resolve, and assign disabled until humans have reviewed outputs over time.

Risk: Continuous scheduled processing can act on tickets repeatedly if enabled without operational controls.

Mitigation: Enable the cron job only for intentionally continuous ticket processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webmilmind1/skills/deskcrew-support)
- [DeskCrew](https://deskcrew.io)
- [DeskCrew MCP endpoint](https://deskcrew.io/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces support reply drafts, escalation guidance, MCP setup configuration, and scheduled-run commands; customer-facing actions require separate DeskCrew permissions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
