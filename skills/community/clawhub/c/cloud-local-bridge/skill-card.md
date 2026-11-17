## Description:

Enables bidirectional communication between cloud and local OpenClaw instances, including natural-language pairing, command execution, and file synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[84191879](https://clawhub.ai/user/84191879)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to pair cloud and local OpenClaw environments, route cloud-originated requests to a local bridge service, execute local commands, and move files between environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge gives a paired remote party broad local command-execution and file-access capability.

Mitigation: Install only when that level of remote control is intended; run with least privilege, avoid running as root, and restrict access to non-sensitive working directories.

Risk: A publicly exposed bridge port or long-lived token can allow unauthorized local machine access if the token is leaked or guessed.

Mitigation: Use a private network or secure tunnel, do not expose the port publicly, use strong tokens, and rotate tokens after pairing or suspected exposure.

Risk: The file features can read or transfer sensitive OpenClaw memory, configuration, SSH keys, or other private files.

Mitigation: Do not grant the bridge access to sensitive local paths, and review requested file paths before allowing read, download, upload, or sync operations.

## Reference(s):

- [Cloud-Local Bridge usage examples](references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash, JSON, Python, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bearer-token bridge configuration, command examples, and file path arguments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
