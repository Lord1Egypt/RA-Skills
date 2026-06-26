## Description: <br>
A skill to set up and operate a Dogecoin Core full node with RPC access, blockchain tools, and optional tipping functionality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GreatApe42069](https://clawhub.ai/user/GreatApe42069) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and node operators use this skill to install, configure, monitor, and operate a local Dogecoin Core node through CLI/RPC commands, including wallet lookups, transaction checks, price lookup, health checks, and optional tipping records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes wallet-spending commands that can transfer DOGE if invoked accidentally or after prompt manipulation. <br>
Mitigation: Use a dedicated low-balance Dogecoin wallet and require separate manual confirmation of recipient address, amount, and wallet context before allowing `/dogecoin-node send`. <br>
Risk: Dogecoin RPC access can control local wallet and node operations if exposed beyond the intended local host. <br>
Mitigation: Keep RPC bound to 127.0.0.1, use strong RPC credentials, and do not expose Dogecoin Core RPC to agents or users that do not need wallet control. <br>
Risk: The release requires installing and running Dogecoin Core binaries and command-line tooling on the host. <br>
Mitigation: Independently verify the Dogecoin Core download before installation and review the generated shell commands before execution. <br>


## Reference(s): <br>
- [ClawHub Dogecoin Node release page](https://clawhub.ai/GreatApe42069/dogecoin-node) <br>
- [Dogecoin Core v1.14.9 release archive](https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz) <br>
- [CoinGecko Dogecoin price API](https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd) <br>
- [Dogecoin Node Skill Heartbeat](artifact/HEARTBEAT.md) <br>
- [Dogecoin RPC Command Cheat Sheet](artifact/RPC_CHEATSHEET.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Dogecoin Core CLI/RPC commands, OpenClaw skill commands, configuration snippets, health-check scripting, and optional SQLite tipping code.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
