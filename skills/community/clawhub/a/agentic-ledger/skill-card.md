## Description:

Agentic Ledger helps OpenClaw users track token and cost usage, enforce spending budgets, and replay captured runs against cheaper or local models while keeping ledger data on the local machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shekharbhardwaj](https://clawhub.ai/user/shekharbhardwaj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to answer cost and usage questions from a local ledger, configure budget walls that stop model calls, and compare captured runs against lower-cost model options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes OpenClaw model calls through a local proxy and stores prompts and responses on the local machine.

Mitigation: Use it only when local capture is acceptable, confirm how to delete or redact ledger data, and avoid sensitive workloads until retention expectations are clear.

Risk: The skill recommends persistent host-side command approval for ledger reads.

Mitigation: Scope any approval exception to /usr/bin/curl only and avoid broader command allowlisting.

Risk: Budget-wall settings change whether model calls are forwarded or refused.

Mitigation: Set and test budget limits and refusal status in a low-risk run before relying on them for spend control.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local HTTP endpoint reads, budget configuration commands, and plain-language cost summaries.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
