## Description: <br>
Google Docs Log Automation - Append log lines to auto-created daily documents in Google Drive by PortEden Secure Access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to append structured run logs to daily Google Docs in a configured Google Drive folder. It helps preserve simple append-only activity records while using PortEden Secure Access for authentication and Drive access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive log contents may be stored in Google Docs. <br>
Mitigation: Avoid logging secrets, credentials, customer data, internal URLs, or sensitive session details, and keep the PE_Logs folder private. <br>
Risk: Logs may be written under the wrong PortEden or Google account. <br>
Mitigation: Verify the active PortEden authentication profile, connected Google account, Drive access, and PE_LOG_FOLDER before logging. <br>
Risk: Old daily log documents may retain operational details longer than needed. <br>
Mitigation: Periodically review and delete old log documents that are no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/porteden/docs-logger) <br>
- [PortEden](https://porteden.com) <br>
- [Publisher profile](https://clawhub.ai/user/porteden) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and compact JSON command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces append-only Google Docs logging workflows using the porteden CLI, PE_API_KEY, and an optional PE_LOG_FOLDER environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
