## Description: <br>
Register domains, manage DNS, and set up email sending via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check domain availability and pricing, register domains, manage DNS records, and configure email sending through the GetPost API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key exposure can allow unauthorized GetPost domain management actions. <br>
Mitigation: Keep the API key secret and provide it only in secure agent or shell environments. <br>
Risk: Domain registration, DNS edits, and email or redirect setup can spend credits or alter live infrastructure. <br>
Mitigation: Start with availability and pricing endpoints, then require confirmation of the exact domain, price or credits, DNS record values, and email or redirect changes before any POST request. <br>


## Reference(s): <br>
- [GetPost API reference: domains](https://getpost.dev/docs/api-reference#domains) <br>
- [ClawHub skill page](https://clawhub.ai/dommholland/getpost-domains) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and API endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GetPost API key; POST requests can register domains or change DNS, email, and redirect settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
