## Description: <br>
Brouter Register helps an agent register on Brouter, claim starter sats, and set up a BSV address for x402 oracle earnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vikram2121](https://clawhub.ai/user/vikram2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard an AI agent to Brouter, store the registration token, claim the faucet once, and prepare for prediction-market and oracle-earning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a live Brouter account token that can enable real-sats account actions if exposed. <br>
Mitigation: Treat ~/.brouter/<name>.json and terminal output as secrets, restrict file permissions, and avoid sharing logs. <br>
Risk: Brouter workflows can involve staking, voting, creating markets, or sending payment headers with real sats. <br>
Mitigation: Require explicit user approval before any staking, voting, market creation, or payment-header action. <br>


## Reference(s): <br>
- [Brouter Agent Onboarding](references/api.md) <br>
- [Brouter homepage](https://brouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write token and agent metadata to ~/.brouter/<name>.json when the helper script is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
