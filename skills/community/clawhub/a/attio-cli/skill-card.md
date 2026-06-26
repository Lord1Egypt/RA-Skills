## Description: <br>
Command-line tool to list, get, and manage objects, records, and lists in an Attio CRM workspace via the Attio API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FroeMic](https://clawhub.ai/user/FroeMic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CRM operators use this skill to install and run attio-cli commands for inspecting Attio objects, records, lists, and attributes, and for generating a Markdown workspace schema. It also provides examples for API operations that can search, create, and add CRM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Attio API credentials and CRM metadata. <br>
Mitigation: Use a least-privileged Attio API key, avoid committing or sharing credential files, and treat generated workspace schema files as sensitive business metadata. <br>
Risk: Create-record and add-entry examples can change the target CRM workspace. <br>
Mitigation: Run mutating commands only when the intended workspace, object, list, and payload have been reviewed. <br>
Risk: Installation depends on an external attio-cli repository that was not server-resolved as release provenance. <br>
Mitigation: Inspect or pin the external repository before installing and running the CLI. <br>


## Reference(s): <br>
- [Attio CRM CLI ClawHub page](https://clawhub.ai/FroeMic/attio-cli) <br>
- [Attio API base endpoint](https://api.attio.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline bash and curl examples; generated workspace schema is Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires attio-cli, jq, and an ATTIO_API_KEY; some examples can modify the connected CRM workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
