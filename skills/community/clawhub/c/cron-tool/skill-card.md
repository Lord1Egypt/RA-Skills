## Description:

Perform cron-tool operations from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to manage user crontab entries from a command-line workflow, including listing, adding, disabling, backing up, restoring, and editing scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron changes can persistently modify, disable, or erase scheduled jobs.

Mitigation: Back up the crontab before use, review proposed changes carefully, and avoid running the skill as a privileged or service account.

Risk: Security evidence reports weak disclosure and an unsafe removal path for remove, enable, disable, and edit operations.

Mitigation: Do not allow automated agent use of remove, enable, disable, or edit until the removal bug and confirmation gaps are fixed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or invoke cron-management commands that alter persistent scheduled jobs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
