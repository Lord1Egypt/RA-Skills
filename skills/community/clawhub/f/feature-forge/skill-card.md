## Description: <br>
Generates complete features from natural language, including components, API routes, migrations, types, and tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Feature Forge to implement full-stack Next.js App Router feature slices from a natural-language request, including UI, schema, API, auth, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad multi-file changes across application code, API routes, tests, and database migrations. <br>
Mitigation: Run it on a clean branch and review the planned file list and final diff before accepting the changes. <br>
Risk: Generated migrations, API routes, and auth changes can affect production data access or authorization behavior. <br>
Mitigation: Inspect schema, RLS, API, and auth changes carefully and test them in a non-production environment before deployment. <br>
Risk: The skill's workflow may prepare or create a commit before the user has fully reviewed the diff. <br>
Mitigation: Do not allow commits until a human has checked the generated code, tests, and migration behavior. <br>


## Reference(s): <br>
- [Feature Forge ClawHub listing](https://clawhub.ai/guifav/feature-forge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify multiple project files, create database migrations, run local checks, and prepare a git commit when allowed by the agent environment.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
