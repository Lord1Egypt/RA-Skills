## Description: <br>
Creates comprehensive test suites for Move contracts with a 100% coverage requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and review Aptos Move contract test suites covering happy paths, access control, input validation, edge cases, and coverage verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic testing prompts may activate the skill outside Aptos Move work. <br>
Mitigation: Confirm the task involves Aptos Move contracts before applying the templates, commands, or coverage expectations. <br>
Risk: A 100% line coverage target does not by itself prove contract security or business-logic correctness. <br>
Mitigation: Use coverage as quality guidance and pair the generated tests with code review, security review, and project-specific threat analysis. <br>
Risk: Generated examples may not match a project's exact module APIs, abort codes, or accessor functions. <br>
Mitigation: Run `aptos move test --coverage`, inspect failures and uncovered paths, and adapt tests to the contract's actual public API and validation order. <br>


## Reference(s): <br>
- [Aptos Move unit testing documentation](https://aptos.dev/build/smart-contracts/book/unit-testing) <br>
- [ClawHub skill page](https://clawhub.ai/iskysun96/generate-tests) <br>
- [Publisher profile](https://clawhub.ai/user/iskysun96) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Move code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on Aptos Move unit tests, expected-failure cases, and coverage verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
