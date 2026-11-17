## Description:

Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regan-milne](https://clawhub.ai/user/regan-milne)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to save, load, list, and migrate persistent encrypted agent memory across sessions and machines using Jackal decentralized storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys, encryption keys, wallet mnemonics, and memory content that may be sensitive.

Mitigation: Set required secrets directly in the local environment, avoid pasting them into chat or logs, and run the skill in a clean environment with only the required Jackal variables.

Risk: Persistent memory depends on local wallet and encryption material; losing these values can prevent recovery of stored memories.

Mitigation: Back up and protect the wallet mnemonic, encryption key, and local key manifest before relying on the skill for important memory.

Risk: The skill uses a Railway-hosted API, external Jackal providers, and Node dependencies.

Mitigation: Verify endpoint trust in the deployment environment and review or update the npm dependency tree before using the skill with sensitive memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regan-milne/skills/claw-store)
- [Obsideo homepage](https://obsideo.io)
- [Repository listed in OpenClaw metadata](https://github.com/Regan-Milne/jackal-memory)
- [Runtime API host](https://web-production-5cce7.up.railway.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and text or JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local encrypted-memory configuration, wallet, and manifest files under the user's home configuration directory.]

## Skill Version(s):

1.3.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
