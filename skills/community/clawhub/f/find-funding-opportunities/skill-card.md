## Description:

Searches the Karma Funding Map public API for funding programs, including grants, hackathons, bounties, accelerators, VC funds, and RFPs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheshmurthy](https://clawhub.ai/user/maheshmurthy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find relevant funding opportunities by program type, ecosystem, budget, category, deadline, organization, or keyword. The skill guides the agent to query Karma's public API and return concise, actionable program summaries with application links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Karma's public API along with a per-use invocation ID and skill version header.

Mitigation: Avoid entering confidential application details in search queries and review outgoing requests before execution.

Risk: Funding program data can be stale or incomplete, including budgets, eligibility, deadlines, and application links.

Mitigation: Verify critical details on the linked program or organization site before applying or making decisions.

## Reference(s):

- [Karma Funding Map API Reference](references/api-reference.md)
- [Karma Funding Map API](https://gapapi.karmahq.xyz)
- [ClawHub Skill Page](https://clawhub.ai/maheshmurthy/skills/find-funding-opportunities)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown results with inline shell commands and funding program links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Karma API queries and formats ranked program results; no credentials required.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
