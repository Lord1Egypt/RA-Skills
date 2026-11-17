## Description:

Build, run, and share a simple full-stack web application with a TypeScript Express backend, React frontend, SQLite database, and public LiteApp URL for demos, testing, or review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, run, deploy, and manage small React, Express, TypeScript, and SQLite web apps in a workspace, then expose them through a shared public LiteApp URL for demos, testing, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated apps are reachable through public port 33333 and may have weak default security.

Mitigation: Use disposable demo data by default, restrict network exposure where possible, and add authentication before using the generated app with sensitive or production data.

Risk: Long-running app processes may inherit the agent environment.

Mitigation: Limit which environment variables child processes receive and avoid placing secrets in the agent environment before deployment.

Risk: Generated app metadata and user-controlled content may be rendered by the app.

Mitigation: Escape or validate user-controlled metadata and content before presenting the app to untrusted viewers.

## Reference(s):

- [Autoload Integration Guide](references/autoload.md)
- [Scaffold Commands](references/scaffold.md)
- [Script Contracts](references/scripts.md)
- [Stack Guide](references/stack.md)
- [UI Style Guide](references/ui-style.md)
- [ClawHub Skill Page](https://clawhub.ai/kadbbz/skills/develop-and-deploy-web-app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with shell commands, generated project files, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace app files, registry metadata, documentation files, and local Node.js processes.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
