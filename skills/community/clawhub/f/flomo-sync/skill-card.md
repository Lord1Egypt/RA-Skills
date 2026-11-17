## Description:

Synchronizes and backs up flomo memos to local Markdown files using a Python script, with incremental sync, attachment handling, and per-memo file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giraffe-tree](https://clawhub.ai/user/giraffe-tree)

### License/Terms of Use:


## Use Case:

Developers and flomo users use this skill to configure and run a local sync workflow that exports flomo notes to Markdown for backup or local knowledge management. It is intended for users who can safely handle a flomo access token and local note exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a flomo access token that can expose account data if pasted into chat, committed to source control, or shared through cloud sync.

Mitigation: Store the token only in a private .flomo.config file, exclude it from git and shared folders, and rotate the token if exposure is suspected.

Risk: The sync writes exported notes, attachments, and a lock file to local disk, which can disclose private memo content if the output folder is public or synced.

Mitigation: Use a dedicated private absolute output directory and exclude exported content from repositories and shared backup locations unless intentionally published.

Risk: Attachment downloads use remote URLs and may write files derived from memo metadata.

Mitigation: Prefer --no-download when attachments are not required, and review downloaded files and output paths before using exports in other workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/giraffe-tree/skills/flomo-sync)
- [flomo web app](https://v.flomoapp.com)
- [flomo API endpoint](https://flomoapp.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one Markdown file per memo, optional local attachment files, and a .flomo.lock state file for incremental sync.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
