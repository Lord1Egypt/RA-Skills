## Description: <br>
Work with Microsoft Dynamics 365 CRM records, accounts, contacts, leads, opportunities, and activities - powered by ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations users can ask an agent to find, create, and update Dynamics 365 CRM records such as accounts, contacts, leads, opportunities, cases, invoices, and sales orders through ClawLink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Dynamics 365 CRM records, which may affect customer, sales, invoice, case, or opportunity data. <br>
Mitigation: Review proposed tool calls and parameters before approving write actions, and rely on Dynamics 365 roles and field-level permissions to limit access. <br>
Risk: The workflow depends on ClawLink OAuth and credential handling for a connected Dynamics 365 account. <br>
Mitigation: Connect only a trusted ClawLink account, review requested permissions during OAuth, and revoke or reconnect access if credentials or permissions change. <br>


## Reference(s): <br>
- [ClawHub Dynamics 365 skill page](https://clawhub.ai/hith3sh/dynamics-365-crm) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dynamics-365-crm) <br>
- [ClawLink Dynamics 365 connection dashboard](https://claw-link.dev/dashboard?add=dynamics-365) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawLink pairing and a connected Microsoft Dynamics 365 account before CRM tools are available.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
