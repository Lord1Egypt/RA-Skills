## Description:

Builds a reusable tool that finds and ranks relevant stakeholders at supplied accounts, with optional verified work email and phone enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

GTM engineering, RevOps, and sales development teams use this skill to configure a reusable workflow that finds stakeholders matching an account-specific use case and returns a ranked shortlist with supporting profile evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command uses an unpinned CLI release, and the security assessment is incomplete.

Mitigation: Review the installation instructions and imported skill, use a verified pinned CLI version and immutable source revision, and install in an environment without production credentials or unnecessary file access.

## Reference(s):

- [Audit seller context and approve the people](references/audit.md)
- [Configure contact sourcing](references/configure.md)
- [Run contact sourcing](references/run.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Structured contact data]

**Output Format:** [Reusable Cargo tool with ranked stakeholder records and supporting profile evidence]

**Output Parameters:** [Per account; return all qualified stakeholders or up to a requested positive N]

**Other Properties Related to Output:** [Optional verified work email and phone enrichment; enrichment does not change ranking.]

## Skill Version(s):

0.2.0 (source: target metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
