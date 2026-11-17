## Description:

Agent Sovereign Stack helps developers onboard an agent by uploading identity and memory files to FilStream, registering the agent on Base, optionally deploying a treasury, and setting up agent-to-agent messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quriustus](https://clawhub.ai/user/quriustus)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to provision decentralized identity, persistent memory, treasury controls, and messaging for OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identity, memory, and message content may be sent to the configured FilStream service without transport encryption or client-side encryption.

Mitigation: Use only data you are comfortable exposing, inspect files before upload, and add transport encryption or client-side encryption before handling sensitive material.

Risk: The onboarding flow uses wallet private keys for blockchain actions.

Mitigation: Use a dedicated low-balance wallet, avoid passing private keys on the command line, and keep signing credentials outside shared workspaces.

Risk: On-chain registration and treasury deployment can create persistent or irreversible state.

Mitigation: Start on Base Sepolia, confirm addresses and spending policies before execution, and require human review before mainnet transactions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus terminal summaries and JSON configuration files from scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution can upload local identity and memory files, write local agent state, and submit blockchain transactions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
