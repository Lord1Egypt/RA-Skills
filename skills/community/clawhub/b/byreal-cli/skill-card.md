## Description: <br>
Byreal Cli helps agents use the Byreal Solana DEX CLI to query pools, tokens, TVL, APR, k-line charts, farmer rankings, launchpad projects, and DeFi position statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggg223399](https://clawhub.ai/user/ggg223399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to discover and invoke Byreal CLI commands for Solana DEX analytics. The skill is also used to keep wallet setup and confirmed write actions inside the CLI's own interactive flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as analytics-focused, but the documented CLI can perform wallet-backed write actions that may affect funds. <br>
Mitigation: Use read-only analytics by default; for write actions, run dry-run first, inspect the output, and require explicit user approval before using --confirm. <br>
Risk: Wallet setup could expose sensitive credentials if handled through chat. <br>
Mitigation: Do not ask users to paste private keys; direct users to the interactive byreal-cli setup flow. <br>
Risk: The CLI self-update path may introduce unreviewed behavior in sensitive environments. <br>
Mitigation: Avoid self-update in sensitive environments unless the target release has been reviewed or is otherwise trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ggg223399/byreal-cli) <br>
- [Byreal CLI Homepage](https://github.com/byreal-git/byreal-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/ggg223399) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to CLI-rendered tables, charts, and JSON output from byreal-cli.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
