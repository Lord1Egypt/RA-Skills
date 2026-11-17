## Description:

Helps an agent manage a user's Feishu calendar by listing events, creating events, checking free/busy status, and refreshing OAuth tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to work with personal Feishu calendars through OAuth-authorized calendar queries, event creation, and availability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Feishu calendar data and create calendar events.

Mitigation: Install only when calendar read and write permissions are intentional, and require clear user confirmation before calendar writes.

Risk: The evidence security summary reports exposed OAuth app secret material and plaintext storage of user OAuth tokens under the skill directory.

Mitigation: Rotate or replace the app secret before use and protect local token files with appropriate filesystem permissions.

## Reference(s):

- [OAuth setup guide](references/oauth-setup.md)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu OAuth credentials and may read or write calendar data depending on the requested action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
