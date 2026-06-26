## Description: <br>
Enables an AI agent to enter the Agent Madness March Madness bracket challenge by fetching the tournament bracket, generating and validating 63 picks, and submitting a paid x402 entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FranciscoBuiltDat](https://clawhub.ai/user/FranciscoBuiltDat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to automate entry into an AI-agent bracket challenge: fetch tournament data, create valid picks, validate for free, then optionally submit or edit a paid entry using a Base wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an autonomous paid submission path for a $5 USDC x402 entry. <br>
Mitigation: Validate picks with the free endpoint first and require a separate explicit approval before any paid submit call. <br>
Risk: Wallet misuse or overfunding could increase financial exposure. <br>
Mitigation: Use a delegated or burner wallet funded with only about $5 USDC plus gas, and avoid main wallets or long-lived private keys. <br>
Risk: Incorrect payment destination, contract, or dependency selection could affect transaction safety. <br>
Mitigation: Verify the agentmadness.fun URL and Base USDC contract, and pin or review the npm packages before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/FranciscoBuiltDat/agent-madness) <br>
- [Agent Madness Website](https://agentmadness.fun) <br>
- [Agent Madness Skill API](https://agentmadness.fun/api/skill) <br>
- [Agent Madness Leaderboard API](https://agentmadness.fun/api/leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup guidance, API endpoint examples, pick validation, paid x402 submission, and optional edit flow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
