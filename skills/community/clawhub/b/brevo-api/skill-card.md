## Description: <br>
Brevo API integration with managed OAuth for email marketing, transactional emails, SMS, contacts, CRM, campaigns, lists, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Brevo through Maton-managed OAuth, including sending email, managing contacts and lists, creating campaigns, and working with templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY and uses Maton to proxy Brevo API traffic and manage OAuth for the connected Brevo account. <br>
Mitigation: Keep MATON_API_KEY private, avoid sharing terminal output that may reveal it, and install only when the user trusts Maton for Brevo API access. <br>
Risk: Write, send, update, and delete operations can affect contacts, lists, campaigns, templates, senders, and outgoing email. <br>
Mitigation: Require explicit user approval before write or send actions, and confirm recipients, lists, campaign IDs, resource IDs, and expected effects first. <br>
Risk: Requests may target the wrong Brevo account when multiple OAuth connections exist. <br>
Mitigation: Use the Maton-Connection header to specify the intended connection when multiple Brevo accounts are available. <br>


## Reference(s): <br>
- [ClawHub Brevo release](https://clawhub.ai/byungkyu/brevo-api) <br>
- [Brevo API Overview](https://developers.brevo.com/) <br>
- [Brevo API Key Concepts](https://developers.brevo.com/docs/how-it-works) <br>
- [Brevo OAuth 2.0](https://developers.brevo.com/docs/integrating-oauth-20-to-your-solution) <br>
- [Manage Contacts](https://developers.brevo.com/docs/synchronise-contact-lists) <br>
- [Send Transactional Email](https://developers.brevo.com/docs/send-a-transactional-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API examples and inline shell or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Brevo OAuth connection managed by Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
