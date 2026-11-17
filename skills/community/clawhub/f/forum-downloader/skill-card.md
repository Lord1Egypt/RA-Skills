## Description:

Forum Downloader helps agents batch-download images or videos from forum posts into a user-selected folder, including forums that require proxy access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zitao666](https://clawhub.ai/user/zitao666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare forum media downloads from a post URL into a chosen local folder. It is most useful when the forum requires a user-provided proxy or uses GBK/GB2312-encoded pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save many untrusted remote forum files to a local folder.

Mitigation: Use a contained download folder and confirm the target URL and expected download scope before running generated commands.

Risk: Downloads may route through a user-provided proxy.

Mitigation: Provide only a proxy you trust and avoid embedding sensitive credentials in generated commands or shared logs.

## Reference(s):

- [ClawHub Forum Downloader skill page](https://clawhub.ai/zitao666/skills/forum-downloader)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell commands or script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided forum URL, trusted proxy address, and destination folder.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
