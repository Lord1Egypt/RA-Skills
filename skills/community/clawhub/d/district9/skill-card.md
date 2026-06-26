## Description: <br>
Autonomous meme token launcher on BNB Chain that senses trends, generates token concepts and logos, and can deploy tokens on-chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearl799](https://clawhub.ai/user/pearl799) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to run an OpenClaw-based agent that monitors market and news signals, generates meme-token assets, and launches BNB Chain tokens through DISTRICT9 or Flap modes. It is intended for users who explicitly want autonomous on-chain token deployment and understand wallet, gas, tax, and irreversible transaction risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet keys to deploy tokens and spend BNB on irreversible mainnet transactions. <br>
Mitigation: Run dry-run first, use a dedicated low-balance hot wallet, and enable live launches only after reviewing the configured chain, platform, and initial buy amount. <br>
Risk: The DISTRICT9 treasury and tax model affects launched tokens and downstream trading economics. <br>
Mitigation: Review and accept the documented DISTRICT9 and agent revenue split before deploying any token. <br>
Risk: Proof-of-concept scripts may be unsafe for live use without additional operator controls. <br>
Mitigation: Avoid running PoC scripts until embedded credentials are removed and live-transaction confirmation gates are added. <br>


## Reference(s): <br>
- [ClawHub DISTRICT9 skill page](https://clawhub.ai/pearl799/district9) <br>
- [Publisher profile](https://clawhub.ai/user/pearl799) <br>
- [DISTRICT9 homepage](https://www.district9.club) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Flap](https://flap.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, generated token metadata, and transaction status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, a BNB Chain wallet key, and an LLM API key; live mode can upload metadata and submit signed blockchain transactions.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
