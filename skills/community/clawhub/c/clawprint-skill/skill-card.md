## Description: <br>
Create LLCs for AI agents with human sponsor oversight. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clabasky](https://clawhub.ai/user/clabasky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to discover Clawprint products, register for API credentials, and request AI-agent business formation with human sponsor oversight. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad authenticated access to a sensitive business-formation API with inconsistent scope and weak credential-safety guidance. <br>
Mitigation: Use a dedicated Clawprint account and key, keep the secret key out of chats, logs, screenshots, shell history, and source control, and review the live products list before each action. <br>
Risk: The skill can create businesses, submit sponsor or KYC data, and use banking or payment-related capabilities. <br>
Mitigation: Require explicit human approval before creating businesses, submitting sponsor or KYC data, or invoking banking or payment-related actions. <br>


## Reference(s): <br>
- [Clawprint skill page](https://clawhub.ai/clabasky/clawprint-skill) <br>
- [Clawprint website](https://clawprintai.com) <br>
- [Clawprint API](https://clawprintai.com/api) <br>
- [README.md](README.md) <br>
- [SETUP.md](SETUP.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger authenticated business-formation, KYC, banking, or payment-related API workflows when used with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
