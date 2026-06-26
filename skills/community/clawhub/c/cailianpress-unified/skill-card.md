## Description: <br>
Provides a unified, auditable access layer for Cailian Press telegraph data, including normal, red-level, hot, and article-detail queries with JSON, text, and Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caimao9539](https://clawhub.ai/user/caimao9539) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to fetch, store, normalize, and query CLS telegraph news through a single reusable interface instead of calling multiple CLS endpoints directly. It supports live queries, SQLite-backed local history, article-detail completion, and downstream report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls public CLS endpoints and may maintain a local news database. <br>
Mitigation: Install it only when that data access pattern is intended, and review the documented endpoint strategy before enabling scheduled ingestion. <br>
Risk: Suggested cron jobs can create recurring network calls and local data updates. <br>
Mitigation: Enable scheduled ingestion and pruning deliberately, with an operating cadence that matches the deployment environment. <br>
Risk: Raw ingest logs are documented for online retention for 30 days before direct deletion. <br>
Mitigation: Confirm the retention policy meets audit needs before relying on raw logs for long-term review. <br>
Risk: The release depends on the unpinned requests package. <br>
Mitigation: Pin and lock the dependency before production deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caimao9539/cailianpress-unified) <br>
- [API contract](docs/api_contract.md) <br>
- [SQLite mode](docs/sqlite_mode.md) <br>
- [Snapshot mode](docs/snapshot_mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, plain text, Markdown, Python CLI commands, and cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can query live CLS endpoints or a local SQLite store; local raw ingest logs are documented for 30-day online retention before deletion.] <br>

## Skill Version(s): <br>
0.1.5 (source: release evidence and CHANGELOG, released 2026-03-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
