## Description:

Monitors 1688 wholesale product prices and helps users query dropshipping prices, supplier information, comparable listings, minimum order quantities, and profit estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, purchasing operators, and agents use this skill to look up 1688 wholesale prices, supplier details, dropshipping options, and simple profit calculations before making sourcing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network and dependency risk from using a Python helper that calls 1688 pages with the requests package.

Mitigation: Use a virtual environment, review and pin dependencies before installation, and run the helper only in an environment allowed to access the target network.

Risk: Price, supplier, and product data may be incomplete, stale, or unavailable.

Mitigation: Verify prices, suppliers, and transaction terms directly on 1688 before purchasing or making business decisions.

Risk: The inspected release is a simple lookup helper rather than a full monitoring system.

Mitigation: Treat outputs as point-in-time lookup guidance and add separate scheduling, alerting, and validation controls if continuous monitoring is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/1688-price-monitor)
- [Publisher profile](https://clawhub.ai/user/275254cl-hash)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summaries with optional JSON output from the Python price lookup helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product identifiers, price ranges, supplier details, shipping values, minimum order quantities, and profit calculations when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
