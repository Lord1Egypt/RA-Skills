## Description: <br>
Creates bar, line, pie, scatter, doughnut, radar, and related chart images from structured data through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate professional chart images for reports, dashboards, presentations, publications, and embedded content from structured chart data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart inputs are sent to AgentPMT and QuickChart remote services. <br>
Mitigation: Avoid confidential, regulated, customer, or unpublished research data unless the user explicitly accepts remote processing. <br>
Risk: Chart files are stored by default and returned as temporary signed URLs. <br>
Mitigation: For sensitive outputs, set return_base64 to true and store_file to false, or avoid using the skill for that data. <br>
Risk: The skill may be selected for generic data tasks where remote chart generation was not requested. <br>
Mitigation: Confirm the user wants remote chart generation before sending chart data to the tool. <br>


## Reference(s): <br>
- [Chart Generator schema](schema.md) <br>
- [AgentPMT Chart Generator marketplace page](https://www.agentpmt.com/marketplace/chart-generator) <br>
- [ClawHub Chart Generator release page](https://clawhub.ai/agentpmt/skills/chart-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API Calls, Files] <br>
**Output Format:** [JSON responses containing chart metadata, signed URLs, or base64 image data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return PNG, SVG, PDF, or WebP charts; stored files use signed URLs with configurable 1-7 day expiration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
