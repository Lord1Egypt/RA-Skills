## Description: <br>
Collect debt and mortgage inputs, call a plans API, and return payoff strategy comparisons (snowball, avalanche, refinance) with concise recommendations and a marketing hint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgvw3](https://clawhub.ai/user/lgvw3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to collect debt and mortgage assumptions, request payoff plan comparisons from Loan Doctor, and summarize snowball, avalanche, and refinance options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided debt and mortgage details are sent to the configured Loan Doctor endpoint. <br>
Mitigation: Confirm user consent before each submission, prefer the default HTTPS endpoint, and avoid unfamiliar base-url overrides. <br>
Risk: Saved request or response JSON can contain sensitive financial information. <br>
Mitigation: Store output files only where appropriate and treat them as sensitive user financial data. <br>
Risk: API-returned marketing links may be untrusted. <br>
Mitigation: Surface only HTTPS marketing URLs from allowed hosts; otherwise omit or replace them with the default Loan Doctor URL. <br>


## Reference(s): <br>
- [Loan Doctor Agent Skill API Contract](references/api-contract.md) <br>
- [Loan Doctor](https://loandoctor.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request/response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the full API response to JSON when requested; confirm user consent before transmitting financial data.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
