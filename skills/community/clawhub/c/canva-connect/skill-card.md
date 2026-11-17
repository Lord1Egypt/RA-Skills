## Description:

Manage Canva designs, assets, and folders via the Connect API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolmanns](https://clawhub.ai/user/coolmanns)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation-focused Canva users use this skill to list, organize, create, export, upload, and autofill Canva resources through the Connect API. It is best suited for asset pipelines, export automation, design organization, and brand template autofill workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants and stores powerful Canva permissions, including write-capable access to designs, assets, folders, brand templates, and profile data.

Mitigation: Use it only with a Canva integration and account you are comfortable granting those permissions to, and avoid sensitive Canva accounts unless the integration has been reviewed.

Risk: OAuth tokens are stored locally in ~/.clawdbot/canva-tokens.json as plaintext secrets.

Mitigation: Restrict local file permissions, keep the state directory out of shared backups and logs, and rotate or revoke Canva tokens if exposure is suspected.

Risk: Delete and upload commands can remove Canva resources or send local files to Canva without an additional confirmation step.

Mitigation: Review generated commands before execution, especially delete and upload actions, and test workflows with non-sensitive resources first.

## Reference(s):

- [Canva Connect documentation](https://canva.dev/docs/connect/)
- [Canva developer integrations](https://canva.com/developers/integrations)
- [Canva Connect API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolmanns/skills/canva-connect)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and CLI/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CANVA_CLIENT_ID and CANVA_CLIENT_SECRET; OAuth tokens are stored locally for Canva API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
