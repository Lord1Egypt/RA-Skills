## Description:

Official Easyship integration for shipping rates, shipment and label management, tracking, pickups, billing, address validation, and analytics across 550+ couriers in 200+ countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulld](https://clawhub.ai/user/paulld)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to compare shipping rates, create and manage shipments and labels, track packages, schedule pickups, validate addresses, review billing records, and inspect shipping analytics through a hosted Easyship integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Easyship API token enables shipment management, label purchases, pickup scheduling, billing access, and analytics access.

Mitigation: Install only when that hosted access is intended, use a revocable or appropriately scoped token where available, and rotate or revoke the token if access is no longer needed.

Risk: Shipment creation, label purchase, pickup scheduling, cancellation, and deletion can affect real shipping operations or incur costs.

Mitigation: Review and approve operational or billing-impacting actions before execution, especially label purchase, shipment creation, pickup scheduling, cancellation, and deletion.

Risk: Shipping rates and delivery estimates may be inaccurate when address, parcel, item, or customs data is assumed or incomplete.

Mitigation: Provide complete origin, destination, parcel, and customs details where possible, and present estimated rates as estimates when assumptions were used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulld/skills/easyship-official)
- [Hosted Easyship MCP endpoint](https://mcp.easyship.com)
- [Easyship API token setup](https://app.easyship.com/connect)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown text with tables, links, and tool/API call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Easyship document URLs, rate comparisons, tracking checkpoints, billing records, pickup slots, and analytics summaries.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
