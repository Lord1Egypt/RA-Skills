## Description:

Creates and manages secure, shareable links to an Aicoo agent, including sign-in requirements, scoped access, expiration, and link analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, update, revoke, and inspect share links that let selected recipients talk to an Aicoo agent with controlled scope, permissions, expiration, and sign-in behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of an Aicoo API token against notes search and note editing endpoints, which may affect sensitive notes or investor materials.

Mitigation: Review the skill before installation, use folder-scoped access where possible, and verify the exact note ID and intended content before allowing note patches.

Risk: Anonymous public links can expose agent content to recipients without sign-in.

Mitigation: Keep links sign-in-required by default, use short expirations, and set requireSignIn:false only when the user explicitly wants public anonymous access.

Risk: Write or edit notes access grants broader capabilities than read-only sharing.

Mitigation: Use least-privilege permissions, prefer read-only links for confidential content, and revoke or expire links when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xisen-w/skills/aicoo-share-agent)
- [Aicoo API Reference](reference/API.md)
- [Basic Share Example](examples/basic-share.md)
- [Aicoo API Base URL](https://www.aicoo.io/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated share URLs, link scope, notes and calendar permissions, expiration, sign-in status, and access sandboxing notes.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
