## Description: <br>
Register this AI agent on Clawl, generate a clawl.json discovery file, and ping Clawl for indexing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlshlad85](https://clawhub.ai/user/wlshlad85) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent maintainers use this skill to publish an agent discovery manifest and register public-facing agent metadata with Clawl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send public agent metadata to a default service that differs from the documented Clawl URLs. <br>
Mitigation: Set CLAWL_API explicitly to the intended Clawl-controlled host or run the script with --json to generate clawl.json without network registration. <br>
Risk: The script writes clawl.json in the current workspace and may overwrite an existing file. <br>
Mitigation: Run it only in the intended directory, inspect any existing clawl.json first, and review the generated manifest before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wlshlad85/clawl-register) <br>
- [Clawl](https://clawl.co.uk) <br>
- [Clawl Protocol](https://clawl.co.uk/protocol) <br>
- [Clawl schema v0.1](https://clawl.co.uk/schema/v0.1.json) <br>
- [Clawl registration](https://clawl.co.uk/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [Markdown guidance with command examples and generated clawl.json configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes clawl.json in the current workspace and may send public agent metadata to the configured Clawl API unless run in JSON-only mode.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
