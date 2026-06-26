## Description: <br>
Creates V5 tokens on BSC, performs USDT token buys and sells, and runs automated market-making and volume workflows through BNB Chain MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flap-builder](https://clawhub.ai/user/flap-builder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and token operators use this skill to create BSC V5 tokens, buy or sell tokens with USDT, and run market-making workflows from an agent connected to BNB Chain MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad financial authority to an agent for live token creation, approvals, trading, worker funding, and volume workflows. <br>
Mitigation: Use a fresh low-balance wallet, confirm every address and amount before execution, and set explicit bot rounds and gas budgets. <br>
Risk: The market-making workflow may use large or unlimited token approvals. <br>
Mitigation: Avoid unlimited approvals where possible, revoke allowances after use, and remove allowed callers when the workflow is finished. <br>
Risk: Generated worker key files can expose funds if retained or shared. <br>
Mitigation: Protect generated worker files during use and delete them after funds are collected. <br>
Risk: Automated volume-generation may be unlawful or unacceptable for some tokens or venues. <br>
Mitigation: Use the 做市/刷量 workflow only after confirming it is lawful and acceptable for the token and venue involved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flap-builder/flap-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/flap-builder) <br>
- [BNB Chain Skills Documentation](https://docs.bnbchain.org/showcase/mcp/skills/) <br>
- [Flap Token Launcher Portal](https://docs.flap.sh/flap/developers/token-launcher-developers/launch-token-through-portal) <br>
- [Flap Deployed Contract Addresses](https://docs.flap.sh/flap/developers/token-launcher-developers/deployed-contract-addresses) <br>
- [Contract ABI Reference](references/contract-abi.md) <br>
- [Project Homepage](https://github.com/flap-builder/flap-skills) <br>
- [Project Support](https://github.com/flap-builder/flap-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, contract-call parameters, and generated local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local worker-wallet JSON files and launch long-running market-making scripts.] <br>

## Skill Version(s): <br>
1.8.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
