## Description: <br>
Manage ATX on BSC with wallet creation, price and balance queries, PancakeSwap V3 swaps, liquidity operations, LP positions and holdings, and BNB/ERC20 transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentswapx](https://clawhub.ai/user/agentswapx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ATXSwap to manage ATX wallets and perform BSC workflows, including live balance queries, ATX/USDT swaps, PancakeSwap V3 liquidity operations, and token transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real funds through wallet, swap, transfer, and liquidity commands. <br>
Mitigation: Use a low-balance dedicated wallet, run live previews first, and require explicit confirmation before any write action. <br>
Risk: Passing wallet passwords on the command line can expose sensitive credentials through shell history or process listings. <br>
Mitigation: Prefer interactive or secure local workflows and never print passwords, private keys, or decrypted wallet material in chat. <br>
Risk: Registry bypass instructions can lead users to ignore meaningful security warnings. <br>
Mitigation: Review the source and dependency trust path before installation, and do not treat the package's force-install path as proof that warnings are harmless. <br>
Risk: Repeated or ambiguous transfer submissions can duplicate a real asset transfer. <br>
Mitigation: Treat each asset/from/to/amount tuple as a single transfer intent, check chain or wallet state after ambiguous submissions, and do not retry blindly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentswapx/atxswap) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/agentswapx) <br>
- [Project homepage](https://github.com/agentswapx/skills/tree/main/atxswap) <br>
- [ATXSwap SDK on npm](https://www.npmjs.com/package/atxswap-sdk) <br>
- [ATXSwap SDK source](https://github.com/agentswapx/atxswap-sdk) <br>
- [ATXSwap team documentation](https://docs.atxswap.com/guide/team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands and write commands are separated by preview and confirmation flows; wallet, swap, liquidity, and transfer scripts emit JSON.] <br>

## Skill Version(s): <br>
0.0.31 (source: frontmatter, package.json, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
