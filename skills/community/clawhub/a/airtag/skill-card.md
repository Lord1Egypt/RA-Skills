## Description:

Give your agent controlled access to all AirTags in your Apple account to locate items, run diagnostics, and recover setup failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to let an agent assist with AirTag and Find My workflows, including item location, recovery planning, connector setup, diagnostics, battery checks, and unknown-AirTag safety handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle sensitive AirTag item-location details and incident history.

Mitigation: Approve each location pull or local write deliberately, and periodically review or delete ~/airtag/ notes that contain locations, safe zones, or incident history.

Risk: Programmatic API Mode depends on high-trust third-party private-protocol tooling.

Mitigation: Prefer Direct App Control or Shared Link Mode when possible, and use API Mode only with a connector the user explicitly trusts.

## Reference(s):

- [AirTag ClawHub Page](https://clawhub.ai/ivangdavila/skills/airtag)
- [AirTag Homepage](https://clawic.com/skills/airtag)
- [iCloud Find My](https://www.icloud.com/find)
- [Apple Find My Shared Item Access](https://find.apple.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise procedural guidance and optional inline commands or configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create user-approved local AirTag notes under ~/airtag/ when the user explicitly confirms.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
