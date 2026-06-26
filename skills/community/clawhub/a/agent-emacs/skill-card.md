## Description: <br>
Agent Emacs provides a unified persistent text-based Emacs environment for AI agents that need to maintain state across sessions, perform structural code editing, or manage remote nodes with TRAMP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PiTZE](https://clawhub.ai/user/PiTZE) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run AI coding agents inside a persistent Emacs daemon so they can keep buffers and workspace state across turns, perform structural edits through Emacs Lisp, and manage remote files with TRAMP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad local and remote control through a persistent Emacs daemon and TRAMP sessions without clear safety boundaries. <br>
Mitigation: Install only in a trusted or sandboxed workspace, restrict SSH access to approved least-privilege hosts, require explicit user approval for remote commands, and know how to stop the daemon and clear persistent buffers or TRAMP sessions. <br>
Risk: The bootstrap script expects an agent-init.el dependency that is not present in the artifact evidence. <br>
Mitigation: Review scripts/bootstrap.sh before execution and fix or verify the missing dependency before using the skill. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Usage Guide: Emacs-Agent Interaction](references/usage.md) <br>
- [Advanced Agent Workflows in Emacs](references/agent-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and Emacs Lisp examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guidance for persistent buffers, TRAMP remote access, Magit workflows, and daemon bootstrap commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
