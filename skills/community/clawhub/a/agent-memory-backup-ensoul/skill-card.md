## Description:

Agent Memory Backup (Ensoul) helps agents create a persistent identity, back up memory and state, and restore that state through the Ensoul Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suitandclaw](https://clawhub.ai/user/suitandclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register an agent identity, back up selected agent memory or state, check backup status, and inspect other registered agents on the Ensoul Network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a persistent private seed in ~/.ensoul/agent-identity.json.

Mitigation: Protect the identity file with restrictive permissions, do not display or log the seed, and rotate or remove the identity if the file may have been exposed.

Risk: Backup actions may process broad agent memory or private conversation context.

Mitigation: Use explicit user confirmation and a narrow allowlist for files such as SOUL.md and MEMORY.md, and exclude secrets or sensitive private conversations.

Risk: The skill performs external network and blockchain actions that may be persistent.

Mitigation: Confirm registration and sync actions before execution, explain that transactions may be final, and retry failed network requests no more than once.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suitandclaw/skills/agent-memory-backup-ensoul)
- [Ensoul website](https://ensoul.dev)
- [Ensoul explorer](https://explorer.ensoul.dev)
- [@ensoul-network/sdk on npm](https://www.npmjs.com/package/@ensoul-network/sdk)
- [Ensoul network status](https://status.ensoul.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read ~/.ensoul/agent-identity.json and selected local agent state files when the user invokes backup or status commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
