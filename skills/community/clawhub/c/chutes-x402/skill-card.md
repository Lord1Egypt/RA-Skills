## Description: <br>
Build a pay-per-inference proxy for Bittensor Chutes AI. Accept USDC payments for decentralized AI inference using x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primer-dev](https://clawhub.ai/user/primer-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI service operators use this skill to scaffold and configure a Chutes AI proxy that accepts USDC payments through x402 and forwards paid inference requests to Bittensor Chutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs third-party x402 or Primer packages and generated project code. <br>
Mitigation: Review the package source, generated files, and dependency changes before running or deploying the proxy. <br>
Risk: The proxy requires a Chutes API key and wallet address and is intended to process paid inference requests. <br>
Mitigation: Use dedicated credentials, start with low payment limits, and verify pricing and wallet configuration before accepting real payments. <br>
Risk: The artifact notes approximate token estimation, pre-payment only, and no streaming support. <br>
Mitigation: Document these limits for users and test expected request sizes, prices, and non-streaming behavior before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/primer-dev/chutes-x402) <br>
- [Chutes AI](https://chutes.ai) <br>
- [Bittensor](https://bittensor.com) <br>
- [x402 Protocol](https://x402.org) <br>
- [x402 Bittensor documentation](https://x402.org/docs/bittensor.html) <br>
- [Primer Systems](https://primer.systems) <br>
- [Primer Systems x402 repository](https://github.com/primer-systems/x402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment variables, API endpoint descriptions, and scaffolded project instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup commands for Node.js, Python, Cloudflare Workers, Docker, and other deployment targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
