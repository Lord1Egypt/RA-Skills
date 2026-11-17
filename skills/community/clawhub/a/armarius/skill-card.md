## Description:

Armarius provides always-on prompt-injection blocking guidance for agents by treating external content as data, not instructions, and logging suspicious injection attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatlantis](https://clawhub.ai/user/tatlantis)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add prompt-injection handling guidance to agent workflows, especially when working with tool outputs, documents, web pages, email, or other untrusted content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change how the agent treats all tool results and documents during a session.

Mitigation: Review the skill before installing and test it in an isolated session before using it in normal workflows.

Risk: The skill may print suspicious content back into chat verbatim, which can expose confidential data.

Mitigation: Avoid using it around confidential data unless logging is changed to redact secrets and limit excerpts.

Risk: The README includes external package and demo commands.

Mitigation: Pin or isolate external packages and demo commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tatlantis/skills/armarius)
- [Armarius homepage](https://github.com/tatlantis/armarius)
- [Armarius issues](https://github.com/tatlantis/armarius/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include defensive handling guidance and logging recommendations for suspicious external content.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
