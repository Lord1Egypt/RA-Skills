## Description:

Find companies by the technologies they use and the roles they are hiring for.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and marketing teams use this skill to find companies that use selected technologies or show hiring signals for specified roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches require Cargo sign-in and consume credits per company returned.

Mitigation: Confirm current filters and pricing, sample a small result set, and approve larger runs only after reviewing the expected cost.

Risk: Unknown filter fields can be silently dropped inside workflow nodes, causing an unfiltered search and unexpected charges.

Mitigation: Use the documented TheirStack filter keys and check that the workflow retains the intended filters before running it.

Risk: The external CLI and broader skill pack are not audited by the supplied security review.

Mitigation: Review those dependencies separately and prefer fixed versions.

## Reference(s):

- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [Tech intent recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/tech-intent.md)
- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/find-companies-using-tech)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Company search results with matching technology and hiring evidence, summarized in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on selected filters and may incur per-company credit charges.]

## Skill Version(s):

1.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
