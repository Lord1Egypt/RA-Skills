## Description: <br>
Automatically analyzes and improves code for performance, readability, security, and best practices in JavaScript, TypeScript, Python, Go, Rust, and Java. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxm1618](https://clawhub.ai/user/fxm1618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to ask an agent to analyze code files and propose or apply performance, readability, security, and best-practice improvements across supported languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can analyze and potentially change source code, including production or security-sensitive code. <br>
Mitigation: Review before/after output and diffs carefully before accepting changes, especially for authentication, cryptographic, or large codebases. <br>
Risk: Optimization suggestions may alter behavior while improving readability, performance, or style. <br>
Mitigation: Run the project's normal tests and code review process before merging generated changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fxm1618/ai-code-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with code snippets and before/after comparisons] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file edits or suggested diffs when the agent applies optimizations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
