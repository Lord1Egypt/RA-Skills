## Description: <br>
Trade tokens on Solana using the ClawDex CLI. Use when the user asks to swap tokens, check balances, get quotes, or manage a Solana trading wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoelCCodes](https://clawhub.ai/user/JoelCCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to check Solana wallet balances, obtain swap quotes, simulate swaps, and execute token trades through the ClawDex CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to operate a Solana trading wallet and execute real swaps through non-interactive commands. <br>
Mitigation: Use a dedicated low-balance wallet, simulate each swap first, set strict safety guardrails, and require explicit human confirmation before any real swap using `--yes`. <br>
Risk: The skill installs or relies on an unpinned external ClawDex CLI package. <br>
Mitigation: Verify and pin the CLI package before installation, and install only when the ClawDex CLI is trusted. <br>
Risk: Wallet keys, API keys, or trading details could be exposed in logs or transcripts. <br>
Mitigation: Avoid exposing wallet secrets and API keys in agent transcripts, shell logs, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JoelCCodes/clawdex-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes machine-parseable JSON output, simulation before execution, exit-code handling, and balance verification after swaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
