## Description:

Enriches company domains with industry, size, geography, founding year, and headquarters using Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and revenue operations teams use it to enrich company domain lists with firmographic details for account research and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company domains are shared with Cargo and aiArk during enrichment.

Mitigation: Use only company domains approved for sharing with those services.

Risk: Batch enrichment costs scale with the number of company records.

Mitigation: Start with a 10–20 record sample, review its results and estimated cost, and approve the full batch only after that review.

## Reference(s):

- [Cargo GTM project](https://github.com/getcargohq/gtm-skills)
- [Build TAM recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/build-tam.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured company firmographic records, often presented as a table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company fields may be blank when no match is found.]

## Skill Version(s):

1.1.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
