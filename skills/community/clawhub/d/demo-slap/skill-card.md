## Description:

Generate CS2 highlights and fragmovies from demos using the Demo-Slap API, with optional Leetify integration and Demo-Slap match history fallback for recent match selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeminay](https://clawhub.ai/user/jeminay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw environments to select CS2 matches, analyze demos, render highlight clips or fragmovies, and deliver MP4 clip URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive API keys or runtime data may be kept in local configuration or data files.

Mitigation: Prefer environment-injected API keys, restrict access to the data directory, and avoid storing secrets in data/config.json.

Risk: Untrusted job, chat, and clip data can be published into OpenClaw system events.

Mitigation: Use typed events or validated and redacted fields before enabling automatic delivery actions.

Risk: Background watchdog jobs can continue beyond the intended render or analysis run if left enabled.

Mitigation: Avoid watchdog jobs when possible; when needed, scope them to the active run and disable them after terminal delivery or error.

## Reference(s):

- [Demo Slap on ClawHub](https://clawhub.ai/jeminay/skills/demo-slap)
- [Demo-Slap API Swagger](https://api-doc.demo-slap.net/)
- [Demo-Slap API](https://api.demo-slap.net)
- [Leetify Public API](https://api-public.cs-prod.leetify.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON script output, runtime state files, and MP4 clip URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEMOSLAP_API_KEY; can use LEETIFY_API_KEY for match discovery and OpenClaw for background notification workflows.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
