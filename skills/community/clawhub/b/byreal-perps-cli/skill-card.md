## Description: <br>
Byreal Perps CLI helps an agent use the byreal-perps-cli command line tool for Hyperliquid perpetual futures account setup, orders, positions, leverage, trade history, market signals, and technical analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggg223399](https://clawhub.ai/user/ggg223399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Hyperliquid perpetual futures CLI workflows, including account initialization, read-only account checks, market and limit orders, position management, leverage updates, and market signal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to execute high-impact leveraged trading commands, including placing orders, changing leverage, canceling orders, and closing positions. <br>
Mitigation: Use testnet or a tightly limited agent wallet first, and require explicit user confirmation before any command that places orders, changes leverage, cancels orders, or closes positions. <br>
Risk: An agent-accessible trading CLI may expose locally configured wallet capabilities if credentials are initialized for a live account. <br>
Mitigation: Initialize credentials only through the interactive CLI flow, never paste private keys into chat, and prefer narrowly funded or restricted wallets for agent use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ggg223399/byreal-perps-cli) <br>
- [Project homepage from ClawHub metadata](https://github.com/byreal-git/byreal-perps-cli) <br>
- [Hyperliquid API info endpoint](https://api.hyperliquid.xyz/info) <br>
- [Hyperliquid testnet API info endpoint](https://api.hyperliquid-testnet.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides CLI use and command selection; trading commands can change positions, orders, leverage, and account exposure.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
