## Description:

Drive a remote chrome-devtools-mcp server over HTTPS using the chrome-devtools CLI so an agent can navigate, screenshot, inspect, or evaluate JavaScript in a browser running on another host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzianisv](https://clawhub.ai/user/dzianisv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to control a trusted remote browser session when local browser automation is unavailable or when the browser must run on another machine such as a tailnet host or CI runner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives a remote browser server and can expose browsing actions, bearer tokens, login credentials, or page data if used with an untrusted endpoint or network path.

Mitigation: Use only a remote browser server the user controls or trusts, avoid sending sensitive credentials unless the endpoint and network path are trusted, and prefer reviewed or pinned package versions.

Risk: Using insecure TLS options can disable certificate verification for remote browser control.

Mitigation: Avoid --insecure for hosted or sensitive endpoints and reserve it only for trusted self-signed environments where the user has accepted the risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dzianisv/skills/chrome-devtools-remote)
- [Publisher Profile](https://clawhub.ai/user/dzianisv)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Markdown]

**Output Format:** [Markdown guidance with bash command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot file paths and browser inspection summaries from a configured remote endpoint.]

## Skill Version(s):

0.26.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
