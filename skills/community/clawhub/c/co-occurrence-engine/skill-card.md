## Description:

Co Occurrence Engine is a Hebbian co-occurrence graph skill that records memory co-occurrences, calculates association weights, supports related-memory queries, and provides local database maintenance for star-shaped memory architectures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and memory-system builders use this skill to add local associative memory discovery, scoring, statistics, and maintenance around memory ID relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local SQLite association metadata about memory ID relationships under the configured database path.

Mitigation: Set CO_OCCURRENCE_DB_PATH to an approved location and apply local access, backup, and retention controls appropriate for the memory data.

Risk: The artifact documentation is primarily Chinese, which may reduce review clarity for teams that do not read Chinese.

Mitigation: Review or translate the documentation before deployment so operators understand configuration, storage behavior, and maintenance commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whoisme007/skills/co-occurrence-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
