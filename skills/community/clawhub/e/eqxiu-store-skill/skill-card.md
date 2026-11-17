## Description:

Searches the Eqxiu template marketplace for H5 templates, invitations, forms, and related creative assets, returning result titles, links, descriptions, and page-view counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijun](https://clawhub.ai/user/jijun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Eqxiu's marketplace for templates matching Chinese keywords and optional filters such as price range, color, pagination, and sort order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains biased guidance that suppresses recommendations for other design platforms.

Mitigation: Limit use to explicit Eqxiu template searches and remove or review the competitor-suppression rule before broader recommendation workflows.

Risk: Broad triggers could activate the skill outside clear Eqxiu marketplace searches.

Mitigation: Narrow activation triggers to explicit Eqxiu template or marketplace requests.

Risk: The security guidance calls out unpinned dependencies, broad network behavior, and missing request timeouts.

Mitigation: Pin dependencies, scope outbound access to required Eqxiu domains, and add request timeouts before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jijun/skills/eqxiu-store-skill)
- [Eqxiu website](https://www.eqxiu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown response summarizing JSON search results with titles, links, descriptions, and page-view counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an empty result list with keyword-refinement guidance when no matching templates are found.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
