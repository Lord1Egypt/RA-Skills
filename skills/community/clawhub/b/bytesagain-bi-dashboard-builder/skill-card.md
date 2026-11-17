## Description:

Build BI dashboard specs, chart plans, SQL queries, and Apache Superset chart JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and BI practitioners use this skill to draft dashboard plans, KPI dictionaries, chart definitions, SQL templates, dataset contracts, QA notes, and Apache Superset chart JSON from dashboard goals, metrics, and dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL templates or Superset JSON may be incorrect for a specific schema, database dialect, or BI environment.

Mitigation: Review and adapt generated queries and chart JSON before execution or import.

Risk: Untrusted table names, metric names, dimensions, or chart types could produce unsafe or misleading draft output in automation.

Mitigation: Use trusted inputs, validate names against an allowlist, and keep generated artifacts in a review step before operational use.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/bytesagain-bi-dashboard-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, SQL, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local dashboard drafts and should be reviewed before database execution or BI import.]

## Skill Version(s):

1.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
