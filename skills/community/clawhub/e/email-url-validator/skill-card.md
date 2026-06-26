## Description: <br>
Validate email addresses, URLs, and domains with live DNS, DNSBL, HTTP reachability, redirect-chain, WHOIS, disposable-domain, and heuristic risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vannelier](https://clawhub.ai/user/vannelier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to validate email addresses, URLs, domains, bulk lists, and uploaded contact or link files before acting on them. It is suited to workflows that need reachable-contact checks, redirect inspection, or domain qualification with an explicit quote-and-approval flow for paid validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags this hosted validation service for review because it can send emails, URLs, domains, and large contact files to the listed operator. <br>
Mitigation: Use the quote-and-approval flow, remove unnecessary columns before upload, and avoid internal URLs or regulated personal data unless approved. <br>
Risk: Webhook callbacks can disclose job metadata to the callback endpoint. <br>
Mitigation: Use webhook_url only for callback endpoints you control and where job metadata disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vannelier/email-url-validator) <br>
- [Hosted service endpoint](https://deep-validator-production.up.railway.app) <br>
- [Operator source code](https://github.com/nathanleclaire/Agent_Validator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, markdown, shell commands, files] <br>
**Output Format:** [Markdown guidance with HTTP API examples; validation calls return JSON responses or CSV/XLSX result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include recommended_action fields for agents to use directly; file validation can return async job IDs and downloadable results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
