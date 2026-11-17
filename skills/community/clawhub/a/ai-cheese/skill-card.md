## Description:

Send paid messages to real humans via the A.I. Cheese platform for surveys, feedback, photo tasks, local knowledge, and verification, with USDC payments on Base through the x402 flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[locjonz](https://clawhub.ai/user/locjonz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search for human respondents, send paid messages, collect replies, and register webhooks for human-in-the-loop tasks such as surveys, feedback, photo requests, local knowledge, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a funded wallet private key to automatically send USDC payments based on remote payment requirements.

Mitigation: Use a dedicated low-balance wallet, avoid main wallet keys, and prefer versions with explicit per-message confirmation and maximum spend limits.

Risk: The security summary reports that the remote server and unpinned runtime code have too much practical authority over a funded wallet.

Mitigation: Review the server endpoint before use, keep the default endpoint only when trusted, and pin and review runtime dependencies before deployment.

## Reference(s):

- [A.I. Cheese Platform](https://aicheese.app)
- [Base Mainnet RPC Endpoint](https://mainnet.base.org)
- [ClawHub Skill Page](https://clawhub.ai/locjonz/skills/ai-cheese)
- [Publisher Profile](https://clawhub.ai/user/locjonz)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration]

**Output Format:** [CLI text output with command-line options and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and a funded wallet private key for paid message sending and balance checks.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
