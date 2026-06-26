## Description: <br>
Tracks FUTA Express (Phương Trang) package delivery status through the public FUTA Express lookup API using a provided tracking code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongtanhieu](https://clawhub.ai/user/tongtanhieu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up FUTA Express shipment status, package details, fees, and delivery history from a tracking code. Results are presented in Vietnamese while preserving the returned field values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A tracking lookup can display personal shipment details, including sender, recipient, phone, and identity fields. <br>
Mitigation: Use the skill only for shipments the user is authorized to check, and mask or omit phone and identity fields unless they are required for the task. <br>
Risk: The agent queries FUTA Express with a user-provided tracking code and may surface sensitive delivery history. <br>
Mitigation: Confirm the tracking code before lookup and avoid sharing returned shipment details beyond the authorized user. <br>


## Reference(s): <br>
- [FUTA Express public package lookup API](https://api.futaexpress.vn/bo-operation/f1/full-bill-by-code-public/<tracking_code>) <br>
- [ClawHub release page](https://clawhub.ai/tongtanhieu/futa-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown tracking report with Vietnamese shipment fields, package details, fees, and status history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a tracking code and may include personal sender, recipient, phone, identity, fee, and shipment-history details returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
