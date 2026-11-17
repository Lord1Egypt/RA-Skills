## Description:

佳明国际账号数据同步到国内账号（基于 garminconnect 开源库）

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucetangc](https://clawhub.ai/user/brucetangc)

### License/Terms of Use:

MIT-0

## Use Case:

Garmin Connect users use this skill to sync recent activity data from an international Garmin account into a China Garmin account by downloading FIT files and uploading them to Garmin Connect China.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command execution can be influenced through unvalidated arguments.

Mitigation: Use execFileSync or spawnSync with validated numeric arguments before deployment.

Risk: The skill handles sensitive Garmin credentials, tokens, and activity files.

Mitigation: Document token and FIT-file storage locations, how to delete them, and review local storage permissions before use.

Risk: Dependency behavior may change because garminconnect is not pinned in the release evidence.

Mitigation: Pin and review the garminconnect dependency before installing in a production or commercial environment.

Risk: Broad triggers and automatic sync behavior can cause unintended account data movement.

Mitigation: Narrow triggers and require explicit confirmation before starting synchronization.

## Reference(s):

- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
- [ClawHub skill page](https://clawhub.ai/brucetangc/skills/garmin-connect-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command results, status summaries, configuration prompts, and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs sync, status, list, and authentication-test flows using configured Garmin credentials.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
