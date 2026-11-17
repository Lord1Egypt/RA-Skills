## Description:

Enables AI agents to communicate securely with each other through encrypted messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to propose encrypted agent-to-agent messaging workflows for coordination, data sharing, broadcasts, and persistent message queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample implementation handles keys, files, and identities too loosely for a security-sensitive communication system.

Mitigation: Use only in controlled experiments or after hardening key storage, path restrictions, identifier validation, and recipient confirmation.

Risk: Messages and attachments may carry data outside the current session.

Mitigation: Avoid sensitive files and require explicit recipient confirmation before sending messages or attachments.

Risk: The advertised impersonation resistance and forward secrecy are not reliable until the implementation changes.

Mitigation: Do not rely on those claims for production security decisions without independent redesign and review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cerbug45/skills/cerbug45-agent-crypto-message)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples and JSON data structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides implementation guidance and sample cryptographic messaging code rather than a deployed communication service.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
