## Description: <br>
Generate beautiful charts by paying per request with x402 micropayments (USDC on Base) instead of an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbyg603](https://clawhub.ai/user/bobbyg603) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate PNG charts through a pay-per-call x402 workflow when they have an EVM wallet with USDC on Base and do not want to use a Chart Splat API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real USDC through an x402 pay-per-request chart workflow. <br>
Mitigation: Use only a fresh low-balance wallet intended for this skill and confirm each paid request before running it. <br>
Risk: The workflow requires access to a raw EVM private key through X402_PRIVATE_KEY or an equivalent CLI option. <br>
Mitigation: Use environment-based secret handling, avoid main wallets, and do not paste or store high-value wallet keys in project files. <br>
Risk: The documented npx workflow may run an unpinned npm CLI package. <br>
Mitigation: Review or pin the npm CLI package before exposing the wallet key in sensitive environments. <br>


## Reference(s): <br>
- [Chart Splat homepage](https://chartsplat.com) <br>
- [Chart Splat docs](https://chartsplat.com/docs) <br>
- [x402 Protocol Reference](references/x402-protocol.md) <br>
- [x402 Protocol and SDKs](https://github.com/x402-foundation/x402) <br>
- [Coinbase x402 facilitator](https://x402.org/facilitator) <br>
- [EIP-3009 Transfer With Authorization](https://eips.ethereum.org/EIPS/eip-3009) <br>
- [Sample chart configurations](examples/sample-charts.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands, JSON configuration examples, and PNG file output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated chart is saved as a PNG file at the requested output path, and successful paid requests may include a BaseScan settlement URL for auditing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
