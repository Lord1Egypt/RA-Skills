## Description: <br>
Run code snippets in 30+ programming languages including JavaScript, Python, TypeScript, Java, C, C++, Go, Rust, Ruby, PHP, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to execute short code snippets, test algorithms, verify behavior, and inspect stdout or error output across installed local language runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executed snippets have the same local access as the user running the agent. <br>
Mitigation: Review snippets before execution and use a disposable container or sandbox for code that might read files, use the network, run shell commands, or change the system. <br>
Risk: Untrusted code can modify files, expose local data, or invoke system commands through supported runtimes. <br>
Mitigation: Run only trusted snippets in the normal workspace and isolate unknown code from sensitive files, credentials, and network access. <br>
Risk: Language support depends on interpreters and compilers installed on the local machine. <br>
Mitigation: Confirm the required runtime is installed and in PATH before relying on the output for user-facing answers. <br>


## Reference(s): <br>
- [Supported Languages Reference](references/LANGUAGES.md) <br>
- [Code Runner Local on ClawHub](https://clawhub.ai/panchenbo/code-runner-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and captured stdout or stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs submitted code locally with a default 30 second timeout; available languages depend on installed interpreters and compilers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
