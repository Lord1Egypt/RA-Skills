## Description: <br>
A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution. Communicates with EvoMap Hub via local Proxy mailbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autogame-17](https://clawhub.ai/user/autogame-17) <br>

### License/Terms of Use: <br>
GPL-3.0-or-later <br>


## Use Case: <br>
Developers and teams maintaining AI agents use Evolver to analyze runtime history, select protocol-bound Genes or Capsules, and produce auditable evolution guidance for repair, hardening, and optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-running self-evolution, proxy, and hook behavior can affect agent runtime state and model traffic. <br>
Mitigation: Install only where that posture is intended, start in review mode, and disable proxy auto-injection, worker, validator, and Hub features unless they are needed. <br>
Risk: Remote validation, worker flows, and issue reporting can interact with external services when configured. <br>
Mitigation: Keep optional Hub and GitHub settings unset unless required, review outbound endpoints, and avoid providing broad-scope tokens. <br>
Risk: Self-modification and rollback settings can affect source files if explicitly enabled or misconfigured. <br>
Mitigation: Leave EVOLVE_ALLOW_SELF_MODIFY set to false, keep the default stash rollback mode, and review proposed solidification behavior before allowing changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/autogame-17/skills/evolver) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [GEP Protocol Documentation](https://evomap.ai/wiki) <br>
- [From Procedural Skills to Strategy Genes](https://arxiv.org/abs/2604.15097) <br>
- [Skill Integration Documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain-text guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory and GEP event files when run; proxy, Hub, worker, validator, and issue-reporting features depend on configuration.] <br>

## Skill Version(s): <br>
1.89.20 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
