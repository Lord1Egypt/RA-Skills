## Description:

Automates WeChat Official Account article drafting or publishing with title and body entry, AI-generated cover imagery, optional summaries, comment settings, reward settings, and cookie-based login reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiebbs](https://clawhub.ai/user/xiebbs)

### License/Terms of Use:

MIT-0

## Use Case:

External content publishers, operators, and developers use this skill to automate WeChat Official Account article preparation, save drafts, or publish posts with generated imagery and common publication settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly to a connected WeChat Official Account.

Mitigation: Use the draft mode first, review the generated article and cover image, and only run direct publishing from a controlled account and machine.

Risk: The skill stores and reuses login cookies for the WeChat Official Account.

Mitigation: Protect the cookie file as a sensitive login session, restrict local access to it, and delete it when the session should no longer be reused.

Risk: Article content loaded from files is inserted into the editor as formatted HTML.

Mitigation: Use trusted article files only until the insertion path is escaped or sanitized.

Risk: Unattended scheduled publishing can amplify account or content mistakes.

Mitigation: Avoid cron or unattended publishing unless the machine, account, and source content are fully controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiebbs/skills/decleormx-wechat-gzh-publish)
- [Publisher profile](https://clawhub.ai/user/xiebbs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands, command-line arguments, and console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local browser cookies and debug screenshots, and may save drafts or publish posts in the connected WeChat Official Account.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
