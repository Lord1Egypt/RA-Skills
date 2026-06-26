## Description: <br>
Local CLI tool for B.Fun (BSC) market inspection, quotes, token details, tax info, and explicitly user-confirmed token operations, with structured JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bfun-ai](https://clawhub.ai/user/bfun-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect B.Fun markets on BSC, retrieve quotes and token details, and run explicitly confirmed token, wallet, and identity operations through the local B.Fun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a disclosed crypto wallet helper and can use a private key for irreversible BSC transactions. <br>
Mitigation: Use a dedicated low-balance wallet, never paste private keys or seed phrases into chat, and confirm address, amount, slippage, network, and token details before signing. <br>
Risk: The installation instructions use an unpinned external npm CLI package when installed with @latest. <br>
Mitigation: Verify the npm package and source before installation and prefer a pinned package version. <br>
Risk: Token creation can upload images and metadata to external services. <br>
Mitigation: Treat token images and metadata as externally shared data and review them before running creation commands. <br>


## Reference(s): <br>
- [B.Fun AI Skill Page](https://clawhub.ai/bfun-ai/bfun-agentic) <br>
- [Contract Addresses](references/contract-addresses.md) <br>
- [Create Flow](references/create-flow.md) <br>
- [Errors](references/errors.md) <br>
- [Token Phases](references/token-phases.md) <br>
- [Trade Flow](references/trade-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summarized JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing operations require transaction-specific user confirmation and local signing configuration.] <br>

## Skill Version(s): <br>
0.5.4 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
