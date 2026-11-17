## Description:

Feishu Reading Notes turns shared public article links into categorized Markdown reading notes saved to Feishu Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxc168](https://clawhub.ai/user/yxc168)

### License/Terms of Use:

MIT-0

## Use Case:

Users who collect articles use this skill to fetch supported public links, organize them by topic, and produce dated Markdown reading notes for storage in Feishu Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use embedded Feishu credentials, fixed cloud folders, and a fixed notification recipient.

Mitigation: Install only after replacing the Feishu app credentials, folder targets, and recipient with values controlled by the deploying user or organization.

Risk: The workflow can delete or overwrite same-named files in configured Feishu folders.

Mitigation: Require explicit confirmation before deleting or replacing files, and keep backup or version history enabled for reading-note folders.

Risk: Category and folder metadata is embedded directly in the skill text.

Mitigation: Move deployment-specific category mappings and folder tokens to external configuration reviewed by the owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxc168/skills/feishu-reading-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reading-note files with metadata, summaries, quotes, and source content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also propose browser extraction steps, Feishu upload actions, and category updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
