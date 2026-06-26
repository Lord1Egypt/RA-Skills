## Description: <br>
Interact with FundraiseUp REST API to manage donations, recurring plans, supporters, campaigns, and donor portal access. Process online and offline donations, retrieve fundraising analytics, and integrate with nonprofit CRM systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aamish99](https://clawhub.ai/user/Aamish99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and nonprofit operations teams use this skill to work with FundraiseUp donation, supporter, recurring plan, campaign, event, and donor portal API workflows. It provides API guidance, request examples, and integration patterns for fundraising operations and CRM synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to donor records and donation data, which may include sensitive supporter information. <br>
Mitigation: Use least-privilege FundraiseUp API keys, redact donor PII from prompts, logs, and summaries, and limit retrieval to the records needed for the task. <br>
Risk: The skill includes workflows for live donation creation and other write actions. <br>
Mitigation: Use test-mode keys for development and require human confirmation before every live write action, especially donation creation or recurring plan changes. <br>
Risk: Donor portal access links provide temporary access to sensitive donor account data. <br>
Mitigation: Generate portal links only after validating supporter ownership, use automatic redirects, and never share links through email, SMS, logs, or public channels. <br>


## Reference(s): <br>
- [Fundraise Up REST API Documentation](https://fundraiseup.com/docs/rest-api/) <br>
- [Fundraise Up API Resources](https://fundraiseup.com/docs/rest-api-resources/) <br>
- [Fundraise Up Seamless Donor Portal](https://fundraiseup.com/docs/seamless-donor-portal/) <br>
- [Fundraise Up Support](https://fundraiseup.com/support/) <br>
- [ClawHub Skill Page](https://clawhub.ai/Aamish99/fundraiseup) <br>
- [Publisher Profile](https://clawhub.ai/user/Aamish99) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, curl commands, Python and Node.js code snippets, and JSON request bodies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FundraiseUp API key supplied through FUNDRAISEUP_API_KEY for live API use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
