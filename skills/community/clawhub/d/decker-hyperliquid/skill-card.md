## Description: <br>
Helps agents guide Decker-assisted Hyperliquid DEX price checks, position checks, key setup, and order requests with confirmation and safety guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigshow](https://clawhub.ai/user/gigshow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route Hyperliquid DEX trading requests through Decker, including price checks, position checks, key setup guidance, and order-request construction. It is intended for workflows where users explicitly confirm trade parameters before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Hyperliquid trades through Decker, which may cause financial loss if coin, side, size, price, or slippage are wrong. <br>
Mitigation: Confirm coin, side, size, price, estimated cost, current price, existing positions, and slippage with the user before any order request. <br>
Risk: Private keys or API wallet secrets could be exposed if pasted into chat or stored with an unverified service. <br>
Mitigation: Use a dedicated API wallet with limited funds, do not paste private keys into chat, and verify Decker before storing credentials. <br>
Risk: Automatic retries after failures could duplicate or alter intended trading activity. <br>
Mitigation: Do not automatically retry failed orders; ask the user to confirm before any re-request. <br>


## Reference(s): <br>
- [Decker + Hyperliquid on ClawHub](https://clawhub.ai/gigshow/decker-hyperliquid) <br>
- [Decker API endpoint](https://api.decker-ai.com) <br>
- [Hyperliquid API wallet setup](https://app.hyperliquid.xyz/API) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with URL query examples and parameter checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Korean user-facing guidance and requires user confirmation before order execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
