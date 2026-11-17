## Description:

Builds practical mini-apps and web tools through a guided FÓRMULA 100K workflow, favoring simple single-file HTML apps unless the requested use case requires a more advanced stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and builders use this skill to turn a short brief into a working mini-app, test it locally, and prepare or publish it through Vercel when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may publish apps to Vercel with a user's token without a clear confirmation gate.

Mitigation: Require explicit user confirmation before every deployment and before using any Vercel token or account session.

Risk: The skill may send generated deliverables through Telegram without a clear confirmation gate.

Mitigation: Require explicit user confirmation before sending files, links, or app outputs to external channels.

Risk: The skill contains conflicting approval guidance for deployment workflows.

Mitigation: Apply the stricter rule in operation: pause for confirmation before deployment, token use, login, or external sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/constructor-miniapps-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated app files, code snippets, and deployment commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce single-file HTML apps by default, or multi-file projects when the brief requires services such as databases, payments, server-side API calls, or browser extensions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
