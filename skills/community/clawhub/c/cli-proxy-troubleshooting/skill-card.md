## Description:

Helps agents troubleshoot CLI Proxy API configuration, authentication, model registration, request encoding, and timeout failures with source-aware diagnostic steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17329971](https://clawhub.ai/user/17329971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose CLI Proxy API failures involving unknown model providers, missing models, API key or auth-dir loading, malformed request bodies, network timeouts, and image-generation support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting steps may involve proxy URLs, API keys, auth directories, and logs that can contain sensitive information.

Mitigation: Use your own proxy URL, keep API keys and auth file contents private, and redact logs before sharing diagnostic output.

Risk: The skill provides documentation-only guidance, so incorrect local configuration or network assumptions can still lead to failed requests.

Mitigation: Validate changes against the local CLI Proxy configuration and logs before relying on the resulting diagnosis.

## Reference(s):

- [CLI Proxy API homepage](https://github.com/stainless-codex/cli-proxy-api)
- [CLI Proxy source architecture](references/source-architecture.md)
- [ClawHub skill page](https://clawhub.ai/17329971/skills/cli-proxy-troubleshooting)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown troubleshooting guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only diagnostic workflow; no executable scripts are bundled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
