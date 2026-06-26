## Description: <br>
Install and apply ClawJection bundles when a user asks to install a ClawJection, run a ClawJection, or configure an OpenClaw instance from a ClawJection repo, archive, or local bundle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmadeleidev](https://clawhub.ai/user/nmadeleidev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or run ClawJection bundles that configure a local OpenClaw instance from a Git repository, archive, zip file, or local directory. The agent follows the bundle manifest, runs the declared entrypoint, reads the structured result, and performs ordered follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded or local ClawJection bundles can run code and alter an OpenClaw setup. <br>
Mitigation: Use trusted sources, inspect the manifest and entrypoint, prefer pinned commits or verified archives, and back up OpenClaw configuration before applying a bundle. <br>
Risk: Bundles may request auth setup, command execution, follow-up actions, or overwrites of core files. <br>
Mitigation: Require explicit user approval before auth setup, command execution, follow-up actions, or overwrites of core OpenClaw files. <br>
Risk: Secrets could be written into workspace files during bundle execution. <br>
Mitigation: Keep secrets out of workspace files unless the bundle explicitly requires that behavior and the user agrees. <br>


## Reference(s): <br>
- [ClawJection on ClawHub](https://clawhub.ai/nmadeleidev/clawjection) <br>
- [ClawJection standard](standard/v1.md) <br>
- [ClawJection manifest schema](schemas/clawjection.schema.json) <br>
- [ClawJection result schema](schemas/result.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to JSON manifests or result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ordered follow-up actions returned by a ClawJection bundle.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
