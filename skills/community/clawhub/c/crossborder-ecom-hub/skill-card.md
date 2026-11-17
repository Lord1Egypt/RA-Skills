## Description:

Crossborder Ecom Hub helps sellers manage products, orders, inventory, pricing, reports, and Feishu exports across TikTok Shop, Amazon, Shopee, and Lazada.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and their agents use this skill to coordinate multi-platform catalog sync, order review, inventory checks, pricing recommendations, reports, and Feishu exports from one CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for powerful marketplace and Feishu credentials that can expose store data or authorize business changes.

Mitigation: Start with least-privilege test credentials, avoid command-line secrets, and restrict permissions on ~/.crossborder-ecom/config.json.

Risk: Bulk sync, inventory, pricing apply, and Feishu export commands can change or upload operational data across connected accounts.

Mitigation: Preview the exact products, prices, inventory records, and uploads in a test account before running these commands against production.

Risk: Server security evidence marks the release suspicious because safeguards for live changes and secrets are weak.

Mitigation: Review the source and configuration before installation, run limited read-only commands first, and monitor connected platform activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/crossborder-ecom-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration and may call third-party commerce or Feishu APIs when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
