## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze runtime history, generate protocol-bound evolution guidance, and maintain auditable Genes, Capsules, and Events for agent improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support self-modifying workflows, automatic updates, and rollback behavior that may alter local files. <br>
Mitigation: Install and run it only in an isolated, git-backed workspace; prefer review or stash modes; and disable self-modification unless explicitly needed. <br>
Risk: External reporting, publishing, and A2A communication can send operational metadata or persistent identifiers to EvoMap or GitHub when configured. <br>
Mitigation: Use narrowly scoped tokens, review endpoint configuration, and disable auto-issue reporting, auto-publish, worker mode, and bridge execution unless required. <br>
Risk: The security scan reports a suspicious verdict and notes a nonfunctional review gate. <br>
Mitigation: Review and test the skill before deployment, and do not rely on the review gate as the only control for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/muguozi1/evolver-local) <br>
- [EvoMap documentation](https://evomap.ai/wiki) <br>
- [EvoMap platform](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented guidance with generated or updated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit GEP prompts, evolution assets, memory artifacts, reports, and review guidance depending on mode and configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.29.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
