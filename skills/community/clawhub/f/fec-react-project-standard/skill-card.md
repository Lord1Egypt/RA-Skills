## Description: <br>
Use when designing or reviewing React + TypeScript project structure, feature/module boundaries, component architecture, hooks organization, routing composition, state/API/error/styling defaults, or repository-wide React conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, or refactor React + TypeScript project structure, module boundaries, component architecture, hooks, routing, state ownership, API layering, error handling, styling defaults, and repository-wide React conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to inspect repository files and run task-relevant commands. <br>
Mitigation: Use it only in repositories where the agent is allowed to inspect project files and run relevant commands; review commands before execution. <br>
Risk: Architecture and refactoring guidance may produce changes that affect module boundaries, routing, state ownership, API handling, or performance behavior. <br>
Mitigation: Review proposed file boundaries and code changes, then verify with the repository's existing tests, type checks, and task-specific validation commands. <br>


## Reference(s): <br>
- [React performance patterns](references/react-performance-patterns.md) <br>
- [React project structure and component boundaries](references/react-project-structure.md) <br>
- [React quality patterns](references/react-quality-patterns.md) <br>
- [React runtime patterns](references/react-runtime-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code snippets and task-relevant shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should respect existing repository conventions and call out relevant loading, error, empty, data, typing, testing, accessibility, and performance considerations.] <br>

## Skill Version(s): <br>
2.7.0 (source: package.json, README, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
