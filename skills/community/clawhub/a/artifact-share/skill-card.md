## Description:

Use when you need to share static web content (HTML/CSS/JS/images) via a publicly accessible URL, including uploading generated files, creating shareable pages, or deploying single-page web artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavin-yyc](https://clawhub.ai/user/gavin-yyc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload static HTML/CSS/JS/image artifacts to a third-party static sharing service and return public preview links, project identifiers, and optional QR-code Markdown to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a permanent API key in plaintext local configuration, and that key can create, update, or delete hosted projects.

Mitigation: Keep the key out of chat, logs, repositories, and shared machines; review the local config before support handoff or workspace sharing.

Risk: Device identifiers based on username and hostname can disclose local identity information to the third-party service.

Mitigation: Use a random device ID and store it locally instead of sending username@hostname.

Risk: Uploaded static content may be publicly accessible when no project password is set.

Mitigation: Avoid uploading private content unless password protection is explicitly enabled and the intended audience is known.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gavin-yyc/skills/artifact-share)
- [Artifact Share Service](https://artifact-share.youthol.top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with URLs, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public share links, project identifiers, API responses, and QR-code data URIs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
