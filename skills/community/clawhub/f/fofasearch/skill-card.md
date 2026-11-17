## Description:

Fofa Search v1.0 helps agents run FOFA OpenAPI searches in batch, paginate results, and export findings to CSV with optional JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biglizi775](https://clawhub.ai/user/biglizi775)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to query FOFA with an API key and search expression, then export selected fields for asset discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FOFA API keys and queries can be sent to a user-supplied API URL.

Mitigation: Use the default FOFA endpoint and avoid untrusted --base-url values.

Risk: FOFA API keys may be exposed if stored in repository files or command history.

Mitigation: Provide keys through environment variables or secure local storage and avoid committing secrets.

Risk: Unpinned Python dependencies can change before operational use.

Mitigation: Review and pin dependencies before deploying the skill in sensitive environments.

## Reference(s):

- [FOFA](https://fofa.info)
- [ClawHub skill page](https://clawhub.ai/biglizi775/skills/fofasearch)
- [Publisher profile](https://clawhub.ai/user/biglizi775)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples for CSV and optional JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local CSV files by default and optional JSON files when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
