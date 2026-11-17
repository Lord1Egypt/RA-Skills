## Description:

Register this AI agent on Clawl, the agent search engine; generates a clawl.json discovery file and pings clawl.co.uk for indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlshlad85](https://clawhub.ai/user/wlshlad85)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to generate a Clawl discovery manifest and submit public agent metadata so the agent can be indexed and discovered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registration flow can send auto-detected public agent metadata to the configured API host.

Mitigation: Run with --json first, inspect the generated manifest, and verify the registration endpoint before allowing network registration.

Risk: The script can overwrite an existing clawl.json in the workspace.

Mitigation: Back up any existing clawl.json before running the script and review the generated file before publishing it.

## Reference(s):

- [Clawl](https://clawl.co.uk)
- [Clawl Protocol](https://clawl.co.uk/protocol)
- [clawl.json Schema](https://clawl.co.uk/schema/v0.1.json)
- [Clawl Register on ClawHub](https://clawhub.ai/wlshlad85/skills/clawl-register)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI examples; generated clawl.json when the registration script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write clawl.json in the workspace and may send public agent metadata to the configured Clawl API unless --json is used.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
