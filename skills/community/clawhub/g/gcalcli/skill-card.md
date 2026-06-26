## Description: <br>
Interact with Google Calendar via gcalcli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gargravish](https://clawhub.ai/user/gargravish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and employees use this skill to query Google Calendar, review upcoming events, search meeting history, and export meeting attachments such as Gemini notes for planning and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run a custom gcalcli fork while accessing sensitive Google Calendar events, attachments, and meeting notes. <br>
Mitigation: Install and run it only after trusting the custom fork and any local gcmd checkout, and use authenticated accounts with the minimum calendar access needed. <br>
Risk: Example commands include hard-coded calendar addresses, local paths, bulk exports, and downloads of meeting notes. <br>
Mitigation: Replace example calendars and paths with intended targets, avoid bulk export unless required, and write exports only to a secure directory. <br>
Risk: Cached Google credentials may remain available after use on shared or less trusted systems. <br>
Mitigation: Clear cached credentials or revoke Google OAuth access after use when operating outside a trusted personal environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gargravish/gcalcli) <br>
- [Official gcalcli documentation](https://github.com/insanum/gcalcli) <br>
- [Custom gcalcli fork with attachment support](https://github.com/shanemcd/gcalcli/tree/attachments-in-tsv-and-json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples and JSON or TSV output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may access Google Calendar data and export meeting attachments when run with authenticated credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
