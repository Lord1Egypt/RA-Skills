## Description:

Query and control Databricks jobs from plain text by checking status, listing recent runs, finding failures, triggering pipelines, browsing Unity Catalog, and running read-only SQL through the Databricks REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerikko](https://clawhub.ai/user/nerikko)

### License/Terms of Use:

MIT

## Use Case:

Developers, data engineers, and operations teams use this skill to inspect Databricks job health, investigate failures, trigger or manage runs, review SLA status, explore catalog objects, and run bounded SQL checks without opening the Databricks UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses powerful Databricks workspace credentials and can trigger, retry, or cancel runs.

Mitigation: Install only from a trusted publisher, use a least-privilege Databricks token, and require human confirmation before run, retry, or cancel actions.

Risk: Misconfigured host or secret exposure could route credentials to the wrong workspace or expose tokens during installation and use.

Mitigation: Set DATABRICKS_HOST only to the intended HTTPS Databricks workspace and avoid running installation or commands in environments containing unrelated secrets.

Risk: The SQL denylist is a best-effort guard and should not be treated as a security boundary.

Mitigation: Enforce read-only access through Databricks permissions and keep DATABRICKS_ALLOW_WRITE_SQL unset unless write SQL is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerikko/skills/databricks-helper)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include job statuses, run IDs, run URLs, error snippets, log snippets, SLA summaries, catalog lists, and bounded tabular SQL results.]

## Skill Version(s):

1.1.0 (source: server release metadata, README, SKILL.md, and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
