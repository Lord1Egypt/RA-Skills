## Description: <br>
Fetches the latest Bloomberg headlines when a user asks for Bloomberg news, financial headlines, or current market updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8treenet](https://clawhub.ai/user/8treenet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent Bloomberg headline data and present each item with a title, link, and localized publication time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external bbgwire Go CLI for headline retrieval. <br>
Mitigation: Review the bbgwire package before deployment and pin a reviewed module version in controlled environments. <br>
Risk: Headline output is time-sensitive and may be incomplete or unavailable if the external source or CLI fails. <br>
Mitigation: Treat headline summaries as informational and verify important items through linked source pages before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/8treenet/bloomberg-headlines) <br>
- [Publisher profile](https://clawhub.ai/user/8treenet) <br>
- [bbgwire Go module](https://github.com/8treenet/bbgwire) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown] <br>
**Output Format:** [Markdown summary of JSON headline results with titles, links, and localized publication times] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 50 recent headlines and requires macOS with the bbgwire CLI available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
