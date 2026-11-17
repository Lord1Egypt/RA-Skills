## Description:

Query and curate knowledge-base using ByteRover CLI. Use `brv query` for knowledge retrieval, `brv curate` for adding context, and `brv push/pull` for syncing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byteroverinc](https://clawhub.ai/user/byteroverinc)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to retrieve, curate, push, and pull project knowledge through the ByteRover CLI in headless workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a ByteRover API key for authentication.

Mitigation: Provide API keys through a secure secret mechanism rather than pasting them into chat or shell history.

Risk: The installation metadata references an unpinned npm CLI package.

Mitigation: Install only if ByteRover and the npm package source are trusted, and prefer a pinned or reviewed CLI version where possible.

Risk: Push, pull, and reinitialization actions can upload, download, change, or delete project knowledge.

Mitigation: Approve push, pull, and reinitialization actions only after confirming the affected team, space, branch, and project knowledge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/byteroverinc/skills/byterover-headless)
- [ByteRover API key settings](https://app.byterover.dev/settings/keys)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use `--headless --format json` for automation; push operations use `-y` only after user approval.]

## Skill Version(s):

1.6.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
