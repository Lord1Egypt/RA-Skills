## Description:

Helps agents administer Dropbox Business teams, including members, groups, team folders, devices, audit logs, sharing, and file requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Dropbox Business administrators use this skill to inspect and manage team members, groups, folders, devices, sharing, and audit activity through an authorized connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative changes or deletions could alter team access or remove resources.

Mitigation: Use the least-privileged admin account and scopes; confirm exact resource identifiers and obtain explicit approval before writes or deletions.

Risk: Access to individual members' files could expose sensitive information.

Mitigation: Access member files only for a clear, explicitly requested business purpose.

Risk: Automations or destinations can continue acting on or forwarding data after setup.

Mitigation: Review active functions, triggers, and destinations, and delete those no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/dropbox-business)
- [Maton](https://maton.ai)
- [Dropbox Business API documentation](https://www.dropbox.com/developers/documentation/http/teams)
- [Dropbox team administration guide](https://developers.dropbox.com/dbx-team-administration-guide)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize authorized API results.]

## Skill Version(s):

1.2.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
