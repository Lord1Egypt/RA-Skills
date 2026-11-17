## Description:

clinstagram gives agents a structured Instagram CLI for posting, direct messages, stories, analytics, followers, hashtags, likes, and comments through Meta Graph API and optional private API backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[199-bio](https://clawhub.ai/user/199-bio)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use this skill to let an agent inspect Instagram account status, route commands across available Instagram backends, and perform account workflows such as posting, messaging, analytics, and audience management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an Instagram account and may use private API actions when credentials exist.

Mitigation: Install only for trusted agents and accounts, keep private API credentials scoped to the intended account, and clear stored sessions with auth logout when private access should end.

Risk: Advertised compliance modes may not be a hard boundary if an agent can force --backend private.

Mitigation: Do not rely on official-only mode alone for policy enforcement; restrict agent command permissions or credentials so private backend actions are unavailable when they are not allowed.

Risk: Media URL handling can make unsafe network requests when an agent is given untrusted media URLs.

Mitigation: Use trusted local media paths or vetted URLs, and avoid passing untrusted media URLs to posting or media-message commands.

## Reference(s):

- [clinstagram ClawHub page](https://clawhub.ai/199-bio/skills/clinstagram)
- [clinstagram homepage](https://github.com/199-biotechnologies/clinstagram)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [instagrapi](https://github.com/subzeroid/instagrapi)
- [Typer](https://typer.tiangolo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can emit structured JSON with exit codes, backend_used, remediation, and retry_after fields.]

## Skill Version(s):

0.2.0 (source: evidence.release.version and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
