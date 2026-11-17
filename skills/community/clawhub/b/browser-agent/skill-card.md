## Description:

Browser Agent controls a local Chrome browser through the Chrome DevTools Protocol and WebSocket connections for navigation, screenshots, element interaction, JavaScript evaluation, and session reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaka4413](https://clawhub.ai/user/kaka4413)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive a real Chrome session for web testing, data collection, content workflows, and cross-platform browser tasks where logged-in state or a visible browser session is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real browser as the user, including authenticated accounts and sensitive pages.

Mitigation: Use a dedicated automation Chrome profile with no personal sessions, and require explicit review before posting, deleting, typing credentials, running JavaScript, or capturing screenshots on sensitive pages.

Risk: Chrome remote debugging and permissive WebSocket origins can expose high-impact browser control if misconfigured.

Mitigation: Keep CDP bound to localhost, avoid wildcard remote origins when possible, close the browser when automation is complete, and do not expose the debugging port to a network.

## Reference(s):

- [Browser Agent API Reference](references/api_reference.md)
- [Chrome DevTools Protocol Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [websocket-client Documentation](https://websocket-client.readthedocs.io/)
- [ClawHub Skill Page](https://clawhub.ai/kaka4413/skills/browser-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and generated browser artifacts such as screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate on an authenticated local browser session and may write screenshot files when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
