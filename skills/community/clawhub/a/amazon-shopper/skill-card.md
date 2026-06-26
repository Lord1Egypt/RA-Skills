## Description: <br>
Buy and return items on Amazon using browser automation. Use for purchasing, reordering, checking order history, and processing returns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to direct an agent-driven browser session for Amazon purchasing, reordering, order-history lookup, and returns. The workflow requires careful user oversight because it can access account sessions and submit purchases or returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle Amazon account access and may encounter credentials. <br>
Mitigation: Use only with manual Amazon login, do not let the agent access a password manager, and prefer a dedicated browser profile. <br>
Risk: The skill can complete purchases or returns without enough user approval. <br>
Mitigation: Require explicit final confirmation before any purchase or return is submitted. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review carefully before installing and keep the browser session visible when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/amazon-shopper) <br>
- [Amazon order history](https://www.amazon.com/gp/your-account/order-history) <br>
- [Amazon](https://www.amazon.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and procedural browser-automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots and short confirmation summaries during shopping and return flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
