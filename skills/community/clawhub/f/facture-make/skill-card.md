## Description: <br>
Generates and prepares a professional invoice, prompts for human confirmation, then sends the confirmed invoice to Make.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cimes19](https://clawhub.ai/user/cimes19) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers, consultants, and business users can use this skill to prepare invoice details, review a confirmation prompt, and send the approved invoice payload to a Make.com automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends business invoice data to a fixed Make.com webhook. <br>
Mitigation: Use it only when the webhook destination is trusted or controlled, and confirm the destination and retention policy before sending invoice data. <br>
Risk: Weak payload scoping could send fields beyond the intended invoice details. <br>
Mitigation: Pass only the confirmed invoice object to the sending script and review the exact fields before execution. <br>
Risk: Client, billing, or private business data may be exposed to an external automation service. <br>
Mitigation: Avoid including unrelated private data and minimize invoice payloads to the fields required by the Make.com workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cimes19/facture-make) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [prepare_invoice.py](artifact/prepare_invoice.py) <br>
- [send_invoice.py](artifact/send_invoice.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and script execution instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human confirmation before sending invoice data to Make.com.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
