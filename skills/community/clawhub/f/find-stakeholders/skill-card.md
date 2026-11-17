## Description:

Finds potential buying committee stakeholders at a target account using title, seniority, and department filters through Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development representatives and account executives use this skill to identify likely decision makers at a target company by filtering for relevant roles, seniority, and departments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial; it notes account changes and a local marker, and does not establish behavior of the externally installed CLI.

Mitigation: Review the reported account and local-file actions, and verify that you trust the installer source and version before installing.

Risk: Credit use scales with the number of returned stakeholder records and can grow across a large batch.

Mitigation: Start with a small sample, review the observed cost and hit rate, and confirm the estimate before a larger run.

## Reference(s):

- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [Account expansion recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/account-expansion.md)
- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/find-stakeholders)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Stakeholder records presented as a Markdown table with names, titles, and profile links, plus concise usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records depend on the target account and selected filters; provider charges credits per returned record.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
