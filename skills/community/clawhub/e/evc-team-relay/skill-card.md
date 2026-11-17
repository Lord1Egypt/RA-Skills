## Description:

Read and write Obsidian notes stored in an EVC Team Relay collaborative vault through REST API helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[venturecrew](https://clawhub.ai/user/venturecrew)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent list, read, create, update, and delete Markdown notes in a shared EVC Team Relay Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and delete shared Obsidian notes through authenticated Relay API calls.

Mitigation: Use a dedicated least-privilege Relay account and require human approval before write or delete operations.

Risk: Relay credentials and bearer tokens grant access to shared vault content.

Mitigation: Store credentials in trusted environment configuration, prefer RELAY_TOKEN over token arguments, avoid exposing tokens in command history or process listings, and rotate credentials when access changes.

Risk: Accidental or incorrect writes can alter team knowledge bases.

Mitigation: Keep backups or versioning for shared vaults and review agent-proposed note changes before applying them.

Risk: Using an untrusted or non-HTTPS control-plane URL can expose credentials or vault content.

Mitigation: Use HTTPS-only RELAY_CP_URL values that point to a trusted Relay deployment.

## Reference(s):

- [EVC Team Relay repository](https://github.com/entire-vc/evc-team-relay)
- [EVC Team Relay API Reference](references/api.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [EVC Local Sync Plugin](https://github.com/entire-vc/evc-local-sync-plugin)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Relay environment variables and curl/jq; read and write operations return Relay API content or JSON responses.]

## Skill Version(s):

1.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
