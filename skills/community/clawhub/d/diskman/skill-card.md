## Description:

DiskMan helps agents scan directories, analyze disk usage, recommend cleanup or migration actions, and manage disk space with rule-based or optional AI-assisted guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyy259](https://clawhub.ai/user/heyy259)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use DiskMan to find large directories, classify cleanup or migration opportunities, and prepare safer disk-space management actions. It is most useful when an agent needs to explain risk, request confirmation, and produce path-specific recommendations before file-system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup tools can delete broad local directories.

Mitigation: Require explicit human approval, preview deletion with dry-run mode first, and avoid using the skill on important directories without a backup.

Risk: Migration tools can move data and replace the original path with a symbolic link or junction.

Mitigation: Confirm source and target paths, ensure target storage has sufficient space, close programs using the directory, and keep a backup before migration.

Risk: Optional AI analysis can send directory metadata and user context to a configured provider.

Mitigation: Do not configure AI credentials unless sharing that metadata with the provider is acceptable; use rule-based analysis when privacy or network exposure is a concern.

Risk: Running the MCP server with elevated privileges increases the impact of accidental cleanup or migration operations.

Mitigation: Run the MCP server with normal user privileges and restrict use to directories the user intends the agent to inspect or manage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heyy259/skills/diskman)
- [Publisher Profile](https://clawhub.ai/user/heyy259)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON configuration snippets, risk levels, recommended actions, paths, and sizes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include dry-run cleanup previews, migration confirmations, AI provider status, and structured scan or analysis results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
