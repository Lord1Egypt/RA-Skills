## Description: <br>
Orchestrates early token launch detection, on-chain risk analysis, social signal verification, and guarded swap execution on Solana and Base chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
DeFi operators and agent users use this skill to evaluate early token-launch opportunities, combine on-chain and social checks, and decide whether to observe, paper trade, or execute bounded entries under explicit guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real funds through wallet-backed trading routes. <br>
Mitigation: Prefer observe or paper mode first, use a dedicated low-balance wallet or constrained vault, and require manual confirmation for live swaps. <br>
Risk: The skill recommends broad upstream skill updates, which can change trading behavior. <br>
Mitigation: Pin or inspect upstream trading skills before use and avoid update-all workflows unless every changed skill will be reviewed. <br>
Risk: Automated token-launch workflows can act on incomplete or misleading market signals. <br>
Mitigation: Keep hard position and slippage limits, require both security and sentiment gates to pass, and fail closed when evidence is ambiguous. <br>


## Reference(s): <br>
- [Defi Sniper ClawHub page](https://clawhub.ai/h4gen/defi-sniper) <br>
- [ClawHub homepage](https://clawhub.ai) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured decision sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces detection, on-chain risk, social signal, execution decision, and audit trail sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
