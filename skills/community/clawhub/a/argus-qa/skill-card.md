## Description: <br>
Argus provides incremental backend API and frontend browser testing with persistent memory, monitoring commits, enriching insufficient commit messages, and running targeted tests scoped to changed files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiansyao](https://clawhub.ai/user/tiansyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Argus to maintain persistent regression-test memory, generate backend and frontend tests from routes and commits, run targeted test suites, and produce health reports for changed code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Argus can persist repository-level automation through a Git post-commit hook. <br>
Mitigation: Review .git/hooks/post-commit after initialization and disable or remove the hook if commit-time automation is not desired. <br>
Risk: Argus can amend local commits while enriching insufficient commit messages. <br>
Mitigation: Require manual approval before any git commit --amend and avoid using amendment behavior on shared or already-pushed branches. <br>
Risk: Argus may install browser-testing dependencies and run local backend or frontend tests. <br>
Mitigation: Run it in a virtual environment or container with local test services and minimal test credentials. <br>


## Reference(s): <br>
- [Argus on ClawHub](https://clawhub.ai/tiansyao/argus-qa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Python test code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update .argus state, pytest and Playwright tests, reports, and a Git post-commit hook.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
