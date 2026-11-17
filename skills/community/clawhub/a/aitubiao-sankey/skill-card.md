## Description:

Generates AI-assisted Sankey flow diagrams from pasted or uploaded tabular data through the Aitubiao API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitubiao](https://clawhub.ai/user/aitubiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn tabular flow data into Aitubiao Sankey chart projects, then view or export supported formats after authentication, quota checks, and user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart data is sent to Aitubiao's API and an API key is stored locally.

Mitigation: Install only if sending chart data to Aitubiao is acceptable, use an API key copied from the official Aitubiao console, and remove ~/.aitubiao/credentials when it is no longer needed.

Risk: The security evidence reports that credential handling can execute injected shell code.

Mitigation: Avoid credential content from untrusted messages, recreate credentials from the official console if there is any doubt, and review the local credentials file before use.

Risk: The bundled CLI exposes broader actions than the Sankey-specific workflow.

Mitigation: Use only the documented authentication, quota, create-sankey, and project-download commands needed for the requested Sankey workflow.

Risk: The security guidance calls out export/download path and attachment URL caution.

Mitigation: Use explicit writable output paths, avoid source directories, and report the saved path returned by the CLI after file integrity checks pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitubiao/skills/aitubiao-sankey)
- [Aitubiao API key management](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)
- [Aitubiao workspace](https://app.aitubiao.com/workspace)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline shell commands, JSON API results, project links, and optional downloaded export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.aitubiao.com, local Aitubiao API credentials, curl, jq, and explicit user confirmation before creating projects.]

## Skill Version(s):

1.2.5 (source: server release metadata; artifact metadata version 1.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
