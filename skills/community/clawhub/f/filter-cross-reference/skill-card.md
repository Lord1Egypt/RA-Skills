## Description:

Looks up cross-reference, equivalent, and interchange part numbers for heavy-duty oil, air, fuel, hydraulic, cabin, and water-separator filters using the public Precise Filters lookup service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly0pants](https://clawhub.ai/user/fly0pants)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and maintenance teams use this skill to identify replacement or interchange filter part numbers from a user-provided part number. It returns direct matches, key fitment details, selected cross-references, and links for full product review or manual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided part numbers are sent to precise-filters.com for lookup.

Mitigation: Use the skill only when it is acceptable to send the queried part numbers to that public service.

Risk: Returned specs and cross-reference lists may be partial, and visually similar filters can differ in fitment-critical details.

Mitigation: Verify dimensions, sealing, thread, flow direction, and machine compatibility against the linked product page or another authoritative source before ordering.

## Reference(s):

- [Precise Filters Website](https://www.precise-filters.com)
- [Precise Filters Cross-Reference Lookup](https://www.precise-filters.com/en/cross-reference)
- [Precise Filters Product Catalog](https://www.precise-filters.com/en/products)
- [Precise Filters Contact Page](https://www.precise-filters.com/en/contact)
- [ClawHub Skill Release Page](https://clawhub.ai/fly0pants/skills/filter-cross-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries with links, optional compact tables, and source-backed lookup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One lookup request is made per part number; responses may include product links, fitment specs, cross-reference numbers, and manual verification links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
