## Description: <br>
ExchangeService provides Node.js-powered EWS operations for on-premises Exchange Server 2016 CU21 mail, folders, calendars, and meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JokerMeC](https://clawhub.ai/user/JokerMeC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to let an agent inspect and manage an on-premises Exchange mailbox, folder tree, and calendar through EWS while requiring explicit confirmation for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive mailbox and calendar data for the configured Exchange account. <br>
Mitigation: Install only for intended mailbox access, use a least-privilege mailbox account, and narrow read scopes and time windows when possible. <br>
Risk: Credentials, master keys, or command output could expose mailbox access if captured in logs or shared terminals. <br>
Mitigation: Keep the master key, Exchange password, generated config, and command output out of logs and shared artifacts. <br>
Risk: Using the insecure TLS option can weaken server certificate validation for a request. <br>
Mitigation: Avoid the insecure option unless the TLS risk is understood and accepted for the specific Exchange endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JokerMeC/exchangeserviceskill) <br>
- [Microsoft Exchange EWS operations reference](https://learn.microsoft.com/en-us/exchange/client-developer/web-service-reference/ews-operations-in-exchange) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with npm command examples and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js/npm plus configured Exchange URL, username, authentication mode, password, and master key environment values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
