## Description: <br>
Registers an AI agent on Clawl by generating a clawl.json discovery file and submitting public agent metadata for indexing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlshlad85](https://clawhub.ai/user/wlshlad85) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make an AI agent discoverable through Clawl by publishing a clawl.json manifest and registering public-facing agent metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registration script may send public agent metadata to an unexpected default endpoint. <br>
Mitigation: Set CLAWL_API explicitly before running if registration should target a specific Clawl endpoint. <br>
Risk: The script can overwrite a local clawl.json file without the documented confirmation flow. <br>
Mitigation: Review or back up any existing clawl.json before running the registration script. <br>
Risk: Running the skill publishes agent name, description, capabilities, and optional contact or site fields. <br>
Mitigation: Provide only metadata intended for public discovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wlshlad85/clawl-the-agent-web) <br>
- [Clawl](https://clawl.co.uk) <br>
- [Clawl protocol](https://clawl.co.uk/protocol) <br>
- [clawl.json schema v0.1](https://clawl.co.uk/schema/v0.1.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus a generated JSON discovery manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes clawl.json in the workspace and may submit public agent metadata to a registration endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
