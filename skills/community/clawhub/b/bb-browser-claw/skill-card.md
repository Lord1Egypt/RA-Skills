## Description:

Automates a host Chromium browser through the bb-browser daemon and Chrome DevTools Protocol for real-session web tasks across search, social, finance, research, translation, and direct browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatgptnexus](https://clawhub.ai/user/chatgptnexus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a real Chromium session through bb-browser for web research, social media, finance, job search, translation, and direct page control while reusing logged-in browser state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent act through a real logged-in browser profile and access private account data.

Mitigation: Use a dedicated Chrome or Chromium profile with no unrelated logins, saved credentials, or private sessions.

Risk: Direct browser control, JavaScript evaluation, and network capture can expose sensitive page content or credentials.

Mitigation: Approve each target site and private resource explicitly, and avoid eval or network capture unless it is narrowly required.

Risk: The skill depends on a host daemon, browser extension, and binary outside the skill artifact.

Mitigation: Verify the bb-browser binary, daemon, and extension from a trusted source before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chatgptnexus/skills/bb-browser-claw)
- [Publisher profile](https://clawhub.ai/user/chatgptnexus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets plus JSON-producing bb-browser commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a host bb-browser daemon, the browser extension, and active Chromium sessions; commands may access logged-in browser data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
