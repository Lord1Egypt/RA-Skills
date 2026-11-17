## Description:

Control a remote browser through Claw Relay using a CLI client for navigation, authenticated browsing, clicking, form filling, screenshots, page content capture, and JavaScript evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreagriffiths11](https://clawhub.ai/user/andreagriffiths11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need controlled access to a user's real browser session from environments that can run shell commands but do not support MCP. It supports browser navigation, interaction, page inspection, screenshots, and optional JavaScript execution through a relay-authenticated CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real logged-in browser session.

Mitigation: Install only when authenticated browser control is required, and use narrow relay scopes, explicit site allowlists, rate limits, and audit logs.

Risk: Relay tokens and browser traffic can be exposed if configured unsafely.

Mitigation: Prefer wss:// relay URLs, store tokens in environment variables or secret storage, and avoid passing tokens on the command line.

Risk: JavaScript evaluation and screenshots can expose or change sensitive page state.

Mitigation: Avoid evaluate unless explicitly needed, review actions before use on sensitive sites, and save screenshots only to low-risk paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreagriffiths11/skills/claw-relay-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples; relay actions return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each CLI invocation connects, authenticates, performs one browser action, prints JSON, and exits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
