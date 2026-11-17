## Description:

Manages Forge AI articles, evaluations, tags, file uploads, and authentication through the Forge AI API when the user explicitly invokes /forge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scemoon](https://clawhub.ai/user/scemoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to manage Forge AI articles, evaluations, tags, uploads, and account session actions from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and session tokens can be exposed through shell history, process listings, shared folders, commits, or backups.

Mitigation: Use only trusted Forge accounts, avoid entering real passwords directly in shell commands, and keep .forgeai/session.json out of shared folders, source control, and backups.

Risk: The skill can perform account-changing Forge AI actions for articles, evaluations, tags, and file uploads.

Mitigation: Review JSON request bodies, selected files, and account context before running create, update, upload, or tag mutation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scemoon/skills/forge-skill)
- [Forge AI API endpoint](https://cloud1-2gavd8kj8a1ce021.service.tcloudbase.com/api/forge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .forgeai state files and call Forge AI API endpoints.]

## Skill Version(s):

1.2.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
