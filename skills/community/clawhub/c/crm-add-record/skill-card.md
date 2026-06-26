## Description: <br>
Automates adding new records to the Fractal CRM system by navigating the CRM, handling login, mapping natural language input to fields, and submitting the form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangli123456](https://clawhub.ai/user/zhangli123456) <br>

### License/Terms of Use: <br>


## Use Case: <br>
CRM users and automation agents use this skill to convert free-form customer or sales lead details into Fractal CRM record fields and add a new CRM entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes shared CRM login credentials. <br>
Mitigation: Remove and rotate the exposed credentials before use, and require user-owned or managed secrets for authentication. <br>
Risk: The skill can create CRM records without a clear final approval step. <br>
Mitigation: Require confirmation of the exact fields and destination record before saving or submitting any CRM entry. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangli123456/crm-add-record) <br>
- [Fractal CRM Modify Page](https://niw26kl7.fractaltest.cn/Crm/Backend/modify.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, plus JSON from parser scripts and text CRM record summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate browser automation against a CRM page and may print standardized CRM fields for manual entry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
