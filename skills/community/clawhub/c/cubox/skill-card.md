## Description: <br>
Save web pages and memos to Cubox using the Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liam8](https://clawhub.ai/user/Liam8) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to save selected web pages and quick text memos into Cubox with optional titles, descriptions, tags, and folder placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Cubox API URL is a credential that can authorize saves to the user's Cubox account. <br>
Mitigation: Store CUBOX_API_URL privately, avoid logging or sharing it, and rotate it if it is exposed. <br>
Risk: Selected URLs, memos, tags, and descriptions are sent to Cubox for storage and processing. <br>
Mitigation: Do not send confidential, regulated, secret, or otherwise sensitive content unless the user is comfortable storing it in Cubox. <br>
Risk: Cubox Premium API usage is limited to 500 calls per day. <br>
Mitigation: Use the skill for selected saves and monitor usage if running it in repeated or automated workflows. <br>


## Reference(s): <br>
- [Cubox API Help](https://help.cubox.pro/save/89d3/) <br>
- [Cubox](https://cubox.pro) <br>
- [ClawHub Skill Page](https://clawhub.ai/Liam8/cubox) <br>
- [Publisher Profile](https://clawhub.ai/user/Liam8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Cubox save requests for user-provided URLs or memo text; requires a user-configured CUBOX_API_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
