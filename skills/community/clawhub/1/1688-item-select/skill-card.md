## Description:

Helps 1688 merchants identify and search priority products using multidimensional product scoring, S/A/B/C tiers, and product-selection outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 merchants and commerce operators use this skill to retrieve shop and product metrics, score products across sales, traffic, growth, marketing ROI, and health, and select priority items or search products for operational focus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant Access Key handling may expose sensitive credentials through configuration or gateway setup.

Mitigation: Use a least-privilege 1688 AK, verify OPENCLAW_GATEWAY_URL, prefer environment or secret injection, and protect or avoid plaintext openclaw.json storage.

Risk: Signed requests and usage telemetry are sent to the 1688/OpenClaw gateway.

Mitigation: Review the expected network destination and telemetry flow before installing, and run the skill only where that data flow is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-item-select)
- [Scoring rules](references/scoring_rules.md)
- [Interaction specifications](references/interaction-specs.md)
- [Table schema](references/table_schema.md)
- [Get item overview capability](references/capabilities/get_item_overview.md)
- [Get shop data capability](references/capabilities/get_shop_data.md)
- [Score and select capability](references/capabilities/score_and_select.md)
- [Search offer by keyword capability](references/capabilities/search_offer_by_keyword.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown product recommendations with JSON CLI responses and interactive table payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 3 recommended products, supports user-selected recommendation counts from 1 to 10, and requires a configured 1688 AK for live data access.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
