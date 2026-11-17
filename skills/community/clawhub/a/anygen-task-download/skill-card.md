## Description:

AnyGen: Download artifacts from a completed task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertilico2001](https://clawhub.ai/user/supertilico2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to download files or thumbnails from completed AnyGen tasks, choosing all artifacts or named files and a local output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command writes downloaded task artifacts to disk, so an unintended output directory can place files where the user does not expect.

Mitigation: Confirm the output directory before running the command and review the returned JSON file paths after download.

Risk: The skill depends on @anygen/cli and ANYGEN_API_KEY, so an unexpected CLI package or overly broad credential can increase supply-chain or credential exposure.

Mitigation: Verify the CLI package publisher before installing, pin or lock the reviewed CLI version where possible, and use a narrowly scoped API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supertilico2001/skills/anygen-task-download)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with bash commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the anygen CLI and ANYGEN_API_KEY; the command writes downloaded artifacts to the selected local directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
