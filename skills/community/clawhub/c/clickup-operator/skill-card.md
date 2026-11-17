## Description:

Route ClickUp ideas, to-dos, and project work with operator-style defaults. Use when the user wants tasks or ideas created, moved, assigned, due-dated, promoted into project lists, or read back from ClickUp without unnecessary confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spotlight-revenue](https://clawhub.ai/user/spotlight-revenue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to let an agent create, route, update, and read ClickUp work using concise operator-style defaults. It is intended for configured ClickUp workspaces where the user has confirmed list, assignee, due-date, and status defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and update real ClickUp tasks with low confirmation when a request is clear.

Mitigation: Install it only for users who want direct ClickUp actions, and add confirmation rules for moves, status changes, due-date changes, or reassignment in shared workspaces.

Risk: Incorrect workspace, list, assignee, due-date, or status defaults can route work to the wrong place.

Mitigation: Confirm discovered defaults with the user, save configuration only after confirmation, and run the safe live smoke test before normal use.

Risk: ClickUp authentication material and tokens may be exposed if handled casually during setup.

Mitigation: Keep token handling private and use the documented onboarding flow to verify the connection without exposing credentials in the skill body.

## Reference(s):

- [ClickUp Operator Routing Rules](references/routing-rules.md)
- [ClickUp Operator Configuration](references/configuration.md)
- [ClickUp Operator Guided Onboarding](references/guided-onboarding.md)
- [ClickUp Structure Discovery](references/structure-discovery.md)
- [ClickUp Operator Safe Live Validation](references/safe-live-validation.md)
- [ClickUp Operator Public Packaging](references/public-packaging.md)
- [Configuration Template](templates/config.template.yaml)
- [Configuration Example](templates/config.example.yaml)
- [ClickUp Operator Test Cases](examples/test-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses with configuration YAML and concise action confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update live ClickUp tasks through the connected ClickUp tool surface after setup and validation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
