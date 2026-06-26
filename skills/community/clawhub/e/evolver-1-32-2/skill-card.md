## Description: <br>
A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pppig1357](https://clawhub.ai/user/pppig1357) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect runtime history, extract evolution signals, and produce protocol-constrained prompts or assets that guide agent repair and improvement. It is suited to teams that need auditable evolution traces and human-reviewable changes rather than free-form live patching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run as a high-authority self-evolving component with shell, network, and write access. <br>
Mitigation: Run in review mode for sensitive environments, keep self-modification disabled unless explicitly needed, and review generated changes before solidifying them. <br>
Risk: Remote task intake and hub communication may affect agent behavior or disclose operational signals. <br>
Mitigation: Review EvoMap hub and task settings, use only intended A2A endpoints, and keep node credentials scoped and protected. <br>
Risk: GitHub issue reporting and release actions can use sensitive credentials and create outbound reports. <br>
Mitigation: Keep EVOLVER_AUTO_ISSUE disabled unless approved, avoid broad GitHub tokens, and use least-privilege credentials. <br>
Risk: Persistent node identity is stored under ~/.evomap. <br>
Mitigation: Treat the local node identity as persistent operational state and remove or rotate it when decommissioning the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pppig1357/evolver-1-32-2) <br>
- [EvoMap](https://evomap.ai) <br>
- [EvoMap Wiki](https://evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell commands, JSON-like evolution assets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local evolution assets, memory files, and solidified source changes when configured to do so.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata); artifact package 1.32.2 (source: package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
