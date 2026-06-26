## Description: <br>
Complete toolkit for building AI agents. Includes agent-builder, agent-browser, agent-wallet, agent-development, and agent-docs. Build, automate, and monetize AI agents faster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobem0706](https://clawhub.ai/user/tobem0706) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this toolkit to create OpenClaw and Claude Code agents, document their behavior, automate browser workflows, and add wallet-enabled transaction flows under user-defined controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-enabled workflows can initiate transfers, swaps, or arbitrary EVM contract calls. <br>
Mitigation: Use testnets or sandbox funds first, claim the wallet and configure spending policies before funding it, and require human approval for transfers, swaps, and contract calls. <br>
Risk: Broad WebFetch, Write/Edit, and Bash allowlists can give an agent more access than a specific workflow requires. <br>
Mitigation: Review tool permissions before installation and keep only the permissions needed for the intended agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobem0706/agent-dev-toolkit) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Agent Browser overview](artifact/dependencies/agent-browser-core/references/agent-browser-overview.md) <br>
- [Agent Browser safety](artifact/dependencies/agent-browser-core/references/agent-browser-safety.md) <br>
- [Agent Builder workspace reference](artifact/dependencies/agent-builder/references/openclaw-workspace.md) <br>
- [Agent Builder templates](artifact/dependencies/agent-builder/references/templates.md) <br>
- [Agent Docs advanced patterns](artifact/dependencies/agent-docs/references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated agent workspace file content, browser automation command sequences, wallet API command examples, documentation structure, and operational guardrails.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
