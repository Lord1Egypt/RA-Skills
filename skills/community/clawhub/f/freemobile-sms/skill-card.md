## Description: <br>
Envoyer des SMS a ton humain via Free Mobile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dClauzel](https://clawhub.ai/user/dClauzel) <br>

### License/Terms of Use: <br>
FPC (Fais pas chier) <br>


## Use Case: <br>
Agents and developers use this skill to send short SMS notifications to the configured Free Mobile subscriber number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Free Mobile SMS credentials could be exposed through logs, commits, or shared environments. <br>
Mitigation: Store FREEMOBILE_SMS_USER and FREEMOBILE_SMS_API_KEY as secrets, avoid printing them, and rotate the API key if exposure is suspected. <br>
Risk: An agent could send an unexpected or important SMS without adequate user intent. <br>
Mitigation: Require confirmation before sending sensitive, surprising, or high-impact messages. <br>
Risk: Free Mobile limits SMS length and send frequency, so long or repeated notifications may fail or be truncated. <br>
Mitigation: Keep messages under 160 characters and space repeated sends by at least 10 seconds. <br>


## Reference(s): <br>
- [Free Mobile SMS skill page](https://clawhub.ai/dClauzel/freemobile-sms) <br>
- [FreeMobile SMS homepage](https://github.com/dClauzel/freemobile-sms) <br>
- [Free Mobile notification SMS documentation](https://mobile.free.fr/account/mes-options/notifications-sms) <br>
- [REFERENCE.md](references/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text CLI status and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SMS message content is limited to 160 characters and requires Free Mobile credentials in environment variables.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
