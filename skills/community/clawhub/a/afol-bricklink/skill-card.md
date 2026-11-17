## Description:

Use the self-contained BrickLink API CLI for OAuth1-signed catalog, pricing, order, inventory, feedback, coupon, shipping, notification, and member-note workflows with guarded marketplace writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

AFOLs, BrickLink sellers, and agents assisting store operators use this skill to query BrickLink catalog and pricing data and to manage orders, inventory, feedback, coupons, shipping methods, notifications, and member notes through a guarded OAuth-signed CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials and marketplace data could be sent to an arbitrary API base URL if BRICKLINK_API_BASE_URL or the CLI base-url option is changed.

Mitigation: Leave BRICKLINK_API_BASE_URL unset or set it exactly to the official BrickLink API URL, and use only a BrickLink account whose OAuth permissions are acceptable for this tool.

Risk: Marketplace write operations can modify live inventory, orders, feedback, coupons, and private member notes.

Mitigation: Use dry-run output first, inspect generated commands and request bodies, and execute with --yes only after explicit confirmation of the exact action.

Risk: Dry-run output and terminal logs may expose private order, buyer, inventory, coupon, feedback, or member-note details.

Mitigation: Treat dry-run and CLI output as private and share only minimal summaries needed for the task.

## Reference(s):

- [BrickLink OpenAPI Reference](references/openapi/bricklink.yaml)
- [BrickLink Tool Guidance](references/prompts/bricklink-tools.txt)
- [BrickLink API Documentation](https://www.bricklink.com/v3/api.page)
- [ClawHub Skill Listing](https://clawhub.ai/musketyr/skills/afol-bricklink)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating marketplace commands require dry-run review and explicit confirmation before --yes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
