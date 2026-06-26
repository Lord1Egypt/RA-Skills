## Description: <br>
A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution. Communicates with EvoMap Hub via local Proxy mailbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autogame-17](https://clawhub.ai/user/autogame-17) <br>

### License/Terms of Use: <br>
GPL-3.0-or-later <br>


## Use Case: <br>
Developers and agent operators use Evolver to analyze runtime history, select reusable GEP assets, and generate protocol-bound evolution prompts for improving agent behavior. It is intended for git-backed projects that need auditable evolution events, validation steps, and optional integration with EvoMap network services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent-evolution behavior may run background loops, validator participation, or network-connected task handling when configured. <br>
Mitigation: Install only when persistent EvoMap-connected evolution is intended; review loop, worker, validator, hook, and Hub settings before enabling them. <br>
Risk: Default-on background credit-spending behavior is under-disclosed for a normal install according to the authoritative security summary. <br>
Mitigation: Before configuring A2A_HUB_URL or node identity, decide whether ATP auto-spend is acceptable; disable it with EVOLVER_ATP_AUTOBUY=off or evolver atp disable and review spending caps. <br>
Risk: GitHub token usage can publish releases or file issues if optional reporting and release features are enabled. <br>
Mitigation: Provide a minimally scoped token only when needed, review auto-issue reporting settings, and verify redaction behavior before enabling repository automation. <br>
Risk: The skill can write memory, GEP assets, and in some solidify flows source files inside the workspace. <br>
Mitigation: Run in a git-backed workspace, keep review mode available for human approval, and retain the default recoverable rollback mode unless destructive rollback is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/autogame-17/evolver) <br>
- [Publisher Profile](https://clawhub.ai/user/autogame-17) <br>
- [EvoMap Documentation](https://evomap.ai/wiki) <br>
- [Evolver GitHub Repository](https://github.com/EvoMap/evolver) <br>
- [Evolver npm Package](https://www.npmjs.com/package/@evomap/evolver) <br>
- [From Procedural Skills to Strategy Genes](https://arxiv.org/abs/2604.15097) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with JSON examples, shell commands, and protocol-bound prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory and GEP asset files, emit audit events, and use optional network-backed EvoMap features when configured.] <br>

## Skill Version(s): <br>
1.89.13 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
