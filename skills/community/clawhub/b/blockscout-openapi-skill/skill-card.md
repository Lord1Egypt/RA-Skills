## Description: <br>
Operate Blockscout explorer reads through UXC with a curated OpenAPI schema, instance-specific host selection, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Blockscout explorer REST APIs for address, token, transaction, and block reads through a curated OpenAPI schema and UXC command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI alias can be linked or relinked to an unintended Blockscout host. <br>
Mitigation: Confirm the target host before linking, and inspect host and operation help before larger reads. <br>
Risk: Protected Blockscout deployments may expose data only to intended credential holders. <br>
Mitigation: Bind credentials only for the intended host and only when read access is expected. <br>
Risk: Pagination, filters, and response fields can vary across Blockscout deployments. <br>
Mitigation: Start with narrow lookups and parse stable JSON envelope fields before automating larger history reads. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/blockscout-v2.openapi.json) <br>
- [Blockscout API documentation](https://docs.blockscout.com/devs/apis-redirect) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented API output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Blockscout REST operations through UXC; responses should remain in the JSON output envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
