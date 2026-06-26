## Description: <br>
Query and filter court-released Jeffrey Epstein email records through a structured JSON API that uses x402 payments in USDC on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlockBoy32](https://clawhub.ai/user/BlockBoy32) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and records analysts use this skill to preview, search, and retrieve structured email records from the court-released Epstein archive while managing x402 payment consent and spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private key exposure could compromise funds. <br>
Mitigation: Use a dedicated low-balance Base wallet, provide the key only through an environment variable, and never log, display, or echo it. <br>
Risk: Paid API requests or pagination could spend more USDC than intended. <br>
Mitigation: Use the free preview endpoint first, estimate request cost, set a spending limit when supported, and get explicit user approval before paid calls or pagination. <br>
Risk: Public-record email data could be misused to harass, doxx, or expose unnecessary personal details. <br>
Mitigation: Use the archive for legitimate records research and avoid unnecessary disclosure of personal details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BlockBoy32/epstein-emails) <br>
- [Epstein Emails API](https://epsteinemails.xyz) <br>
- [x402 protocol](https://x402.org) <br>
- [U.S. Department of Justice Epstein source documents](https://www.justice.gov/epstein) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands] <br>
**Output Format:** [Markdown with JSON examples and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request guidance and structured JSON response examples for preview, search, filtering, and pagination workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
