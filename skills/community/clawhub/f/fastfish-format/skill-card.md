## Description:

Formats and beautifies WeChat official-account and Xiaohongshu articles with 30 preset styles, Markdown-to-HTML rendering, style selection, and image-workflow guidance; it does not publish content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superxs777](https://clawhub.ai/user/superxs777)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and developers use this skill to normalize WeChat and Xiaohongshu article text, render Markdown into styled HTML, inspect available formatting styles, and get image-workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external formatter can execute third-party Python code and dependencies.

Mitigation: Review the referenced repository and dependencies, pin installation to a reviewed commit or trusted release, and run it in a virtual environment or container without root privileges.

Risk: Optional image-generation workflows may involve API keys.

Mitigation: Keep credentials out of command output and chat responses, store them only in appropriate environment configuration, and avoid commands that print secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superxs777/skills/fastfish-format)
- [fastfish-format repository](https://github.com/superxs777/fastfish-format)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-backed CLI results with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rendered HTML, style identifiers, normalized article text, and image-workflow guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
