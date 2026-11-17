## Description:

Fetches Markdown content from Caoliao QR code short links that match the supported qr61.cn two-segment URL format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbjedi](https://clawhub.ai/user/nbjedi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve Markdown content from supported Caoliao QR code short links and return it to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches remote Markdown from qr61.cn links supplied by the user.

Mitigation: Validate that links match the supported qr61.cn URL format before fetching content.

Risk: Fetched Markdown may contain untrusted instructions or misleading content.

Mitigation: Review returned Markdown as untrusted data before following or acting on its contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nbjedi/skills/caoliao-qrcode-markdown-content-skill)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown content or concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows redirects when fetching remote Markdown; returned content should be treated as untrusted remote data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
