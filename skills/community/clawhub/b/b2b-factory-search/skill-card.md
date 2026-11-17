## Description:

Helps business buyers turn manufacturer-sourcing requests into a structured shortlist of candidate factories with public business details, capability tags, and profile links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kayy123](https://clawhub.ai/user/kayy123)

### License/Terms of Use:

MIT-0

## Use Case:

External business buyers and sourcing teams use this skill to search for manufacturers by product, region, capability, certification, and factory type, then review public supplier profile information before contacting vendors themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Factory-search queries and filters are sent to an external B2B search service.

Mitigation: Use only when that data sharing is acceptable, avoid sensitive sourcing details in queries, and keep host permissions limited to running the bundled lookup script.

Risk: Returned supplier profiles may be incomplete, unavailable, or limited to the covered platform.

Mitigation: Preserve unavailable fields, do not fill gaps from assumptions, and direct users to verify details through the linked supplier profiles.

Risk: Public profile information and capability tags could be mistaken for a reliability recommendation.

Mitigation: Present the results as factual profile data only and avoid claims that any supplier is definitively reliable, best, or qualified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kayy123/skills/b2b-factory-search)
- [factory_search interface contract](references/factory_search_bridge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Text, Markdown, or HTML shortlist with supplier profile links and factual factory fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves missing fields as unavailable and limits conclusions to public supplier profile information.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
