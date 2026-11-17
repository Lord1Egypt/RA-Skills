## Description:

1Password UI tab for OpenClaw dashboard. Manage secrets, credential mappings, and auth state from the Control UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to add a 1Password dashboard tab for checking account status, signing in, browsing vault metadata, and mapping 1Password items to skill configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret-reading gateway methods can expose vault values if the gateway is reachable by untrusted callers.

Mitigation: Install only on a trusted, loopback-only or strongly authenticated gateway, and enforce per-skill secret allowlists before relying on it.

Risk: The backend example includes a command-injection risk when invoking the 1Password CLI through shell execution.

Mitigation: Patch the backend to avoid shell execution and pass CLI arguments through an argument-vector process API.

Risk: 1Password Connect tokens can grant vault access.

Mitigation: Use narrowly scoped vault and token permissions, and do not place Connect tokens in checked-in compose files or repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/1password-ui)
- [1Password CLI documentation](https://developer.1password.com/docs/cli)
- [1Password Connect documentation](https://developer.1password.com/docs/connect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual installation steps and reference files for OpenClaw UI and gateway integration.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
