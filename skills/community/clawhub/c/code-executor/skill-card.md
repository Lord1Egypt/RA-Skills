## Description: <br>
Executes Python, JavaScript, Bash, TypeScript, and SQL code dynamically so an agent can create, run, and return code results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate and execute short scripts, run command-line tasks, perform calculations, transform data, prototype automations, and debug code in supported runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad code and shell execution powers, which can affect files, dependencies, and local runtime behavior. <br>
Mitigation: Use it only in a disposable or strongly enforced sandbox; review every generated script and shell command before execution. <br>
Risk: The security evidence says safety limits and activation scope are not clear enough for automatic trust. <br>
Mitigation: Independently verify sandboxing, filesystem permissions, network blocking, timeouts, dependency installation controls, and confirmation prompts before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miguelguerra200022-sudo/code-executor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated scripts, REPL-style interaction, dependency installation prompts, command output, and safety confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
