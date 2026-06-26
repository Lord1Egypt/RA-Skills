## Description: <br>
Zoho Bigin CRM CLI for searching deals, contacts, and accounts, adding notes, moving deal stages, and updating Bigin records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ingodibella](https://clawhub.ai/user/Ingodibella) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operators managing Zoho Bigin CRM use this skill to retrieve pipeline, contact, and account details and, with explicit approval, perform CRM updates such as notes, stage moves, record edits, or raw API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change live CRM data, including notes, deal stages, records, deletes, and raw API calls. <br>
Mitigation: Keep BIGIN_WRITE unset unless approving one specific CRM change, require BIGIN_CONFIRM for deletes, and review record IDs, endpoints, and payloads before execution. <br>
Risk: The artifact references a missing bigin.sh helper, so command behavior depends on a helper not present in the reviewed files. <br>
Mitigation: Install only after verifying the helper source and contents, and confirm it matches the documented read/write/delete guardrails. <br>
Risk: OAuth credentials may grant access to the intended Bigin account and scopes. <br>
Mitigation: Use the least-privileged OAuth file for the intended Bigin account and avoid raw API calls unless the endpoint and payload have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ingodibella/bigin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CRM record or API responses when commands are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands work by default; write and delete operations require explicit environment gates and user approval.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
