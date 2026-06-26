## Description: <br>
Use when implementing new frontend behavior, fixing bugs, or refactoring logic where tests can describe the expected behavior first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend developers and coding agents use this skill to follow a test-first workflow for new behavior, bug fixes, and refactors across components, hooks, utilities, API clients, route guards, and user workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to change tests and source code or suggest test commands. <br>
Mitigation: Review proposed diffs and commands before applying them, and run the relevant project test suite after changes. <br>
Risk: The skill may recommend introducing minimal test infrastructure when a project has none. <br>
Mitigation: Confirm new dependencies, tools, or configuration changes with the project owner before adding them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-tdd-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets and test command summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a failing-then-passing test, minimal implementation changes, refactoring notes, and uncovered risk summaries.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence, metadata.json, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
