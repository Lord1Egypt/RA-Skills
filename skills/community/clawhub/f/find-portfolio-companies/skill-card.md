## Description:

Find every portfolio company of an investor or accelerator, then the people inside them, powered by Cargo. Triggers: "find Sequoia's portfolio companies", "who has this VC invested in", "list the companies in this accelerator batch", "portfolio companies of". Providers: theirStack. Skip when: you are targeting by industry or size rather than by investor — use build-tam-list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Account executives and sales development teams can find companies associated with a named investor or accelerator and use the returned company records for follow-on prospecting. Use an investor filter for portfolios; use a separate skill when targeting by industry or company size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches incur credit charges for each returned company, so a broad first query can use more credits than expected.

Mitigation: Start with a 10–20 company limit, report the estimated cost, and get approval before increasing the limit for a full portfolio.

Risk: Partial investor-name matching can include unrelated funds.

Mitigation: Review each result's investor field and use an exact-name filter when precision matters.

Risk: The security assessment covers the bundled instructions, not the downloaded CLI package or the external recipe.

Mitigation: Review the CLI package and external recipe separately before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/find-portfolio-companies)
- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [Portfolio prospecting recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/portfolio-prospecting.md)

## Skill Output:

**Output Type(s):** [Company search results, Shell commands]

**Output Format:** [Structured company records with domains, LinkedIn URLs, and investor fields; inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result limit caps returned companies; each returned company costs 0.5 credits.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
