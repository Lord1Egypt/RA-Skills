## Description: <br>
Scaffolds a runnable RustChain agent with an Ed25519 RTC wallet, agent code, MCP wiring, node checks, and First-Light bounty guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create a local RustChain starter project with wallet, runnable agent script, MCP configuration, and next-step guidance for funding and use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated wallet.json contains a real private key. <br>
Mitigation: Store it securely, keep it out of version control, and back it up before relying on the generated wallet. <br>
Risk: The generated MCP configuration gives rustchain-mcp access to the wallet path. <br>
Mitigation: Enable the MCP configuration only in trusted editor projects where that wallet access is intended. <br>
Risk: Using --register performs a network write. <br>
Mitigation: Use --register only when ready to register a Beacon identity, and use --node to target an intended testnet or node. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottcjn/create-rustchain-agent) <br>
- [RustChain](https://rustchain.org) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, markdown, guidance] <br>
**Output Format:** [Generated project files and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates wallet.json, agent.py, .mcp.json, README.md, and .gitignore; network writes occur only when --register is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
