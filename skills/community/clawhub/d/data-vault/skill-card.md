## Description:

Data Vault persists and retrieves structured data across sessions using the Lance columnar format for storage, querying, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitorhugoze](https://clawhub.ai/user/vitorhugoze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to create, append, update, read, back up, and delete local Lance datasets for structured data that should persist across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset names may bypass the intended storage boundary.

Mitigation: Use only explicit, simple dataset names; the maintainer should validate dataset names consistently in write.py.

Risk: Delete and drop commands can permanently change stored data.

Mitigation: Back up datasets before destructive operations and add confirmation or recovery for destructive commands.

Risk: Stored records may include secrets or regulated personal data.

Mitigation: Avoid storing secrets or regulated personal data and limit entries to approved structured records.

## Reference(s):

- [Lance columnar format](https://github.com/lance-format/lance)
- [Lance documentation](https://lance.org)
- [Data Vault ClawHub page](https://clawhub.ai/vitorhugoze/skills/data-vault)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON command responses with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local Lance datasets and include status, data, and error fields.]

## Skill Version(s):

1.0.18 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
