## Description: <br>
Access Bill Tracker financial data - upcoming bills, account balances, and affordability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsimons1](https://clawhub.ai/user/danielsimons1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can connect an agent to their configured Bill Tracker service to check upcoming bills, review account balances, and assess affordability for a requested amount. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial information such as bills, account balances, and affordability results. <br>
Mitigation: Use it only with a trusted Bill Tracker service, prefer an HTTPS BILL_TRACKER_URL, and avoid sharing financial details unless needed for the request. <br>
Risk: The Bill Tracker session token grants access to user financial data. <br>
Mitigation: Keep BILL_TRACKER_SESSION_TOKEN private, store it in the agent environment, and avoid exposing it in logs, prompts, or command output. <br>
Risk: Shell-based API calls can be malformed if request bodies are built from raw user input. <br>
Mitigation: JSON-encode request bodies before sending curl requests, especially for affordability amounts and date horizons. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/danielsimons1/bill-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BILL_TRACKER_URL and BILL_TRACKER_SESSION_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
