## Description: <br>
DanceArc helps agents and developers implement, debug, and explain Arc Testnet native USDC payment flows using HTTP 402 x402-shaped challenges, Circle Gateway verification, and human/agent settlement patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to work with DanceArc payment flows, including pay-per-call APIs, Arc Testnet USDC transfers, Circle wallet integration, and troubleshooting payment verification failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment instructions can cause users or agents to send USDC to the wrong chain, recipient, or amount. <br>
Mitigation: Confirm the chain, recipient, and amount against the challenge or health endpoint before sending any USDC. <br>
Risk: Circle credentials and private keys may be exposed if copied into browser or agent-visible contexts. <br>
Mitigation: Keep Circle secrets and private keys in server-side or local test contexts only, and never commit environment files. <br>
Risk: Manual installation from an external repository can introduce unreviewed code or documentation changes. <br>
Mitigation: Verify the external repository and review the skill contents before installing or using it. <br>


## Reference(s): <br>
- [DanceArc ClawHub page](https://clawhub.ai/arunnadarasa/dancearc) <br>
- [DanceArc repository](https://github.com/arunnadarasa/dancearc) <br>
- [API routes](references/api-routes.md) <br>
- [Payment flow](references/payment-flow.md) <br>
- [OpenClaw workspace hints](references/openclaw-workspace.md) <br>
- [Arc docs - Connect to Arc](https://docs.arc.network/arc/references/connect-to-arc) <br>
- [Circle Modular Wallets Web SDK](https://developers.circle.com/w3s/modular-wallets-web-sdk) <br>
- [x402 package](https://www.npmjs.com/package/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, API route guidance, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment-flow checklists, troubleshooting steps, route references, environment variable guidance, and example command sequences.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
