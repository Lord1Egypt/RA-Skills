## Description: <br>
Guides users in running Codex through acpx persistent sessions, prompt files, full-access mode, local dependency installs, shell-based writes, and validation for generated deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure acpx/Codex sessions for reliable file creation, local dependency setup, generated deliverables, and troubleshooting of quoting, file-write, and sandbox-boundary issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The playbook encourages full-access acpx sessions and shell or Python writes, which can broaden file-system or command-execution impact if used without boundaries. <br>
Mitigation: Set explicit allowed directories, decide whether full-access and network use are permitted, and require confirmation before shell/Python writes or copying generated files into final locations. <br>
Risk: Dependency installation guidance could modify the local environment or fail when network or package access is restricted. <br>
Mitigation: Prefer project-local virtual environments and avoid assuming global install rights or unrestricted network access. <br>
Risk: Generated deliverables can be incomplete or invalid if declared successful before inspection. <br>
Mitigation: Use the skill's validation checklist for file existence, parseable structure, expected counts, and a short report before final delivery. <br>


## Reference(s): <br>
- [PPT playbook for acpx + Codex](references/ppt-playbook.md) <br>
- [acpx troubleshooting notes](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; it does not execute commands, install dependencies, or write files by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
