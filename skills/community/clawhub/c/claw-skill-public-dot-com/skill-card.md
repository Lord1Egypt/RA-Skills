## Description: <br>
Interact with your Public.com brokerage account using the Public.com API to view portfolio information, get stock quotes, place trades, and get account updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarricsookdeo](https://clawhub.ai/user/tarricsookdeo) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve Public.com account data, inspect market and options information, preflight orders, place trades, and cancel orders through Public.com API-backed scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access brokerage account data and submit or cancel real orders. <br>
Mitigation: Use deliberate user control, require explicit human confirmation before every trade or cancellation, and review order details before execution. <br>
Risk: Public.com API credentials grant sensitive account access. <br>
Mitigation: Use the least-privileged API key or a test account when possible, store credentials in the configured secure file location, and avoid sharing command output that contains account identifiers. <br>
Risk: Options automation examples can lead to unintended live trading losses if run unattended. <br>
Mitigation: Avoid unattended execution with real funds; use preflight checks and test accounts before placing live orders. <br>


## Reference(s): <br>
- [Public.com signup](https://public.com/signup) <br>
- [Public.com API settings](https://public.com/settings/v2/api) <br>
- [Options Automation Playbook](options-automation-library.md) <br>
- [ClawHub skill page](https://clawhub.ai/tarricsookdeo/claw-skill-public-dot-com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account, portfolio, quote, order, transaction, option-chain, option-greek, preflight, order-placement, and cancellation outputs from Public.com API calls.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
