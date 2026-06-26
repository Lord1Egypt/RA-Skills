## Description: <br>
Agentlair Email helps agents claim @agentlair.dev email identities and send or receive email through a REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hawkaa](https://clawhub.ai/user/hawkaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill when an agent needs a dedicated email identity, outbound email delivery, inbox checks, or message retrieval without SMTP or IMAP setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agents to send real email and access mailbox data. <br>
Mitigation: Confirm recipients, subject, body, and mailbox access before use. <br>
Risk: The AGENTLAIR_API_KEY credential and message contents are sensitive. <br>
Mitigation: Keep the API key private and avoid sensitive or regulated email unless AgentLair retention, deletion, and access-control practices have been verified. <br>


## Reference(s): <br>
- [AgentLair homepage](https://agentlair.dev) <br>
- [ClawHub skill page](https://clawhub.ai/hawkaa/agentlair-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include API endpoints, request fields, environment variable setup, and operational cautions for email delivery and mailbox access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
