## Description:

Set up APoW Easy Mode on a supported assistant runtime, verify secure wallet recovery before funding, and use x402 remote GPU grinding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentoshi](https://clawhub.ai/user/agentoshi)

### License/Terms of Use:

MIT-0

## Use Case:

For users of supported assistant runtimes who want guidance for setting up APoW remote GPU mining. It covers runtime checks, independent wallet recovery, funding approval, and starting and monitoring the documented Easy Mode flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags an unpinned CLI reference, and setup invokes an external package through npx.

Mitigation: Review the dependency before running it and use the documented apow-cli@0.12.3 commands; do not substitute latest.

Risk: Easy Mode can use wallet funds and submit ongoing Base mining transactions until its runner is stopped.

Mitigation: Require explicit approval for the spending scope, verify an off-device restore of the same wallet, set an approved budget, and confirm a reliable stop method before starting.

## Reference(s):

- [APoW personal assistant profiles](https://apow.io/docs/technical/assistants)
- [APoW Cloud Mining status](https://apow.io/docs/technical/managed-mining)
- [APoW Mining release on ClawHub](https://clawhub.ai/agentoshi/skills/apow-mining)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-specific setup and safety guidance; no mining result is implied by setup instructions.]

## Skill Version(s):

0.12.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
