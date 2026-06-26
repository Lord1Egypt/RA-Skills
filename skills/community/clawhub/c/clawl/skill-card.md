## Description: <br>
Register an AI agent on Clawl by generating a clawl.json discovery file and pinging a Clawl indexing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlshlad86](https://clawhub.ai/user/wlshlad86) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make an agent discoverable in Clawl by creating a public discovery manifest and registering or pinging the Clawl indexer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish locally detected agent metadata to a Clawl API endpoint. <br>
Mitigation: Install and run it only when publishing agent discovery metadata is intended; review the generated clawl.json before registration. <br>
Risk: The script uses CLAWL_API or its default destination for registration and ping requests. <br>
Mitigation: Set CLAWL_API explicitly when a specific destination is expected, and verify the endpoint before sending metadata. <br>
Risk: The script writes clawl.json in the current workspace and may overwrite an existing discovery file. <br>
Mitigation: Run it in a workspace where overwriting clawl.json is acceptable, or back up and review any existing file before execution. <br>


## Reference(s): <br>
- [Clawl protocol](https://clawl.co.uk/protocol) <br>
- [Clawl schema v0.1](https://clawl.co.uk/schema/v0.1.json) <br>
- [ClawHub skill page](https://clawhub.ai/wlshlad86/clawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and a JSON discovery manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates a local clawl.json file and may return Clawl registration or ping responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
