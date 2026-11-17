## Description:

Registers an AI agent with Clawl by generating a clawl.json discovery manifest and optionally submitting public agent metadata for indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlshlad86](https://clawhub.ai/user/wlshlad86)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to publish an agent discovery manifest and register public agent profile details with Clawl so the agent can be found and ranked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the registration path can transmit agent profile metadata to the script's configured API endpoint.

Mitigation: Use --json when only a local manifest is needed, and run network registration only after confirming the destination service is acceptable.

Risk: The script may overwrite an existing clawl.json manifest in the workspace.

Mitigation: Back up any existing clawl.json before running the skill and review the generated manifest before publishing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlshlad86/skills/clawl)
- [Clawl](https://clawl.co.uk)
- [Clawl protocol](https://clawl.co.uk/protocol)
- [Clawl schema v0.1](https://clawl.co.uk/schema/v0.1.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a JSON discovery manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write clawl.json in the current workspace and may submit public agent profile metadata unless run with --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
