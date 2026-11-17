## Description:

Find B2B leads by job title, company, or keyword and return them as a structured list using Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development teams use this skill to find people matching a prospect profile by title, company, and keyword, then review their returned profile details and LinkedIn URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit-based searches can incur costs as the search volume grows.

Mitigation: Start with a 10–20 record sample, report the observed cost and hit rate, and get approval with a credit estimate before a full run.

Risk: The skill may offer to star its publisher's GitHub repository.

Mitigation: Treat starring as optional and act only after the user gives explicit consent.

Risk: The security review covers the bundled instructions, not external packages or services.

Mitigation: Review and pin the CLI package version, and review the broader Cargo pack separately before installing it.

## Reference(s):

- [Cargo prospecting recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/prospecting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured list of lead profiles with name, title, company, location, and LinkedIn URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles are returned in pages of 25; results contain profile links, not email addresses.]

## Skill Version(s):

1.2.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
