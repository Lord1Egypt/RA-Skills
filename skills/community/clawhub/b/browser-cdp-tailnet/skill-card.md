## Description:

Connects an agent to a detached shared Chromium browser exposed through a tailnet Chrome DevTools Protocol endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to connect to a shared remote Chromium browser over a tailnet CDP endpoint instead of launching a local browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared persistent Chromium session can expose sensitive browser state across users or tasks.

Mitigation: Use only for intentional shared-browser workflows; avoid confidential browsing and personal or business accounts unless access is isolated and session data is cleared after use.

Risk: Agents receive broad control over a remote browser reachable through the tailnet CDP endpoint.

Mitigation: Limit use to trusted agents and users with approved tailnet access, and run a small probe before relying on the browser for a task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lotfinity/skills/browser-cdp-tailnet)

## Skill Output:

**Output Type(s):** [guidance, configuration, code, shell commands]

**Output Format:** [Markdown guidance with endpoint values and connection examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser connection guidance for an existing shared Chromium CDP endpoint; it does not create a new browser session.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
