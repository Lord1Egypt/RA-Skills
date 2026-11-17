## Description:

Cailianpress Unified provides a single auditable access layer for Cailian Press telegraph data, article details, local persistence, and JSON, text, or Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caimao9539](https://clawhub.ai/user/caimao9539)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query, normalize, store, and reuse Cailian Press telegraph records through one stable interface instead of calling CLS endpoints directly. It supports recent telegraph, highlighted, hot, article-detail, snapshot, and SQLite-backed query workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts CLS/Cailian Press endpoints and stores fetched telegraph or news records locally.

Mitigation: Review endpoint access, local data handling, and retention expectations before installation or scheduled ingestion.

Risk: The raw-log pruning workflow directly deletes audit log rows older than 30 days.

Mitigation: Confirm the required audit-retention period before enabling the prune script or cron example, and keep separate backups if longer retention is needed.

Risk: Security guidance notes operational reliability concerns around dependency pinning and a SQLite binding issue.

Mitigation: Pin dependencies and test or fix the SQLite path in the target environment before relying on scheduled or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caimao9539/skills/cailianpress-unified)
- [README](artifact/README.md)
- [API Contract](artifact/docs/api_contract.md)
- [SQLite Mode](artifact/docs/sqlite_mode.md)
- [Snapshot Mode](artifact/docs/snapshot_mode.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, plain text, Markdown, Python service calls, and shell or cron examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include CLS item fields, source/fallback metadata, local SQLite query results, and retention/pruning operation summaries.]

## Skill Version(s):

0.1.5 (source: server release metadata and CHANGELOG, released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
