## Description:

Helps agents manage Dropbox files and folders, search content, and retrieve metadata through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Dropbox users and developers use this skill to inspect and organize files, search content, and manage sharing or user-approved automations in a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account access may expose or change Dropbox files and sharing settings.

Mitigation: Authorize the intended account with the narrowest available scopes, and confirm the account and exact target before writing, deleting, uploading, or sharing.

Risk: Triggers and destinations can create ongoing automated data flows.

Mitigation: Review the trigger, destination, and data sent, and obtain separate user approval before enabling automation.

## Reference(s):

- [ClawHub Dropbox skill](https://clawhub.ai/byungkyu/skills/dropbox-api)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Dropbox HTTP API overview](https://www.dropbox.com/developers/documentation/http/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide instructions for approved Dropbox operations and automations.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
