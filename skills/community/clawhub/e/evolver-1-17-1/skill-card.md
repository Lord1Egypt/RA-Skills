## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent teams use this skill to inspect runtime history, produce protocol-bound evolution prompts, record reusable genes and capsules, and guide reviewable repairs or hardening of agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate as an autonomous agent-evolution daemon with access to local agent history and workspace state. <br>
Mitigation: Install only when that behavior is intended, run in review or dry-run mode first, and keep a clean git working tree before applying changes. <br>
Risk: External hub features, auto-update, auto-publish, loop mode, and rollback behavior can broaden the operational impact of a run. <br>
Mitigation: Disable those features unless they are explicitly required and review their configuration before running the skill. <br>
Risk: VirusTotal was pending and was not used as the basis for the Review verdict. <br>
Mitigation: Treat the clawscan verdict and guidance as the authoritative review source until additional malware scanning is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/evolver-1-17-1) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local agent history and workspace state; review or dry-run modes are recommended before applying suggested changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
