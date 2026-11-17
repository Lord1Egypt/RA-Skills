## Description:

AP2 Agent-to-Agent mock checkout (SuperShoe). HP/HNP with card or x402 via mcporter and local mock MCP. No real payments.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[xielianghai](https://clawhub.ai/user/xielianghai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to exercise AP2 human-present and human-not-present checkout flows against local mock MCP services with card or x402 payment rails. It helps test agent checkout orchestration without real settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended one-command installer runs code outside the reviewed artifact and can modify OpenClaw setup or start local services.

Mitigation: Install from a trusted and reviewed AP2 checkout, verify the AP2 commit, pin the mcporter version when possible, and prefer the manual setup path for tighter review.

Risk: The skill simulates checkout and mandate-signing behavior, which could be confused with a real payment flow if run against the wrong environment.

Mitigation: Use it only with the documented local mock MCP services, confirm the localhost endpoints, and require explicit user approval before signing mandates.

## Reference(s):

- [AP2 Checkout setup reference](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/xielianghai/skills/ap2-checkout)
- [ClawHub publisher profile](https://clawhub.ai/user/xielianghai)
- [mcporter schema](https://raw.githubusercontent.com/steipete/mcporter/main/mcporter.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local AP2 mock backend services, mcporter configuration, AP2_HOME, and a stable session_id; produces no real payment settlement.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
