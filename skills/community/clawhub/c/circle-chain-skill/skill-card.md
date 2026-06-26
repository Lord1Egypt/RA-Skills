## Description: <br>
JavaScript SDK and CLI guidance for Circle Chain, covering @lidh04/circle-chain-sdk user auth, wallet, block, miner, transfers, contacts, HTTP configuration, and the global circle CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidh04](https://clawhub.ai/user/lidh04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating Circle Chain from Node.js or browser code, working in js-circle-chain-sdk, using the circle CLI, configuring HTTP settings, or implementing local mining and wallet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports wallet and transfer workflows where account credentials and pay passwords may be handled. <br>
Mitigation: Treat account credentials and pay passwords as sensitive, and review commands before execution. <br>
Risk: The SDK may perform a Node.js-only GeoIP request to ipwho.is when resolving HTTP gateway settings. <br>
Mitigation: Set an explicit host or use CIRCLE_SKIP_GEO=1 when third-party GeoIP requests are not acceptable. <br>
Risk: Installing the global circle CLI adds a command-line tool for account, wallet, mining, and transfer operations. <br>
Mitigation: Install only from the trusted @lidh04/circle-chain-sdk package and review CLI actions before using them with real accounts. <br>


## Reference(s): <br>
- [Circle Chain Skill on ClawHub](https://clawhub.ai/lidh04/skills/circle-chain) <br>
- [ipwho.is GeoIP service](https://ipwho.is/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK usage patterns, CLI commands, HTTP configuration notes, and security cautions for wallet and transfer workflows.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
