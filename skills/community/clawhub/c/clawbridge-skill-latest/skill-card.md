## Description:

Runs Clawbridge discovery from OpenClaw chat and returns a candidate count with a Vault review link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leethebuilder](https://clawhub.ai/user/leethebuilder)

### License/Terms of Use:

MIT

## Use Case:

External users and developers who already use Clawbridge can trigger a connection-discovery run from OpenClaw chat and review candidates in the Clawbridge Vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path uses a remote shell installer whose exact contents are not pinned in the release evidence.

Mitigation: Install only after trusting the publisher, and prefer a signed, versioned installer with published checksums.

Risk: The skill depends on a private runner that uploads discovery results to a Vault.

Mitigation: Confirm what the runner reads, uploads, stores, and how to uninstall it before using the skill with sensitive workspace data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/leethebuilder/skills/clawbridge-skill-latest)
- [Clawbridge homepage](https://clawbridge.cloud)
- [Clawbridge install script](https://clawbridge.cloud/install)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown text with inline command examples and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parses runner output fields such as VAULT_URL, CANDIDATES_COUNT, and optional DISCOVERY_SOURCE.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
