## Description: <br>
Manages Bohrium dev nodes through the bohr CLI or Bohrium node APIs for lifecycle operations, resource checks, pricing, and access guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, inspect, connect to, stop, delete, and troubleshoot Bohrium cloud dev nodes used for data preparation, compilation, debugging, and post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bohrium access key and may expose node SSH credentials. <br>
Mitigation: Store the access key in the agent's secret configuration, prefer passwordless bohr CLI connections, and avoid printing or sharing node passwords. <br>
Risk: The skill can create, stop, delete, and modify billable cloud nodes and bind datasets. <br>
Mitigation: Require explicit user approval before billable creation, deletion, dataset binding, or any operation that changes node state. <br>
Risk: The bohr CLI installation path runs a remote installer script. <br>
Mitigation: Verify the installer source and contents before running it in a trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-node) <br>
- [Bohrium node OpenAPI endpoint](https://open.bohrium.com/openapi/v1/node) <br>
- [Bohrium dp.tech node API endpoint](https://openapi.dp.tech/openapi/v1/node) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands, API request examples, environment variable setup, resource and pricing guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
