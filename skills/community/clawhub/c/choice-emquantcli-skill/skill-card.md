## Description: <br>
Guides agents to install and use emq-cli for authentication, market data queries, portfolio creation and order commands, quota checks, raw command passthrough, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Greapi](https://clawhub.ai/user/Greapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent produce exact emq-cli commands for setup, authentication, market data lookup, portfolio operations, quota checks, raw command passthrough, and common troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated portfolio and order commands can change account or financial state. <br>
Mitigation: Use demo or least-privilege credentials where possible, start with read-only market and quota commands, and require explicit approval before executing portfolio or order commands. <br>
Risk: Raw passthrough commands can send unintended EMQ parameters. <br>
Mitigation: Require the agent to show the exact raw command and parameters before execution, and approve only commands that match the intended account, portfolio, symbol, date, and action. <br>
Risk: The skill depends on the external emq-cli package and authenticated EMQ access. <br>
Mitigation: Install only when the package and EMQ account are trusted for the target environment. <br>


## Reference(s): <br>
- [EMQ CLI Command Recipes](references/command-recipes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Greapi/choice-emquantcli-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may include authentication, portfolio, order, quota, market data, and raw passthrough operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
