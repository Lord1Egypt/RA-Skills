## Description: <br>
Helps agents simplify, polish, and declutter code while preserving behavior and verifying the resulting changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide cautious code cleanup, refactoring, dead-code removal, and readability improvements without changing public APIs, side effects, or error behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide code mutations, so broad or ambiguous scope could produce unintended behavior changes. <br>
Mitigation: Give narrow scope, review the resulting diff, and run the relevant tests and type checks before relying on the changes. <br>
Risk: Simplification can remove code that encodes domain intent when context or behavior parity is unclear. <br>
Mitigation: Inspect imports, dependents, and existing tests first, and stop when behavior parity cannot be verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-simplifying-code) <br>
- [Skill specification](artifact/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, markdown, shell commands] <br>
**Output Format:** [Markdown with code edits, verification notes, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports scope touched, key simplifications, verification performed, and residual risks.] <br>

## Skill Version(s): <br>
4.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
