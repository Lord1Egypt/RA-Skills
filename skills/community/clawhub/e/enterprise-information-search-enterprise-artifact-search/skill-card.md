## Description:

Multi-hop evidence search and structured extraction over enterprise artifact datasets, with product grounding to reduce cross-product leakage and evidence pointers for returned entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and enterprise agents use this skill to answer multi-hop questions over document, chat, meeting, PR, URL, and directory artifacts while preserving evidence pointers for extracted IDs and entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface employee IDs and internal snippets from enterprise artifacts as part of its intended output.

Mitigation: Install and use it only in workspaces where agent access to enterprise documents, chats, meetings, PRs, URLs, and employee directory metadata is appropriate.

Risk: Search results may mix artifacts from similarly named products or unrelated reports if product grounding is skipped.

Mitigation: Require at least two independent product-grounding signals before accepting a report and reject artifacts that are grounded to a different product.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/enterprise-information-search-enterprise-artifact-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON-ready answer object and evidence map, usually reported in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes artifact identifiers, short supporting snippets, and recommendation status.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
