## Description: <br>
AIUSD Pro is an AI-powered trading agent that lets users trade, check balances, and manage positions through natural language conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech-FE-aiusd](https://clawhub.ai/user/tech-FE-aiusd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to interact with AIUSD through natural language for balance checks, trading, staking, position management, and market queries. Agents use it to relay user intent to the AIUSD CLI, handle authentication and session flow, and return the backend response to the authenticated user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates trading, staking, cancellation, and position-management actions to an external AIUSD CLI and backend. <br>
Mitigation: Use only when the user trusts the aiusd-pro npm package and AIUSD backend, and require exact confirmation of asset, amount, venue, leverage, fees, and risk before any financial action. <br>
Risk: The skill maintains session context and may return backend links or raw outputs that expose account or trading information. <br>
Mitigation: Relay outputs only to the authenticated user and avoid sharing AIUSD links or response content outside that user's session. <br>


## Reference(s): <br>
- [AIUSD Pro on ClawHub](https://clawhub.ai/tech-FE-aiusd/aiusd-pro) <br>
- [tech-FE-aiusd Publisher Profile](https://clawhub.ai/user/tech-FE-aiusd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and relayed CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include an AIUSD browser link for continuing the authenticated conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
