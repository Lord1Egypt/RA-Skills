## Description: <br>
Agent Commerce Engine is a production-ready universal engine that lets autonomous agents interact with compatible headless e-commerce backends through a standardized protocol for product discovery, cart operations, and secure user management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NowLoadY](https://clawhub.ai/user/NowLoadY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and commerce operators use this skill to connect agents to compatible headless e-commerce stores for product search, cart management, account flows, profile updates, order creation, and payment handoff. Agents use it to issue commerce CLI commands and interpret structured store responses while leaving final payment authorization to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store account tokens locally and interact with carts, profile details, and unpaid order creation for connected stores. <br>
Mitigation: Use only trusted HTTPS store URLs, keep credential files local to the user environment, run logout to purge saved credentials when finished, and confirm cart, profile, and order changes before execution. <br>
Risk: Registration or authentication flows may expose sensitive tokens or account details in command output if a backend returns them unexpectedly. <br>
Mitigation: Review registration and login output before sharing it, avoid pasting command output into public channels, and use known compatible stores with clear token handling. <br>
Risk: Agents can prepare an order-ready checkout state, but they cannot complete consumer payment authorization. <br>
Mitigation: Return any payment or order URL to the human user for final payment approval instead of attempting automated payment completion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NowLoadY/agent-commerce-engine) <br>
- [GitHub Repository](https://github.com/NowLoadY/agent-commerce-engine) <br>
- [README.md](README.md) <br>
- [SERVER_SPEC.md](SERVER_SPEC.md) <br>
- [Lafeitu Gourmet Skill Reference Case](https://clawhub.com/NowLoadY/agentic-spicy-food) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON or human-readable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the requests package; uses optional COMMERCE_URL and COMMERCE_BRAND_ID environment variables and local per-domain credential files.] <br>

## Skill Version(s): <br>
1.7.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
