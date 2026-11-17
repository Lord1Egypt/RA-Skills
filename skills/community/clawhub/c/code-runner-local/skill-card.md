## Description:

Run code snippets in 30+ programming languages including JavaScript, Python, TypeScript, Java, C, C++, Go, Rust, Ruby, PHP, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to execute snippets, test algorithms, verify outputs, and inspect syntax or runtime behavior across many local programming language runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary snippets run directly on the local host without enforced isolation.

Mitigation: Use the skill only in a contained environment with no sensitive files, credentials, or broad network access.

Risk: Executed code can access files, make network requests, run system commands, or modify environment variables.

Mitigation: Review snippets before execution and avoid running untrusted code in normal workspaces.

Risk: Language execution depends on locally installed interpreters and compilers.

Mitigation: Confirm required runtimes are installed and use command errors to guide setup or troubleshooting.

## Reference(s):

- [Supported Languages Reference](references/LANGUAGES.md)
- [Code Runner Local on ClawHub](https://clawhub.ai/panchenbo/skills/code-runner-local)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with command examples, stdout, stderr, and error explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution depends on local runtimes being installed; code execution uses a default 30-second timeout.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
