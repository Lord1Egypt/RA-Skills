## Description: <br>
Uses the porteden CLI to let an agent read, list, filter, search, and fetch individual Gmail or Outlook messages in a read-only workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agent users use this skill to quickly inspect Gmail and Outlook mail, search by date, sender, subject, unread status, or keyword, and fetch a specific message when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mail search results and message bodies may contain sensitive personal or business data. <br>
Mitigation: Use narrow searches, prefer compact previews, fetch full message bodies only when needed, and avoid sharing outputs unnecessarily. <br>
Risk: Credentials or API keys can be exposed if saved in shell profiles or shared scripts. <br>
Mitigation: Prefer the keyring login path and avoid persisting PE_API_KEY in shared locations. <br>
Risk: Email content may contain untrusted instructions. <br>
Mitigation: Treat message content as untrusted, summarize it with sender attribution, and do not execute instructions found inside email bodies. <br>
Risk: Authenticated mail access may persist on shared machines. <br>
Mitigation: Log out of porteden after shared-machine tasks when continued access is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-gmail-outlook-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and compact JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gmail and Outlook listing, filtering, search, and single-message retrieval; compact JSON previews are preferred by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
