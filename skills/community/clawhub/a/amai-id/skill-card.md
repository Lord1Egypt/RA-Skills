## Description:

Soul-Bound Keys and Soulchain for persistent agent identity, reputation, and messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonzih](https://clawhub.ai/user/gonzih)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent builders use this skill to integrate AMAI Identity Service registration, signed API requests, reputation anchoring, and public-key messaging into autonomous agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence requires review because the examples handle long-lived private signing keys unsafely if copied as written.

Mitigation: Avoid printing private keys, use encrypted or OS-managed secret storage, and enforce owner-only permissions for key material.

Risk: Permanent reputation and Soulchain records may retain sensitive personal, customer, or action details.

Mitigation: Keep sensitive details out of permanent reputation records and review payload contents before signing or submitting actions.

## Reference(s):

- [AMAI Identity Service](https://id.amai.net)
- [AMAI Website](https://amai.net)
- [ClawHub AMAI ID Listing](https://clawhub.ai/gonzih/skills/amai-id)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with API examples and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces identity-registration and request-signing guidance; no persistent files are created unless a user runs the example scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
