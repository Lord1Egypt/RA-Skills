## Description:

Analyzes user-specified OSS data through Alibaba Cloud AnalyticDB for MySQL Serverless with read-only, bounded Presto SQL and guarded source selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to discover, query, and analyze user-authorized OSS paths through an ADB Serverless workspace. It favors registered Hive metadata when available and falls back to bounded OSS table functions only within the confirmed scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only cloud queries can still expose sensitive OSS data or incur query costs.

Mitigation: Verify the endpoint or region, workspaceId, OSS scope, and planned SQL before live use, and keep queries bounded with explicit scopes, filters, and limits.

Risk: Runtime access tokens could be exposed if copied into commands, logs, SQL, files, or responses.

Mitigation: Use a per-request token or ADB_ACCESS_TOKEN without printing or persisting it, and pass credentials only through runtime parameters or child-process environment variables.

Risk: Direct OSS file inference may fail or scan a broader path than intended if the source scope is ambiguous.

Mitigation: Discover registered Hive metadata first, restrict direct table-function use to confirmed prefixes or partitions, and stop on terminal source or format-inference errors.

## Reference(s):

- [Query API](references/query-api.md)
- [OSS Table Functions](references/oss-table-functions.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline Presto SQL, shell commands, and redacted result or error summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the analysis result directly; writes files only when the user's analysis goal explicitly requests a deliverable.]

## Skill Version(s):

0.0.1-beta.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
