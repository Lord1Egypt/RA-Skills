## Description:

Fetches LLM benchmarks and pricing from the Artificial Analysis API and syncs them to a Feishu Bitable model catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neymar011ren](https://clawhub.ai/user/neymar011ren)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, solution, and developer teams use this skill to fetch current LLM benchmark, pricing, speed, and model metadata from Artificial Analysis and maintain a Feishu Bitable catalog for review and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled bitable-config.json contains a prefilled Feishu app_token and table_id, so an agent could read or update a Bitable destination the user did not choose.

Mitigation: Remove or replace the bundled destination values before use, confirm the exact Feishu app and table with the user, and operate only on that explicit destination.

Risk: The workflow requires an Artificial Analysis API key and can read it from a local credential file.

Mitigation: Prefer ARTIFICIAL_ANALYSIS_API_KEY for temporary use or keep any credential file private with restrictive permissions, and never include the key in shared output.

Risk: Repeated full refreshes can consume the Artificial Analysis free API quota.

Mitigation: Reuse the cached llms-latest.json data unless the user explicitly asks to refresh, and avoid unnecessary repeated pulls.

## Reference(s):

- [Feishu Bitable setup fields](references/bitable-setup.md)
- [Artificial Analysis API Reference](https://artificialanalysis.ai/api-reference)
- [Artificial Analysis LLM models endpoint](https://artificialanalysis.ai/api/v2/data/llms/models)
- [Artificial Analysis Insights Platform](https://artificialanalysis.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated JSON data files, and Feishu Bitable records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Artificial Analysis API key and Feishu Bitable tools; uses cached API results and batch record operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
