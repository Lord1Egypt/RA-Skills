## Description: <br>
Safely manage EVM treasury operations and native Hyperliquid trading for OpenClaw agents, including wallet balance checks, guarded token transfers, cross-chain USDC bridging, Hyperliquid deposits, destination gas top-ups, trading safety, and structured quoting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fiowind](https://clawhub.ai/user/fiowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and treasury operators use this skill to let OpenClaw agents quote, validate, and execute guarded EVM, Solana bridge-source, and Hyperliquid perpetual workflows with structured JSON responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds, sign transactions, and place trades when configured with wallet keys. <br>
Mitigation: Use a dedicated treasury wallet or limited hot wallet, keep large balances elsewhere, set strict allowlists and max single/daily limits, and keep DRY_RUN_DEFAULT enabled until reviewed. <br>
Risk: External swap, bridge, and approval flows can expose assets to unwanted routing, fees, or approvals. <br>
Mitigation: Review route quotes, fee and slippage details, and token approvals before real execution; use quote_operation and dryRun=true immediately before state-changing calls. <br>
Risk: Multi-stage bridge and Hyperliquid deposit flows can partially complete before an error is returned. <br>
Mitigation: Re-check source and destination balances after any partial execution, then re-run quote_operation with the remaining balance before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fiowind/crypto-treasury-ops) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON responses with CLI invocation examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing tools support dry-run and quote-first workflows; responses include request status, timestamps, data, warnings, or errors.] <br>

## Skill Version(s): <br>
0.1.7 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
