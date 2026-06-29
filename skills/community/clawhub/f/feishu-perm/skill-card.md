## Description: <br>
Feishu permission management for documents and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumuzhi4843-a](https://clawhub.ai/user/sumuzhi4843-a) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help list, add, and remove collaborators on Feishu documents, files, folders, spreadsheets, wikis, and related drive assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change access to Feishu documents, files, folders, spreadsheets, wikis, and related drive assets. <br>
Mitigation: Enable the skill only when document-permission management is intended, and verify the target token, recipient identity, member type, and permission level before add, remove, or full_access operations. <br>
Risk: The full_access permission level delegates the ability to manage permissions. <br>
Mitigation: Treat full_access as administrative delegation and reserve it for recipients who are authorized to manage access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumuzhi4843-a/feishu-perm) <br>
- [Publisher profile](https://clawhub.ai/user/sumuzhi4843-a) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API Calls] <br>
**Output Format:** [Markdown with JSON and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit Feishu tool configuration and the drive:permission scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
