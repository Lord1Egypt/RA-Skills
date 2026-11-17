## Description:

Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regan-milne](https://clawhub.ai/user/regan-milne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to save, load, list, and migrate encrypted agent memory across sessions and machines using Jackal-backed storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may retain sensitive personal or operational data across sessions.

Mitigation: Store only information intended for retention, avoid raw secrets unless explicitly required and accepted, and review saved memory before relying on it.

Risk: Wallet credentials, API keys, and encryption keys are required for normal operation.

Mitigation: Use a dedicated Jackal wallet and API key, keep credentials in the local environment, and back up the wallet mnemonic and encryption key securely.

Risk: Local environment variables or a parent .env file could expose unrelated secrets to the Node dependency chain.

Mitigation: Run from a clean environment without unrelated cloud or repository tokens, avoid secret-bearing parent .env files, and audit dependencies before installation.

Risk: The security evidence reports a vulnerable or deprecated Node dependency tree.

Mitigation: Upgrade and audit the Node dependencies before trusting the skill with valuable wallet-backed storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regan-milne/skills/claw-store-1-3-3)
- [Obsideo homepage](https://obsideo.io)
- [Source repository](https://github.com/Regan-Milne/jackal-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory save/load guidance and command examples for a local Python and Node.js helper workflow.]

## Skill Version(s):

1.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
