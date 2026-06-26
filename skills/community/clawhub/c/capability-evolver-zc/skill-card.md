## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze agent logs and history, select reusable GEP assets, and produce protocol-bound prompts or operations for repair, hardening, or controlled evolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous evolution can affect local code, repository state, background execution, updates, and external reporting. <br>
Mitigation: Run first in review mode, inspect configuration, and disable EVOLVE_BRIDGE, EVOLVER_AUTO_ISSUE, autoUpdate, A2A, and worker settings unless each capability is required. <br>
Risk: External integrations may contact EvoMap or GitHub and may use broad tokens if configured. <br>
Mitigation: Use least-privilege credentials, avoid broad GITHUB_TOKEN access unless release or issue automation is intended, and keep node identity values out of source files. <br>
Risk: Repository rollback and cleanup behavior can discard local changes when unsafe modes are enabled. <br>
Mitigation: Use a clean git workspace, keep backups or sync enabled, and prefer safer rollback settings such as stash mode in active workspaces. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/capability-evolver-zc) <br>
- [EvoMap](https://evomap.ai) <br>
- [EvoMap documentation](https://evomap.ai/wiki) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured text with inline JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write files or affect repository state when run with execution options; review configuration before use.] <br>

## Skill Version(s): <br>
1.27.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
