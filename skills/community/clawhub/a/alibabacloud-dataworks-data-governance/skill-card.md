## Description: <br>
Manages Alibaba Cloud DataWorks data asset tags by creating, updating, listing, binding, unbinding, and querying tag keys, tag values, and data assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud data-governance operators use this skill to manage DataWorks data asset tag metadata with confirmed parameters, credential checks, and RAM permission guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, bind, and unbind operations against live Alibaba Cloud DataWorks assets. <br>
Mitigation: Require manual confirmation of region, project, asset identifiers, tag keys, tag values, and operation intent before execution. <br>
Risk: The skill requires sensitive Alibaba Cloud credential access through an existing CLI or SDK profile. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, check credential status without exposing secrets, and never paste access keys into chat or commands. <br>
Risk: Security evidence marks the release suspicious because setup guidance and triggers are broader than the narrow cloud metadata task. <br>
Mitigation: Install only for Alibaba Cloud DataWorks tag management and review proposed setup, plugin, and API actions before use. <br>
Risk: Deletion of tag keys or tag values is outside the supported behavior. <br>
Mitigation: Do not call or suggest DeleteDataAssetTag; route deletion requests through separately authorized channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-dataworks-data-governance) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related API Commands](references/related-commands.md) <br>
- [Success Verification](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Alibaba Cloud DataWorks API call patterns and verification steps after user confirmation.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
