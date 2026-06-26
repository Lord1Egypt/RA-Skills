## Description: <br>
OpenClaw plugin development assistant that outputs runnable plugin skeletons, install commands, and debugging steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boleyn](https://clawhub.ai/user/boleyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to decide whether an OpenClaw extension should be a Skill or Plugin, generate a minimal runnable plugin scaffold, and get install, debug, publish, and rollback commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shell, install, publish, or rollback commands can change local projects or release state if run without review. <br>
Mitigation: Review commands before execution, run them only in the intended project directory, and use version control or backups before applying changes. <br>
Risk: Generated plugin scaffolds and configuration may not match every OpenClaw project or release workflow. <br>
Mitigation: Review generated files, test locally, and verify publish settings before releasing a plugin. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boleyn/crayfish-plugin-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include a recommended solution type, directory structure, key files, install commands, debug commands, publish commands, rollback commands, and risk troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
