## Description:

ClawPlot lets agents submit SVG artwork to order physical pen-plotted art with archival ink, payment options, and worldwide shipping through ClawPlot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theghostofjoemacmillan](https://clawhub.ai/user/theghostofjoemacmillan)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn SVG artwork into commissioned physical pen-plotted pieces, including gifts and collectible art. The skill guides catalog lookup, order submission, payment selection, and order-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could submit a paid physical-art order or initiate a payment flow before the user has confirmed the details.

Mitigation: Require explicit user confirmation of price, recipient, shipping address, selected options, and payment method before calling the order or checkout endpoints.

Risk: The ordering workflow can send SVG content, shipping name and address, and payment-method choice to clawplot.com.

Mitigation: Use this skill only when the user explicitly wants to order from ClawPlot, and minimize personal data to the fields required for fulfillment.

Risk: Submitted SVG artwork may be invalid, too large, or poorly suited to pen plotting.

Mitigation: Validate SVG 1.1 markup, keep files within the documented 500KB limit, and prefer clean stroke-based designs before submitting an order.

## Reference(s):

- [ClawPlot API Reference](references/api.md)
- [ClawPlot service](https://clawplot.com)
- [ClawHub skill page](https://clawhub.ai/theghostofjoemacmillan/skills/clawplot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in external API requests that create paid physical art orders and transmit SVG, shipping, and payment-method details.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
