## Description:

Find the best products in any category with expert picks, value recommendations, and budget options across US, UK, and EU retailers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralph-oei](https://clawhub.ai/user/ralph-oei)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare products by category and receive top, value, and budget recommendations with regional availability and price context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search terms are sent through built-in web search and fetch tools, and product names are embedded in generated Google search URLs.

Mitigation: Avoid entering sensitive or private purchase details in product queries; review generated search links before opening them.

Risk: Cached product results are stored locally for up to 6 hours.

Mitigation: Clear the documented cache folder when cached product names and prices should not remain on the local machine.

Risk: The default shopping region is the Netherlands, which can produce less relevant retailers or prices for users in other markets.

Mitigation: Specify a supported region in the request when shopping outside the Netherlands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ralph-oei/skills/best-product)
- [Publisher Profile](https://clawhub.ai/user/ralph-oei)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style product recommendation text with product names, price ranges, short rationale, sources, and search links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to the Netherlands unless the user specifies a supported region; caches product result data locally for 6 hours.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
