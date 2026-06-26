## Description: <br>
管理电科院人员信息和科室关系的技能。支持添加、查询、更新电科院工作人员、科室、办公室等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HumbleBin](https://clawhub.ai/user/HumbleBin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or external users who need a lightweight local directory can record and look up Diankeyuan staff, departments, roles, and office locations during contact-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores identifiable staff records in a local JSON file. <br>
Mitigation: Use it only for personnel data approved for local storage, restrict filesystem access where possible, and document where the data is stored. <br>
Risk: Delete operations can remove contact records. <br>
Mitigation: Make backups before delete workflows and prefer a version that requires confirmation before removing records. <br>
Risk: The security review found insufficient disclosed controls for personnel data. <br>
Mitigation: Review before installing and prefer an updated version that declares file permissions and data-handling behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HumbleBin/diankeyuan-contacts) <br>
- [HumbleBin publisher profile](https://clawhub.ai/user/HumbleBin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local JSON data operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, query, and delete locally stored personnel records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
