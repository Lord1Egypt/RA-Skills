## Description:

Persistent agent memory and versioned markdown documents over the Mark Protocol (mark://).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontehfritz](https://clawhub.ai/user/ontehfritz)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers and agent users use this skill to configure persistent memory, fetch and publish mark:// markdown documents, keep journals, and preserve useful context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow runs a remote installer that is not pinned or checksum-verified.

Mitigation: Review the installer before running it, or use a pinned, checksum-verified installer.

Risk: A local memory server may be exposed on the network.

Mitigation: Bind the server to localhost and avoid opening firewall access unless network exposure is explicitly required.

Risk: Persistent journals or remote servers can store sensitive context.

Mitigation: Use remote mode only with trusted servers and avoid storing secrets or private user data in journals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ontehfritz/skills/demarkus)
- [Demarkus homepage](https://demarkus.io)
- [Demarkus installer](https://raw.githubusercontent.com/latebit-io/demarkus/main/install.sh)
- [mcporter call syntax](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md)
- [mcporter CLI reference](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and Mark Protocol document operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent-memory setup guidance and document operation instructions for local or user-provided remote Mark servers.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
