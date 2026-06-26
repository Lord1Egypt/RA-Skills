## Description: <br>
Manage Feishu document, file, folder, and wiki permissions by setting access levels, sharing with users or groups, or revoking access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erick0309](https://clawhub.ai/user/erick0309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to have an agent help manage Feishu permissions for documents, drive files and folders, and wiki pages. It supports setting access levels, sharing resources with specific users or groups, changing permission levels, and revoking access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An incorrect permission update could expose a Feishu resource or remove needed access. <br>
Mitigation: Before applying any permission change, require the agent to restate the target document, file, folder, or wiki page, the affected user or group, and the exact permission level or revocation. <br>
Risk: Permission changes may fail or be inappropriate if the requesting user lacks authority over the Feishu resource. <br>
Mitigation: Require the user to authenticate with a Feishu account that has appropriate owner or editor permissions before attempting changes. <br>


## Reference(s): <br>
- [Feishu Perm ClawHub release](https://clawhub.ai/erick0309/feishu-perm-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown or plain text instructions for Feishu permission changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Before applying changes, the agent should restate the target resource, affected user or group, and exact permission level or revocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
