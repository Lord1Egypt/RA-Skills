## Description: <br>
Provides CLI guidance for managing AFFiNE documents, tags, folders, collections, files, databases, comments, journals, and workspaces on cloud or self-hosted deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodcoal](https://clawhub.ai/user/woodcoal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent prepare AFFiNE CLI commands for workspace, document, tag, folder, collection, file, database, comment, and journal workflows. It is suited to users who intentionally want an agent-assisted CLI path for changing AFFiNE cloud or self-hosted workspace content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to AFFiNE workspace content, including deletion, publishing, permanent cleanup, replacement, and bulk database operations. <br>
Mitigation: Use a limited token where possible and require explicit user confirmation before destructive, publishing, replacement, or bulk operations. <br>
Risk: AFFINE_API_TOKEN values and workspace identifiers may be exposed if placed directly in shared command text or logs. <br>
Mitigation: Prefer environment variables or a secure secret store, avoid inline tokens in shared transcripts, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub AFFiNE Skill](https://clawhub.ai/woodcoal/affine) <br>
- [affine-cli Project Page](https://github.com/woodcoal/affine-cli) <br>
- [AFFiNE Documentation](https://deepwiki.com/toeverything/AFFiNE) <br>
- [AFFiNE Token Settings](https://app.affine.pro/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variable names, AFFiNE workspace identifiers, document IDs, database IDs, and confirmation prompts for destructive operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
