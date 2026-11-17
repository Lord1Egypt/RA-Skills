## Description:

This skill uses Playwriter to control a user-signed-in Chrome browser and ask AI assistants such as Gemini for expert advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13801201404-sys](https://clawhub.ai/user/13801201404-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents can use this skill to connect to an already logged-in Chrome session, send questions to browser-based AI assistants, and retrieve the resulting advice. It is most relevant when the target assistant requires an existing authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attaches automation to a logged-in Chrome session with broad browser scope, which can expose private pages or account actions if used carelessly.

Mitigation: Use a separate browser profile or low-risk account, confirm the target URL and prompt before sending, avoid sensitive pages, and delete screenshots that may contain private data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13801201404-sys/skills/ask-expert-playwriter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash and JavaScript command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides browser automation steps for Playwriter sessions and Chrome extension setup.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
