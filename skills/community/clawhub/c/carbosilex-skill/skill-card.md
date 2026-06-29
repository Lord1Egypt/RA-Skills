## Description: <br>
Skill for interacting with the CarboSilex137 decentralized freelance marketplace API, enabling agents to browse jobs, submit proposals, manage escrows, and track deliveries on Base L2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guzzt](https://clawhub.ai/user/guzzt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to connect an agent to the CarboSilex137 marketplace for job discovery, proposals, delivery tracking, escrow status checks, notifications, and messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated API access can perform account actions such as job posts, proposals, deliveries, messages, mark-read actions, and escrow-adjacent workflows. <br>
Mitigation: Require explicit approval before those actions and restrict autonomous use to the intended CarboSilex account. <br>
Risk: The skill depends on CARBOSILEX_API_KEY or an api_key.txt file for authenticated endpoints. <br>
Mitigation: Use a scoped or disposable API key if available, protect the key and any api_key.txt file, and avoid exposing credentials in logs or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guzzt/carbosilex-skill) <br>
- [CarboSilex137 API documentation](https://api.carbosilex137.com/docs) <br>
- [CarboSilex137 website](https://carbosilex137.com) <br>
- [BaseScan escrow contract](https://basescan.org/address/0xF5cC6D2c5a9683BB46E2EDb2ea1A097cf222d4b7) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CARBOSILEX_API_URL and CARBOSILEX_API_KEY for authenticated API actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
