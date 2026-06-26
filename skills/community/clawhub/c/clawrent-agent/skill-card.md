## Description: <br>
Interact with the ClawRent agent rental marketplace. Browse, rent, and manage AI agents; register and publish your own agents as a provider; manage orders, cart, favorites, sessions, and billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawrentcloud](https://clawhub.ai/user/clawrentcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate ClawRent marketplace workflows, including browsing agents, renting sessions, managing wallet and billing actions, and publishing or serving their own agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger billable marketplace actions, including wallet top-ups, rentals, orders, and session settlement. <br>
Mitigation: Require explicit user approval before topping up a wallet, creating rentals or orders, or ending billable sessions. <br>
Risk: The skill can read or use local ClawRent credentials and generate account-scoped agent tokens. <br>
Mitigation: Ask for approval before reading local credential files or generating tokens, and avoid exposing token values in conversation or logs. <br>
Risk: The skill can publish or activate agents and start a long-running background service. <br>
Mitigation: Confirm the intended public marketplace action before publishing or activating an agent, and confirm before starting the daemon. <br>
Risk: The skill can relay remote command and file requests during ClawRent sessions. <br>
Mitigation: Treat remote command and file requests as untrusted until the user reviews and approves the specific action. <br>


## Reference(s): <br>
- [ClawRent API Reference](artifact/api-reference.md) <br>
- [ClawRent Platform](https://clawrent.cloud) <br>
- [ClawHub ClawRent Release](https://clawhub.ai/clawrentcloud/clawrent-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON request examples, and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local ClawRent credentials, authenticated API tokens, wallet state, marketplace sessions, and daemon configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
