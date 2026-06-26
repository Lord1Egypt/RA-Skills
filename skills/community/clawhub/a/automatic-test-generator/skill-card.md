## Description: <br>
Automatically generate unit tests from functions with comprehensive coverage and edge cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelatamuk](https://clawhub.ai/user/michaelatamuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate unit test suites for existing functions, classes, and modules across common testing frameworks. It is most useful for improving coverage, creating edge-case tests, and building reviewable starting points for test files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works by inspecting source code, which can expose unrelated private code or secrets if the agent is given broad access. <br>
Mitigation: Point the agent at specific files or directories and avoid sharing secrets, credentials, or unrelated private configuration. <br>
Risk: Generated tests can contain incorrect assertions, incomplete mocks, or assumptions that do not match the intended business behavior. <br>
Mitigation: Review and edit generated tests before committing them, running them in CI, or using them against real services. <br>


## Reference(s): <br>
- [Automatic Test Generator on ClawHub](https://clawhub.ai/michaelatamuk/automatic-test-generator) <br>
- [Jest Documentation](https://jestjs.io) <br>
- [Vitest Documentation](https://vitest.dev) <br>
- [Pytest Documentation](https://docs.pytest.org) <br>
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated test code, framework-specific snippets, and optional shell or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated tests are starting points and should be reviewed, customized, and run in the target project before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
