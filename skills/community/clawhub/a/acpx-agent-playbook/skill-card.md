## Description: <br>
Practical playbook for running agents through acpx in persistent sessions for reliable file creation, local installs, shell-based writes, structured deliverables, validation, permission troubleshooting, and multi-step coding work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and run acpx-based agent delivery workflows that need persistent sessions, prompt files, explicit validation, reliable file output, and troubleshooting across Codex, Claude, Gemini, OpenCode, Pi, or other ACP-compatible agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using full-access session mode can broaden an agent's ability to edit files or use networked tooling within the session. <br>
Mitigation: Use read-only or auto modes for inspection, reserve full-access for trusted delivery tasks, and validate outputs before accepting changes. <br>
Risk: Prompt files, reports, and temporary artifacts may retain sensitive task details. <br>
Mitigation: Avoid placing secrets in persistent prompt files and clean up temporary /tmp artifacts when they may contain sensitive content. <br>
Risk: Dependency installation guidance could affect the host environment if global installs are used unnecessarily. <br>
Mitigation: Prefer project-local virtual environments and use system-level installs only when explicitly intended and permitted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spyfree/acpx-agent-playbook) <br>
- [PPT playbook for acpx agents](references/ppt-playbook.md) <br>
- [acpx troubleshooting notes](references/troubleshooting.md) <br>
- [provider and agent compatibility notes](references/provider-compat.md) <br>
- [agent matrix](references/agent-matrix.md) <br>
- [migration notes](references/migration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational guidance for acpx session setup, permission posture, artifact generation, validation, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
