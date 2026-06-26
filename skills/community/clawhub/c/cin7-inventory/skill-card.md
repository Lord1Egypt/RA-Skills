## Description: <br>
Cin7 Core inventory management -- products, stock, orders, purchases, customers, and suppliers via bash scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yashthesiya1](https://clawhub.ai/user/Yashthesiya1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operations teams, developers, and agents use this skill to query and manage Cin7 Core products, stock, sales orders, purchase orders, customers, and suppliers from bash scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Cin7 stock, sales, and purchase records without built-in confirmation or dry-run safeguards. <br>
Mitigation: Require human review before running write commands such as stock adjustments, stock transfers, order updates, and purchase creation. <br>
Risk: The skill requires Cin7 API credentials and may load them from a local .env file. <br>
Mitigation: Use a least-privileged Cin7 API key where possible and protect any .env file from disclosure. <br>
Risk: API requests are sent to the configured Cin7 endpoint using the provided credentials. <br>
Mitigation: Verify CIN7_API_URL before execution and keep the default endpoint unless a trusted alternate endpoint is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yashthesiya1/cin7-inventory) <br>
- [Cin7 Core API Docs](https://help.core.cin7.com/) <br>
- [Cin7 Core API base URL](https://inventory.dearsystems.com/ExternalApi/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and bash with CIN7_ACCOUNT_ID and CIN7_APP_KEY environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
