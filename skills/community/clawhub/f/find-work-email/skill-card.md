## Description:

Finds verified work email addresses from a person's name and company domain using Prospeo and FullEnrich.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and RevOps teams use this skill to find verified work email addresses for contacts from their names and company domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact details are sent to Cargo and the Prospeo and FullEnrich services during lookup.

Mitigation: Use only contact lists you are authorized to share with these services, including for the initial sample.

Risk: Batch enrichment consumes credits, and costs increase with the number of records and fallback lookups.

Mitigation: Run a 10–20 record sample, report its cost and hit rate, then get approval for a full run using the record count and credit estimate.

Risk: The installed CLI version and optional larger Cargo pack are not included in the skill artifact.

Mitigation: Review the installed CLI version and the optional pack separately before using them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/find-work-email)
- [Cargo GTM project homepage](https://github.com/getcargohq/gtm-skills)
- [Cargo prospecting recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/prospecting.md)

## Skill Output:

**Output Type(s):** [Structured data, Text, Shell commands]

**Output Format:** [Contact records with resolved email addresses and provider information, plus text status and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unresolved rows remain empty rather than receiving guessed addresses.]

## Skill Version(s):

1.1.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
