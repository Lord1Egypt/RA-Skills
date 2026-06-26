## Description: <br>
Apaleo hotel property management API integration with managed OAuth. Manage properties, units, unit groups, and unit attributes. Use this skill when users want to list hotel properties, create rooms and units, check availability, or manage property inventory in Apaleo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hotel operators, and property-management teams use this skill to connect an agent to Apaleo through ClawLink OAuth, discover property inventory, and manage properties, units, unit groups, and unit attributes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide write or delete operations against Apaleo property inventory. <br>
Mitigation: Confirm write and delete actions before execution, and review requested Apaleo scopes such as properties.manage, units.create, or setup.manage. <br>
Risk: The skill requires OAuth-backed access to an Apaleo account through ClawLink. <br>
Mitigation: Connect only the intended Apaleo account, verify the active connection before use, and reconnect through the documented dashboard flow when access changes. <br>
Risk: Some destructive Apaleo actions, including unit deletion or test-property data reset, may be irreversible. <br>
Mitigation: Use read/list tools to verify target property, unit, and unit-group identifiers before running destructive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/apaleo) <br>
- [Apaleo API Docs](https://apaleo.com/api/) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink dashboard connection](https://claw-link.dev/dashboard?add=apaleo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions require an active ClawLink Apaleo connection; write and delete operations should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
