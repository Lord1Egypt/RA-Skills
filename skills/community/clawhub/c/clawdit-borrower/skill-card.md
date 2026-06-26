## Description: <br>
Become an autonomous borrowing agent that uses a WDK-powered smart wallet, ERC-8004 reputation data, balances, PnL, API billing, and revenue signals to request and repay P2P loans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NatX223](https://clawhub.ai/user/NatX223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent register a smart wallet and ERC-8004 profile, evaluate its financial position and reputation, request P2P loans, and manage repayments through the Clawdit service. It is intended for agentic crypto-borrowing workflows that need explicit borrowing limits, repayment strategy, and operator oversight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to request loans and make repayments through a crypto wallet. <br>
Mitigation: Use explicit borrowing and repayment limits, require per-action approval for loan requests and repayments, and keep a clear pause or revocation process available. <br>
Risk: The skill instructs the agent to retain an agentCode transaction passkey and exposes wallet, billing, revenue, reputation, and profile data to an external service. <br>
Mitigation: Store agentCode only in secure secret storage outside ordinary memory and treat wallet, billing, revenue, reputation, and profile data as sensitive information. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/NatX223/clawdit-borrower) <br>
- [Publisher profile](https://clawhub.ai/user/NatX223) <br>
- [ERC-8004 registration specification](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON request bodies, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for registration, wallet setup, loan requests, repayment checks, and error handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
