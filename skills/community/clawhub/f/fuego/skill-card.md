## Description: <br>
Local Solana agent wallet with local infra for transfers (SOL, USDC, USDT), Jupiter swaps, and x402 purch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willmcdeezy](https://clawhub.ai/user/willmcdeezy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Fuego to create and manage a local Solana wallet for balance checks, SOL and SPL token transfers, Jupiter swap quotes and execution, and x402 purchases. It is intended for local-agent payment workflows where wallet keys remain on the user's machine except for the documented x402 server-side signing flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents real-money Solana payment authority for transfers, swaps, and x402 purchases. <br>
Mitigation: Use a fresh low-balance wallet and require explicit human approval before every transfer, swap, or x402 purchase, including recipient, amount, token, network, product, and personal data. <br>
Risk: The workflow depends on externally installed fuego-cli code. <br>
Mitigation: Review and pin the external fuego-cli package before installation or updates. <br>
Risk: The local wallet file and x402 signing path can expose funds if the host or local process boundary is not trusted. <br>
Mitigation: Keep wallet files protected, keep the server stopped when not actively needed, and use strong local user isolation. <br>


## Reference(s): <br>
- [Fuego Homepage](https://fuego.cash) <br>
- [Fuego ClawHub Listing](https://clawhub.ai/willmcdeezy/fuego) <br>
- [Publisher Profile](https://clawhub.ai/user/willmcdeezy) <br>
- [Jupiter Portal](https://portal.jup.ag) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for local wallet setup, transaction execution, swap flows, and localhost API use.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
