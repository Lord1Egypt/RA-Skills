## Description:

Helps developers migrate existing iOS or macOS apps from Auth0.swift v2 to v3 by detecting the installed version, checking the target SDK source, and applying only breaking changes that affect real call sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to upgrade existing Auth0.swift v2 integrations to v3 while preserving authentication, credential storage, logout, MFA, and build behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled evaluation runner can copy broad project contents, including sensitive files, and send source snippets to an external Claude CLI.

Mitigation: Run evals only on sanitized projects; remove secrets and exclude .env and credential-bearing configuration files before evaluation.

Risk: Migration changes can affect authentication, credential storage, logout, MFA, and Management API flows.

Mitigation: Start from a clean git worktree, review generated diffs, preserve Keychain and PKCE behavior, and rerun build, tests, and security checks before committing.

Risk: Applying SDK changes from assumptions instead of the target release can break authentication behavior.

Mitigation: Fetch and read the target Auth0.swift v3 source, then apply only changes for APIs found in the project source audit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-swift-major-migration)
- [Publisher Profile](https://clawhub.ai/user/auth0)
- [OpenClaw Homepage](https://github.com/auth0/agent-skills)
- [Auth0.swift GitHub](https://github.com/auth0/Auth0.swift)
- [Auth0.swift Releases](https://github.com/auth0/Auth0.swift/releases)
- [Auth0.swift API Documentation](https://auth0.github.io/Auth0.swift/documentation/auth0/)
- [Migration Process](references/process.md)
- [Security Checklist](references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Swift, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose source edits and commands; migration changes are gated by project source audit.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
