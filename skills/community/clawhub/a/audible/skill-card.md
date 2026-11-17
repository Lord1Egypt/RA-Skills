## Description:

Audible helps agents summarize public Audible product pages, catalog entry points, membership information, help content, and promotional pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research public Audible catalog, membership, help center, and campaign pages. It supports concise summaries, tables, and link lists while staying within copyright and account-safety boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide private Audible or Amazon account data, purchase history, or credentials.

Mitigation: Do not request, process, or retain private account data; redirect the task to public Audible pages or general account-safety guidance.

Risk: Audible membership terms, content availability, and download rules can vary by region and time.

Mitigation: State the region and date context when summarizing terms, and verify details against the current public page before making a recommendation.

Risk: Requests may seek pirated downloads, copyright bypass, account sharing, or membership abuse.

Mitigation: Decline bypass or abuse instructions and provide only public, rights-respecting information from Audible and its help content.

## Reference(s):

- [Audible](https://www.audible.com/)
- [ClawHub Audible Skill](https://clawhub.ai/mikeclaw007/skills/audible)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries, tables, and link lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Audible information only and does not handle private account data.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
