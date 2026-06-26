## Description: <br>
Complete toolkit for building AI agents, including agent-builder, agent-browser, agent-wallet, agent-development, and agent-docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cahdieng](https://clawhub.ai/user/cahdieng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this toolkit to design OpenClaw agents, generate workspace files, automate browser workflows, manage EVM-wallet workflows, and produce AI-readable documentation. It is intended for agent-development workflows that may involve external services, browser actions, and wallet operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit teaches high-impact wallet, browser, and agent-permission workflows with under-scoped safeguards. <br>
Mitigation: Require human confirmation for every transaction, swap, contract call, refund, post, and form submission before execution. <br>
Risk: Wallet workflows can involve purchases, crypto transfers, contract calls, and sensitive credentials. <br>
Mitigation: Set wallet policies before funding any wallet, use testnets or sandbox accounts first, and keep tokens least-privilege. <br>
Risk: Browser automation and external publishing workflows can act on live websites or accounts. <br>
Mitigation: Avoid wildcard WebFetch permissions, constrain domains, and review proposed browser or publishing actions before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cahdieng/agent-dev-toolkit-cahdieng) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cahdieng) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Agent Browser safety reference](dependencies/agent-browser-core/references/agent-browser-safety.md) <br>
- [Agent Browser command map](dependencies/agent-browser-core/references/agent-browser-command-map.md) <br>
- [OpenClaw workspace reference](dependencies/agent-builder/references/openclaw-workspace.md) <br>
- [Agent builder templates](dependencies/agent-builder/references/templates.md) <br>
- [Agent documentation advanced patterns](dependencies/agent-docs/references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, workspace file templates, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm according to server-parsed metadata; includes workflows for browser automation, external publishing, and wallet operations that require human review before high-impact actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
