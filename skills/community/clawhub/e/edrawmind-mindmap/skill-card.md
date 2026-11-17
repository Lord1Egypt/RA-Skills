## Description:

Generates professional mind maps from natural language topics, Markdown documents, code architecture notes, requirements, or other structured text through the EdrawMind API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

Proprietary Software License

## Use Case:

Developers, analysts, and content creators use this skill to convert topics, outlines, Markdown files, project structures, and requirements into editable EdrawMind mind maps with layout, theme, background, and hand-drawn style options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown content is sent to EdrawMind's online API and may include sensitive information.

Mitigation: Use the skill only with content approved for upload to EdrawMind's service, and avoid secrets, credentials, private documents, or confidential source material.

Risk: The documented --text shell-command pattern can execute local shell commands if an agent interpolates untrusted Markdown into a command line.

Mitigation: Prefer stdin or a safely created input file for generated or untrusted Markdown, and quote or avoid command-line interpolation when using --text.

Risk: Custom API endpoints, --insecure transport, or command-line API keys can expose data or credentials to untrusted destinations or local process history.

Mitigation: Avoid --insecure, custom --api-url, and command-line API keys unless the endpoint and environment are trusted; prefer EDRAWMIND_API_KEY for credentials.

## Reference(s):

- [Markdown input format](artifact/references/markdown-format.md)
- [Style parameter guide](artifact/references/style-guide.md)
- [CLI tool reference](artifact/references/tool-reference.md)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/edrawmind-mindmap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and returned file_url, thumbnail_url, or JSON response data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate editable mind-map links and thumbnail previews; supports layout, theme, background, region, API key, and output options.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
