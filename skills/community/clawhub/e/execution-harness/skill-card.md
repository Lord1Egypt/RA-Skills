## Description: <br>
Navigation hub for an agent execution reliability system that routes users to hook and script patterns for preventing premature stops, unsafe tool use, context loss, coordination conflicts, recovery failures, and missing verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and configure execution-reliability patterns for Claude Code agents, including persistent execution loops, tool governance, context memory, multi-agent coordination, error recovery, and quality verification. It is a navigation and guidance skill; concrete behavior is implemented by its bundled sub-skills and shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful local hook automation for Claude Code sessions. <br>
Mitigation: Review each shell script before enabling it, start with the minimal hook set, and expand only for workflows that need stronger execution controls. <br>
Risk: Cron-based tmux recovery can affect the wrong pane or resume a session at an unsafe prompt if scoped poorly. <br>
Mitigation: Use tmux recovery only with tightly scoped panes and keep the documented secondary prompt checks enabled before sending input. <br>
Risk: Handoff and working-memory files can expose sensitive project details if agents write secrets into shared state. <br>
Mitigation: Do not store secrets in handoff or working-memory files, and periodically delete or protect ~/.openclaw/shared-context. <br>
Risk: The security verdict is suspicious because the package requests broad local automation. <br>
Mitigation: Treat installation as a local automation grant, scan the release, and deploy only the sub-skills and hooks needed for the current project. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/execution-harness) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lanyasheng) <br>
- [Artifact README](artifact/README.md) <br>
- [Execution Harness Hub Skill](artifact/SKILL.md) <br>
- [Execution Loop Skill](artifact/execution-loop/SKILL.md) <br>
- [Tool Governance Skill](artifact/tool-governance/SKILL.md) <br>
- [Context Memory Skill](artifact/context-memory/SKILL.md) <br>
- [Error Recovery Skill](artifact/error-recovery/SKILL.md) <br>
- [Quality Verification Skill](artifact/quality-verification/SKILL.md) <br>
- [Multi-Agent Coordination Skill](artifact/multi-agent/SKILL.md) <br>
- [Harness Engineering Principles](artifact/principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or recommend local hook configuration and state files for Claude Code workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
