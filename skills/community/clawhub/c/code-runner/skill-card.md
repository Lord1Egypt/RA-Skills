## Description: <br>
Run code snippets in 30+ programming languages including JavaScript, Python, TypeScript, Java, C, C++, Go, Rust, Ruby, PHP, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[formulahendry](https://clawhub.ai/user/formulahendry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to execute snippets, test algorithms, verify output, run quick scripts, and check code behavior across interpreted and compiled languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local code snippets, which can access files, network, subprocesses, or environment variables depending on the code and runtime. <br>
Mitigation: Review snippets before execution and use a sandbox or disposable environment for untrusted code. <br>
Risk: Execution depends on local interpreters, compilers, and platform behavior, so unsupported or missing runtimes can fail. <br>
Mitigation: Confirm the required language runtime is installed and review stderr or timeout output before relying on results. <br>


## Reference(s): <br>
- [Supported Languages Reference](references/LANGUAGES.md) <br>
- [Code Runner on ClawHub](https://clawhub.ai/formulahendry/code-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command examples and execution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution uses local language runtimes and a default 30 second timeout.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
