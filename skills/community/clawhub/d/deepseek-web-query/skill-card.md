## Description:

Uses a browser-controlled DeepSeek web session to send internet query requests, detect login state, reuse the browser session, and return extracted Markdown answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andeymei](https://clawhub.ai/user/andeymei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route prompt-prefixed or web-research questions to a logged-in DeepSeek browser session and receive the raw answer content. It is intended for current information lookup, general knowledge questions, code-related research, text analysis, translation, and summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and page interactions are sent through a logged-in DeepSeek browser session.

Mitigation: Use the skill only for data appropriate to send to DeepSeek, and avoid confidential or regulated content unless approved for that environment.

Risk: Clipboard-based extraction may expose sensitive clipboard or session content.

Mitigation: Clear sensitive clipboard contents before use and prefer extraction methods that scope collection to the latest DeepSeek answer.

Risk: The recovery flow may configure browser tooling with an unpinned MCP dependency.

Mitigation: Review the configuration before installation, pin the MCP package version, and require confirmation before replacing existing MCP settings.

## Reference(s):

- [DeepSeek Chat](https://chat.deepseek.com/)
- [ClawHub skill page](https://clawhub.ai/andeymei/skills/deepseek-web-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown answers, JSON command plans, and inline shell or browser-control commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a logged-in DeepSeek browser session and clipboard access; output is intended to preserve DeepSeek's raw response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
