## Description: <br>
Mirror frontend and backend code across the stack. Invoke when user wants to generate backend from frontend code, generate frontend from backend code, sync existing code across stack, or scaffold full-stack features from one side. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangach](https://clawhub.ai/user/liangach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Code Mirror to generate matching frontend or backend code from the opposite side of an application stack, including API contracts, data models, routes, validation logic, typed clients, hooks, and scaffolding for full-stack features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated routes or CRUD logic may create, update, or delete application data incorrectly if applied without review. <br>
Mitigation: Review generated CRUD, authentication, authorization, validation, and error-handling code before applying it to a project. <br>
Risk: The skill may read project files to infer stack details and code structure. <br>
Mitigation: Use it in workspaces where project source access is appropriate and avoid exposing unrelated sensitive files. <br>


## Reference(s): <br>
- [Code Mirror on ClawHub](https://clawhub.ai/liangach/code-mirror) <br>
- [Server-resolved GitHub provenance](https://github.com/liangach/code-mirror) <br>
- [Publisher profile](https://clawhub.ai/user/liangach) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with file paths, code blocks, diffs, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code should be reviewed for correctness, security, and fit with the existing project before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
