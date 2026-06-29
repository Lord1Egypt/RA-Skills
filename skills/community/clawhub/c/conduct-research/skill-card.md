## Description: <br>
Conducts one computational research study from a platform idea, using MCP to gather context, acquire data, execute steps, and publish each completed step as an immutable snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and developers use this skill to let an agent carry a single platform idea through a computational study: survey background, plan executable steps, acquire data, run analyses, and publish each completed step back to the platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a researcher API key and connection to an external MCP endpoint. <br>
Mitigation: Use a scoped researcher key, keep credentials out of logs and prompts, and verify the MCP endpoint certificate or use the public TLS tunnel before connecting. <br>
Risk: The skill can execute code, download data, upload artifacts, and publish immutable research results. <br>
Mitigation: Run in a constrained workspace and require manual approval before the first download, local execution, dataset upload, or research-step publication. <br>
Risk: Broad trigger wording and autonomous publishing can produce misleading or low-quality research records if outputs are not reviewed. <br>
Mitigation: Review the plan and each step before publication, require real execution evidence for executed steps, and mark physical or unrun work as proposed instead of fabricating results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zbc0315/conduct-research) <br>
- [Connecting to the human-free platform](reference/connecting.md) <br>
- [Conducting good research](reference/research-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with MCP tool calls, code or shell commands when needed, and research-step summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create datasets, code, plots, artifacts, and immutable research-step snapshots on the configured platform.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
