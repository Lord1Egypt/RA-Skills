## Description:

Use when checking for security vulnerabilities in NanoClaw skills, before installing new skills, or when asked about security advisories affecting the bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NanoClaw operators use this skill to check installed or candidate skills against ClawSec security advisories, verify skill package signatures, and monitor protected bot files for unauthorized changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive host-side integrity tools that can approve protected-file changes or restore critical bot files.

Mitigation: Require separate human or administrator approval before exposing integrity approval or auto-restore for global instructions or group registration files.

Risk: Production installs could trust a modified release package or unpinned installation path.

Mitigation: Use a pinned installer or the documented signed release verification path before installing or extracting the release.

Risk: Advisory scans may inspect an unintended skills directory if broad paths are supplied.

Mitigation: Restrict advisory scans to the intended NanoClaw skills directory and review scan scope during deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-nanoclaw)
- [ClawSec Advisory Feed](https://clawsec.prompt.security/advisories/feed.json)
- [Installation Guide](INSTALL.md)
- [File Integrity Monitoring for NanoClaw](docs/INTEGRITY.md)
- [Skill Package Signing and Verification](docs/SKILL_SIGNING.md)
- [ClawSec Security Architecture](https://clawsec.prompt.security/docs/architecture)
- [Ed25519 Specification (RFC 8032)](https://tools.ietf.org/html/rfc8032)
- [OpenSSL Ed25519 Documentation](https://www.openssl.org/docs/man3.0/man7/Ed25519.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-oriented tool results with inline TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing MCP tool output can include advisory matches, safety recommendations, signature verification results, integrity status, audit verification, and remediation guidance.]

## Skill Version(s):

0.0.10 (source: SKILL.md frontmatter, artifact/skill.json, CHANGELOG, ClawHub release evidence; released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
