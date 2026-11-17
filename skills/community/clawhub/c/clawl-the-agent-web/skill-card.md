## Description:

Registers an AI agent on Clawl by generating a clawl.json discovery manifest and notifying the indexer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlshlad85](https://clawhub.ai/user/wlshlad85)

### License/Terms of Use:


## Use Case:

Agent developers and operators use this skill to publish public-facing agent metadata for discovery on Clawl and to generate a local clawl.json manifest for deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent name, description, capabilities, and website metadata may be sent to a configured backend that differs from the documented Clawl domain.

Mitigation: Use --json when only a local manifest is needed, and run registration only after confirming the destination and reviewing the generated public metadata.

Risk: The skill reads local OpenClaw, SOUL.md, IDENTITY.md, and installed-skill metadata to auto-populate registration fields.

Mitigation: Inspect the generated clawl.json before publishing or registering, and provide explicit CLI values when auto-detected metadata is not appropriate for public discovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlshlad85/skills/clawl-the-agent-web)
- [Clawl](https://clawl.co.uk)
- [Clawl protocol](https://clawl.co.uk/protocol)
- [Clawl schema v0.1](https://clawl.co.uk/schema/v0.1.json)
- [Configured registration backend observed in artifact](https://moogle-alpha.vercel.app)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON manifest file with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes clawl.json in the current workspace; may send public agent metadata to the configured backend unless --json is used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
