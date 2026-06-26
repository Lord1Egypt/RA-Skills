## Description: <br>
Reviews ExUnit test code for proper patterns, boundary mocking with Mox, and test adapter usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Elixir ExUnit test files and test helper configuration for async safety, mock boundaries, test adapters, and database isolation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings can be misleading if they are made without concrete file evidence or without applying the documented false-positive checks. <br>
Mitigation: Require each finding to cite FILE:LINE evidence and pass the skill's stated gates before relying on it. <br>
Risk: The security guidance notes a Swoosh adapter wording mismatch that may confuse email test configuration. <br>
Mitigation: Confirm the correct Swoosh test adapter naming and project configuration before applying email testing guidance. <br>
Risk: The skill references a separate review-verification protocol that is not included in this artifact. <br>
Mitigation: Inspect that referenced protocol before treating the cross-protocol verification gate as satisfied. <br>


## Reference(s): <br>
- [ExUnit Patterns](references/exunit-patterns.md) <br>
- [Mox Boundaries](references/mox-boundaries.md) <br>
- [Test Adapters](references/test-adapters.md) <br>
- [Integration Tests](references/integration-tests.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to include FILE:LINE evidence after the skill's review gates.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
