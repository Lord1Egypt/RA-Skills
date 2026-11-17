## Description:

A modern text-based browser that renders web pages in the terminal using headless Firefox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers, engineers, and terminal users use this skill to launch Browsh, open URLs in a text-based browser, and browse web content through Firefox from a PTY session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on separately installed browsh and firefox binaries.

Mitigation: Install browsh and firefox only from trusted sources and confirm both binaries are expected before use.

Risk: Running Browsh browses the web through Firefox.

Mitigation: Use it only for URLs and browsing sessions appropriate for the user's environment and security posture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/browsh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browsh and firefox binaries in PATH and a PTY session for the TUI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
