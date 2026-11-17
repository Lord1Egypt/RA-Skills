## Description:

Mirror frontend and backend code across the stack. Invoke when user wants to generate backend from frontend code, generate frontend from backend code, sync existing code across stack, or scaffold full-stack features from one side.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangach](https://clawhub.ai/user/liangach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Code Mirror to generate backend implementations from frontend code, generate frontend integrations from backend code, synchronize types and API calls, and scaffold full-stack features from one side of an application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CRUD, authentication, database, or migration code may affect sensitive application behavior or account data.

Mitigation: Review generated routes, authorization checks, database changes, and migrations before applying them to a real project.

Risk: Mirrored frontend and backend code may mismatch request shapes, response shapes, validation rules, or error handling.

Mitigation: Compare generated code against the source-side contracts and run project tests before deployment.

## Reference(s):

- [Code Mirror source repository](https://github.com/liangach/code-mirror)
- [Code Mirror provenance commit](https://github.com/liangach/code-mirror/commit/6a3a80259406d62b02ba236b19310cd11726e976)
- [Code Mirror ClawHub skill page](https://clawhub.ai/liangach/skills/code-mirror)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with file-path headings and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide full generated files or diffs depending on the requested sync operation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
