## Description: <br>
Automatically identifies todo tables in Feishu documents, parses fuzzy dates, and creates Feishu calendar events with owners and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using Feishu can use this skill to turn document-based milestone tables into calendar reminders. It helps agents read todo rows, resolve dates and assignees, and prepare or execute calendar creation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Feishu document content and may expose document details through calendar entries, invitations, or notifications. <br>
Mitigation: Use it only on documents whose contents are intended to become calendar data, and review extracted todos, assignees, invitees, and descriptions before event creation. <br>
Risk: Broad triggers and limited confirmation guidance can lead to unintended calendar events or invitations. <br>
Mitigation: Require explicit user confirmation of the parsed todo list, resolved dates, attendees, and reminder settings before running calendar creation commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/icesumer-lgtm/feishu-doc-todo) <br>
- [OpenClaw documentation](https://openclaw.dev/) <br>
- [Feishu calendar API documentation](https://open.feishu.cn/document/ukTMukTMukTM/ucjM14iNz4yM14iN) <br>
- [Feishu document API documentation](https://open.feishu.cn/document/ukTMukTMukTM/ucjM14iNz4yM14iN) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create calendar events, attendees, descriptions, and reminder settings when run with Feishu document and calendar access.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
