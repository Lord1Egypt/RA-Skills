## Description:

Helps agents build targeted prospect lists with Exa web search by translating an ideal customer profile into search queries, enriching promising results, and organizing qualified companies or contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, partnership, and go-to-market users use this skill to build ranked prospect lists from an ideal customer profile for outreach, ABM campaigns, or partnership prospecting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command templates could create command-injection risk if user queries or search-result IDs are interpolated directly.

Mitigation: Pass queries and IDs as literal process arguments, validate IDs, and avoid direct shell interpolation.

Risk: The skill may read local product-marketing context files when they are present.

Mitigation: Review local product-marketing context for sensitive or inappropriate information before using it in prospecting workflows.

Risk: Prospecting workflows use Exa web or API searches and may produce stale, incomplete, or unsuitable lead data.

Mitigation: Review and qualify the generated prospect list before outreach or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-exa-lead-generation)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown prospect list with tables, prospect details, search queries, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include company websites, fit rationale, qualifying signals, and suggested next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
