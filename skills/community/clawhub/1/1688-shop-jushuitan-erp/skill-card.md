## Description: <br>
Connects to Jushuitan ERP data and helps merchants configure local access, confirm consent, and analyze shops, products, inventory, orders, purchasing, daily reports, and replenishment reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and operations teams use this skill to connect merchant-provided Jushuitan ERP credentials, record data consent, and ask natural-language questions about authorization, catalog quality, inventory, orders, purchasing, alerts, and recurring business reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Jushuitan ERP credentials locally in plaintext. <br>
Mitigation: Use the skill only when local plaintext storage is acceptable, save credentials only after explicit user authorization, keep the files private, and avoid logging or echoing secrets. <br>
Risk: The skill can issue broad raw ERP API calls without strong scoping or per-use confirmation. <br>
Mitigation: Confirm the active profile, API path, and data domain before use, and grant only the specific read-only API permissions needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-shop-jushuitan-erp) <br>
- [Jushuitan ERP API Map](references/api-map.md) <br>
- [Jushuitan ERP Scenarios](references/scenarios.md) <br>
- [Jushuitan Open Platform](https://openweb.jushuitan.com/) <br>
- [Jushuitan Application Management](https://openweb.jushuitan.com/management/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls, Files] <br>
**Output Format:** [Markdown guidance with JSON or shell command snippets, local configuration updates, and ERP API response summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local profiles.json and consent.json files when the user explicitly authorizes credential storage and data access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
