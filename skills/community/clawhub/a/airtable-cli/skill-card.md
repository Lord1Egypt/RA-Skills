## Description:

Airtable API client for listing bases and tables, reading and changing records, searching/filtering data, and importing or exporting CSV with pagination and rate-limit awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, operations teams, and agents use this skill to inspect Airtable bases and tables, automate record CRUD workflows, perform batch create/delete or upsert operations, and export Airtable data as JSON or CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from an unpinned raw main-branch URL can execute code that differs from the audited package.

Mitigation: Install from the packaged audited artifact or from a pinned, verified release.

Risk: Delete, batch-delete, and upsert commands can remove or bulk-change Airtable records.

Mitigation: Use a least-privilege Airtable token, test first against non-production bases, and verify base IDs, table names, record IDs, and merge keys before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/airtable-cli)
- [Airtable personal access tokens](https://airtable.com/create/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may be plain text, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and an AIRTABLE_API_KEY environment variable.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
