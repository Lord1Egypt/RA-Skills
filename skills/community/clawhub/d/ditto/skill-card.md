## Description:

Save, search, fetch, and traverse the user's Ditto memory graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ditto](https://clawhub.ai/user/ditto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Ditto to let agents save, retrieve, update, publish, and traverse long-term personal memories and topic relationships across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can save durable personal memories to a third-party cloud service.

Mitigation: Use remote memory only when intended, avoid saving sensitive data unless the user approves the exact content, and keep saved memories limited to durable facts that should persist.

Risk: The setup flow can create a claimable account and store an API key in local CLI configuration.

Mitigation: Share only the claim URL, never the API key, and use heyditto logout or remove the saved config key when agent access is no longer wanted.

Risk: Installing the CLI from an unpinned package can change behavior as the package evolves.

Mitigation: Prefer a pinned or reviewed @heyditto/cli version where possible and confirm command behavior with heyditto status or heyditto help before use.

## Reference(s):

- [Ditto homepage](https://heyditto.ai)
- [@heyditto/cli on npm](https://www.npmjs.com/package/@heyditto/cli)
- [Ditto ClawHub skill page](https://clawhub.ai/ditto/skills/ditto)
- [Ditto publisher profile](https://clawhub.ai/user/ditto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs from the Ditto CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the heyditto CLI and DITTO_API_KEY or local CLI config for authentication.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
