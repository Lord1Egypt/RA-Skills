## Description:

NanoClaw runtime traffic monitoring baseline for host-side proxy inspection with container-safe MCP and IPC status surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a NanoClaw specification baseline for opt-in host-side traffic monitoring, redacted findings, and container-safe MCP status surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified or floating release could expose users to tampered skill metadata or archives.

Mitigation: Prefer the signed release verification workflow or use a pinned, trusted version of the Skills CLI before installation.

Risk: Future traffic proxying or optional HTTPS inspection could expose sensitive request data.

Mitigation: Keep monitoring opt-in, redact snippets before logs or MCP responses, and keep CA private key material on the host side.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-nanoclaw-traffic-guardian)
- [ClawSec Homepage](https://clawsec.prompt.security)
- [NanoClaw Traffic Guardian Specification](artifact/SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and safe operating constraints; this release is a specification scaffold with no active runtime proxy code.]

## Skill Version(s):

0.0.2 (source: server release metadata, SKILL.md frontmatter, skill.json, CHANGELOG released 2026-09-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
