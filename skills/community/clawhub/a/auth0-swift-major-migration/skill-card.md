## Description: <br>
Use when upgrading an iOS or macOS app's Auth0.swift SDK from v2 to v3 by detecting the current version, checking v3 SDK signatures, and applying only breaking changes that affect real call sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers maintaining iOS or macOS apps with existing Auth0.swift v2 integrations use this skill to migrate dependencies and affected call sites to Auth0.swift v3 while preserving project-specific authentication behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit dependency manifests and Swift source while migrating Auth0.swift v2 projects to v3. <br>
Mitigation: Use it only in projects intended for this migration, start from a clean git working tree, and review the final diff before committing. <br>
Risk: Build, grep, or terminal output can contain project-specific secrets if pasted into prompts or summaries. <br>
Mitigation: Avoid sharing terminal output that includes tokens, client secrets, credentials, or Keychain values; follow the security checklist if scanner commands flag sensitive data. <br>
Risk: Removed client-side Management API functionality can require backend work, and mishandling it could expose privileged tokens. <br>
Mitigation: Preserve affected call-site intent with reviewable TODOs and move Management API operations to a secure backend rather than embedding management tokens in the client app. <br>


## Reference(s): <br>
- [Migration Process - Edge Cases and Procedures](references/process.md) <br>
- [Security Checklist - Auth0.swift Migration](references/security.md) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0.swift GitHub](https://github.com/auth0/Auth0.swift) <br>
- [Auth0.swift Releases](https://github.com/auth0/Auth0.swift/releases) <br>
- [Auth0.swift API Documentation](https://auth0.github.io/Auth0.swift/documentation/auth0/) <br>
- [Auth0 Management API Access Tokens](https://auth0.com/docs/secure/tokens/access-tokens/management-api-access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Swift code blocks; agent runs may also produce project file edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces a migration summary, dependency update guidance, build and test commands, and focused Swift or dependency manifest changes after project usage is confirmed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
