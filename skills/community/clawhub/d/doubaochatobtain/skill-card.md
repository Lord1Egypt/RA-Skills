## Description:

Extracts the full text from Doubao chat thread pages by using browser automation and DOM extraction to work around virtual scrolling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenyang-x](https://clawhub.ai/user/zenyang-x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need to capture the full visible text of a Doubao conversation thread and save it locally for follow-on review or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned browser automation dependency.

Mitigation: Review or pin the agent-browser dependency before installing and running the workflow.

Risk: Extracted conversation data may contain sensitive content and is saved as persistent local data.

Mitigation: Run the workflow only on Doubao conversations intended for extraction and choose a private output location instead of a shared temporary path.

## Reference(s):

- [agent-browser npm package](https://www.npmjs.com/package/agent-browser)
- [DoubaoChatObtain on ClawHub](https://clawhub.ai/zenyang-x/skills/doubaochatobtain)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; extracted conversation content is written as a plain text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses agent-browser JSON output as input to a parser script and persists the extracted transcript to a user-selected local path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
