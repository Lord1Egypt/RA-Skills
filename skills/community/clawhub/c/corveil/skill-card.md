## Description:

Corveil starts a local Corveil development gateway and configures OpenClaw or Claude Code to route AI requests through it for tracking, guardrails, and passthrough or direct provider access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgershman](https://clawhub.ai/user/dgershman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and run Corveil locally, create a Corveil API key, and route Claude Code or OpenClaw traffic through Corveil for logging, spend tracking, and guardrail testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable remote software before routing AI traffic through it.

Mitigation: Review the release source, verify checksums or signatures, and install only releases you intend to run locally.

Risk: Corveil fully logs routed AI requests and may observe sensitive prompts, responses, and coding-session data.

Mitigation: Use the skill only when local request capture is intended, avoid sensitive production data during testing, and review Corveil logs and retention settings.

Risk: Provider and Corveil API credentials are used in shell commands and local configuration.

Mitigation: Use dev or test keys with low limits, avoid pasting real secrets directly into shell history, rotate keys after testing, and remove temporary configuration when finished.

## Reference(s):

- [Corveil ClawHub Skill Page](https://clawhub.ai/dgershman/skills/corveil)
- [Corveil Documentation](https://corveil.com/docs)
- [Corveil GitHub Releases](https://github.com/radiusmethod/corveil-releases/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; may configure OpenClaw or Claude Code environment settings.]

## Skill Version(s):

1.0.6-20260516 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
