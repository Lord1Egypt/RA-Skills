## Description:

Helps enterprise buyers search and compare B2B products across supported marketplaces, returning candidate products with quoted prices, minimum order quantities, supplier names, locations, platform labels, and detail links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kayy123](https://clawhub.ai/user/kayy123)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise procurement users use this skill to convert product names, specifications, budgets, quantities, and shipping-location preferences into a read-only shortlist for price comparison and supplier follow-up through detail links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Procurement searches can expose sensitive buying intent, budgets, preferred locations, or supplier interests.

Mitigation: Review before installing in sensitive procurement environments and restrict use to approved procurement data and approved networks.

Risk: The script can redirect procurement searches to an arbitrary API host through an undocumented environment-variable override.

Mitigation: Remove or allowlist the endpoint override in managed or high-trust environments before deployment.

## Reference(s):

- [Product Search Bridge](references/product_search_bridge.md)
- [ClawHub Skill Page](https://clawhub.ai/kayy123/skills/b2b-product-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Guidance]

**Output Format:** [Markdown table by default; text, HTML, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only product-search results with detail links preserved; no direct contact details, ordering, inquiry sending, or fabricated prices.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
