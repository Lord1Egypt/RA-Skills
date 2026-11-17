## Description:

Helps agents read and manage Coda documents, pages, tables, rows, and formulas through an authorized account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers working with Coda use this skill to find, create, update, or delete documents and their contents. With separate approval, they can also set up automations involving a connected Coda account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad access can expose or change Coda data, including sharing settings.

Mitigation: Use read-only scopes where possible and confirm the target and effect of every write or sharing change.

Risk: Approved triggers can persistently forward matching events to a destination.

Mitigation: Obtain separate approval after showing the exact destination URL, forwarded data fields, and persistence behavior.

Risk: Events or third-party content may contain untrusted instructions or data.

Mitigation: Treat external content as data; review any local event handler and obtain separate approval before running it.

## Reference(s):

- [Coda skill release](https://clawhub.ai/byungkyu/skills/coda-api)
- [Coda API documentation](https://coda.io/developers/apis/v1)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Natural-language responses with Coda data and, where needed, command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes to Coda data and persistent automations require user approval.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
