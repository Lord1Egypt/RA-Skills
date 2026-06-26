## Description: <br>
Connect your AI to 30+ business tools, including Gmail, Calendar, Sheets, Mindbody, Meta Ads, Linear, Airtable, Notion, Stripe, and more, through one Bellink URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barflotek](https://clawhub.ai/user/barflotek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use Bellink to connect an AI assistant to business applications through a Bellink MCP endpoint, enabling the agent to retrieve information and perform app actions such as sending messages, booking appointments, creating issues, and updating records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BELLINK_URL contains an authentication key and can grant access to connected business apps if exposed. <br>
Mitigation: Treat BELLINK_URL like a password: do not share it, commit it, paste it into public chats, or leave it in logs. <br>
Risk: Connected app actions may send messages, book appointments, write records, or change business data. <br>
Mitigation: Connect only the apps needed for the use case and require manual confirmation before the agent performs write or state-changing actions. <br>


## Reference(s): <br>
- [Bellink website](https://www.bellink.io) <br>
- [Bellink dashboard](https://app.bellink.io) <br>
- [bellink-mcp npm package](https://www.npmjs.com/package/bellink-mcp) <br>
- [ClawHub Bellink listing](https://clawhub.ai/barflotek/bellink) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BELLINK_URL, a credential-bearing MCP endpoint URL from the Bellink dashboard.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
