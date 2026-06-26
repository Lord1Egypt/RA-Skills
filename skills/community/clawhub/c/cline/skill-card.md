## Description: <br>
Run the local Cline CLI to plan, build, code, and return the output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate coding, scaffolding, debugging, and multistep planning tasks to an installed local Cline CLI and receive the resulting output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Cline CLI can propose or make file changes in the active project. <br>
Mitigation: Run it only in intended project directories and review generated file changes before keeping them. <br>
Risk: Prompts or command output could expose sensitive information if secrets are pasted into the task. <br>
Mitigation: Keep prompts specific and do not include secrets or credentials. <br>
Risk: Behavior depends on the local cline executable available on PATH. <br>
Mitigation: Install only if you already trust the local Cline CLI and verify the command being invoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elathoxu-crypto/cline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with command output and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local cline command on PATH; review generated file changes before keeping them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
