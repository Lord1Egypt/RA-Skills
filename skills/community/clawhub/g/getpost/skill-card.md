## Description: <br>
The API platform for bots. Email, SMS, search, scrape, AI, domains, shipping - one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill as a reference for connecting bots to the GetPost API for messaging, web access, AI generation, domain management, shipping labels, credits, webhooks, and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes broad paid and destructive API actions, including sending messages, buying credits, registering domains, modifying DNS, creating shipping labels, registering webhooks, and deleting resources. <br>
Mitigation: Require manual confirmation before paid, destructive, or external-communication actions, and set spending limits where possible. <br>
Risk: A GetPost API key may grant broad paid authority if exposed to prompts, logs, or untrusted tools. <br>
Mitigation: Keep the key out of prompts and logs, store it in a secrets manager or protected environment variable, and use only keys the operator is comfortable granting to the agent. <br>


## Reference(s): <br>
- [GetPost OpenAPI Specification](https://getpost.dev/api/openapi.json) <br>
- [GetPost Pricing](https://getpost.dev/api/pricing) <br>
- [ClawHub Package Page](https://clawhub.ai/dommholland/getpost) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline API routes and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References a credits-based external API and requires a bearer API key for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
