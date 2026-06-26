## Description: <br>
Chargebee API integration with managed OAuth for administering customers, subscriptions, invoices, and billing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and billing administrators use this skill to query and manage Chargebee customers, subscriptions, invoices, hosted pages, and portal sessions from an agent workflow. It is intended for environments where the user has a valid Maton API key and an authorized Chargebee connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change real Chargebee billing data through an authorized connection. <br>
Mitigation: Use a least-privilege Chargebee/Maton connection, default to read-only checks, and approve only specific write actions after reviewing the target resource and financial impact. <br>
Risk: Requests may target the wrong Chargebee account when multiple connections exist. <br>
Mitigation: Always specify and verify the intended Maton-Connection value before each request, especially before write, update, cancel, or delete actions. <br>
Risk: MATON_API_KEY and connection URLs are sensitive credentials. <br>
Mitigation: Store credentials only in private secret management or environment variables, keep connection URLs private, and revoke unused connections promptly. <br>


## Reference(s): <br>
- [ClawHub Chargebee skill page](https://clawhub.ai/byungkyu/chargebee) <br>
- [Chargebee API Overview](https://apidocs.chargebee.com/docs/api) <br>
- [Chargebee Customers API](https://apidocs.chargebee.com/docs/api/customers) <br>
- [Chargebee Subscriptions API](https://apidocs.chargebee.com/docs/api/subscriptions) <br>
- [Chargebee Invoices API](https://apidocs.chargebee.com/docs/api/invoices) <br>
- [Chargebee Hosted Pages API](https://apidocs.chargebee.com/docs/api/hosted_pages) <br>
- [Maton](https://maton.ai) <br>
- [Maton settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions and Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an authorized Chargebee connection; supports documented read and write billing operations.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
