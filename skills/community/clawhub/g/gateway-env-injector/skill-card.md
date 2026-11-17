## Description:

Injects API keys from 1Password into macOS LaunchAgent plists for OpenClaw gateway configuration using PlistBuddy and the op CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure OpenClaw gateway LaunchAgent environment variables on macOS from 1Password-managed secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials can be persisted in a LaunchAgent plist and exposed through the process environment.

Mitigation: Use only when that storage model is acceptable, verify plist permissions, and rotate any credentials previously written by the script.

Risk: The 1Password service account token can grant access beyond the intended OpenClaw secrets.

Mitigation: Restrict the service account to the smallest possible vault scope before use.

Risk: The artifact claims to avoid plaintext secret storage while security evidence says credentials are persisted in the plist.

Mitigation: Review the script before installation and communicate the persistence behavior to operators.

## Reference(s):

- [Gateway Env Injector on ClawHub](https://clawhub.ai/nissan/skills/gateway-env-injector)
- [Publisher Profile](https://clawhub.ai/user/nissan)
- [1Password](https://1password.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell-script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS LaunchAgents, Bash, the 1Password CLI, and OP_SERVICE_ACCOUNT_TOKEN or a local service-token file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
