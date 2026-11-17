## Description:

Retrieve real founder experiences, decisions, and outcomes from Echomindr - 1,150+ moments from top startup podcasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voxbase](https://clawhub.ai/user/voxbase)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, operators, and advisors use this skill to retrieve relevant public founder examples for startup dilemmas, decisions, and uncertainty. It helps ground advice in comparable founder moments with decisions, outcomes, lessons, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Founder situation prompts are sent to echomindr.com for lookup.

Mitigation: Send only short, anonymized business-situation summaries and exclude names, emails, company-identifying facts, secrets, customer data, and confidential strategy.

Risk: Retrieved founder examples may be mistaken for directly applicable advice.

Mitigation: Use returned examples as context, compare them against the user's actual situation, and preserve source links so readers can inspect the underlying public founder moment.

## Reference(s):

- [Echomindr homepage](https://echomindr.com)
- [Echomindr API documentation](https://echomindr.com/docs)
- [ClawHub skill page](https://clawhub.ai/voxbase/skills/echomindr-founder-retrieval)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with founder examples, source links, and optional inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include matched founder summaries, decisions, outcomes, lessons, and podcast timestamp links returned by Echomindr.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
